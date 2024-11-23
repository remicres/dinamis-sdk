"""Module dedicated to OAuth2 device flow."""
import datetime
import io
import json
import os
import time
from abc import abstractmethod
from typing import Dict
import requests
from pydantic import BaseModel  # pylint: disable = no-name-in-module
import qrcode
from .utils import (
    log, JWT_FILE, TOKEN_ENDPOINT, AUTH_BASE_URL, settings, create_session
)


class JWT(BaseModel):  # pylint: disable = R0903
    """JWT model."""

    access_token: str
    expires_in: int
    refresh_token: str
    refresh_expires_in: int
    token_type: str


class DeviceGrantResponse(BaseModel):  # pylint: disable = R0903
    """Device grant login response model."""

    verification_uri_complete: str
    device_code: str
    expires_in: int
    interval: int


class GrantMethodBase:
    """Base class for grant methods."""

    headers: Dict[str, str] = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    token_endpoint = TOKEN_ENDPOINT
    base_url = AUTH_BASE_URL
    keycloak_realm = "dinamis"
    client_id: str

    @abstractmethod
    def get_first_token(self) -> JWT:
        """
        Provide the first used token.

        Returns:
            Token

        """
        raise NotImplementedError

    @property
    def data_base(self) -> Dict[str, str]:
        """Base payload."""
        return {
            "client_id": self.client_id,
            "scope": "openid offline_access"
        }

    def refresh_token(self, old_jwt: JWT) -> JWT:
        """
        Refresh the token.

        Args:
            old_jwt: Old token

        Returns:
            New token

        """
        log.debug("Refreshing token")
        assert old_jwt, "JWT is empty"
        data = self.data_base.copy()
        data.update({
            "refresh_token": old_jwt.refresh_token,
            "grant_type": "refresh_token"
        })
        ret = requests.post(
            self.token_endpoint,
            headers=self.headers,
            data=data,
            timeout=10
        )
        if ret.status_code == 200:
            log.debug(ret.text)
            return JWT(**ret.json())
        raise ConnectionError("Unable to refresh token")


class DeviceGrant(GrantMethodBase):
    """Device grant method."""

    client_id = "gdal"

    def get_first_token(self) -> JWT:
        """
        Get the first token.

        Returns:
            JWT token

        """
        device_endpoint = f"{self.base_url}/auth/device"

        log.debug("Getting token using device authorization grant")
        ret = requests.post(
            device_endpoint,
            headers=self.headers,
            data=self.data_base,
            timeout=10
        )
        if ret.status_code == 200:
            response = DeviceGrantResponse(**ret.json())
            verif_url_comp = response.verification_uri_complete
            log.info("Open the following URL in your browser to grant access:")
            log.info("\033[92m %s \033[0m", verif_url_comp)

            # QR code
            qr_code = qrcode.QRCode()
            qr_code.add_data(verif_url_comp)
            buffer = io.StringIO()
            qr_code.print_ascii(out=buffer)
            buffer.seek(0)
            log.info(buffer.read())

            log.info("Waiting for authentication...")
            start = time.time()
            data = self.data_base.copy()
            data.update({
                "device_code": response.device_code,
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code"
            })
            while True:
                ret = requests.post(
                    self.token_endpoint,
                    headers=self.headers,
                    data=data,
                    timeout=10
                )
                elapsed = time.time() - start
                log.debug("Elapsed: %s, status: %s", elapsed, ret.status_code)
                if elapsed > response.expires_in:
                    raise ConnectionError("Authentication link has expired.")
                if ret.status_code != 200:
                    time.sleep(response.interval)
                else:
                    return JWT(**ret.json())
        raise ConnectionError("Unable to authenticate with the SSO")


class OAuth2Session:
    """Class to start an OAuth2 session."""

    def __init__(self, grant_type: GrantMethodBase = DeviceGrant):
        """
        Initialize.

        Args:
            grant_type: grant type

        """
        self.grant = grant_type()
        self.jwt_ttl_margin_seconds = 60
        self.jwt_issuance = datetime.datetime(year=1, month=1, day=1)
        self.jwt = None

    def save_token(self, now: datetime.datetime):
        """
        Save the JWT to disk.

        Args:
            now: current date

        """
        self.jwt_issuance = now
        if JWT_FILE:
            try:
                with open(JWT_FILE, 'w', encoding='UTF-8') as file:
                    json.dump(self.jwt.dict(), file)
                log.debug("Token saved in %s", JWT_FILE)
            except IOError as io_err:
                log.warning("Unable to save token (%s)", io_err)

    def refresh_if_needed(self):
        """Refresh the token if ttl is too short."""
        ttl_margin_seconds = 30
        now = datetime.datetime.now()
        jwt_expires_in = datetime.timedelta(seconds=self.jwt.expires_in)
        access_token_ttl = self.jwt_issuance + jwt_expires_in - now
        access_token_ttl_seconds = access_token_ttl.total_seconds()
        log.debug("access_token_ttl is %s", access_token_ttl_seconds)
        if access_token_ttl_seconds >= ttl_margin_seconds:
            # Token is still valid
            log.debug(
                "Credentials from %s still valid", JWT_FILE
            )
            return
        if access_token_ttl_seconds < ttl_margin_seconds:
            # Access token in not valid, but refresh might be
            try:
                self.jwt = self.grant.refresh_token(self.jwt)
            except ConnectionError as con_err:
                log.warning(
                    "Unable to refresh token (reason: %s). "
                    "Renewing initial authentication.",
                    con_err
                )
                self.jwt = self.grant.get_first_token()
        else:
            self.jwt = self.grant.get_first_token()
        self.save_token(now)

    def get_access_token(self) -> str:
        """Return the access token."""
        if not self.jwt:
            # First JWT initialisation
            if JWT_FILE and os.path.isfile(JWT_FILE):
                log.debug("Trying to grab credentials from %s", JWT_FILE)
                try:
                    with open(JWT_FILE, encoding='UTF-8') as json_file:
                        self.jwt = JWT(**json.load(json_file))
                except FileNotFoundError as error:
                    log.warning(
                        "Warning: can't use token from file %s (%s)",
                        JWT_FILE,
                        error
                    )
            if not self.jwt:
                # if JWT is still None, we use the grant method
                self.jwt = self.grant.get_first_token()
                self.save_token(datetime.datetime.now())

        self.refresh_if_needed()

        return self.jwt.access_token


class TokenServer:
    """Token server."""

    def __init__(self, endpoint: str, retry_total=5, retry_backoff_factor=0.8):
        """Initialize the token server."""
        self.endpoint = endpoint
        self.session = create_session(
            retry_total=retry_total,
            retry_backoff_factor=retry_backoff_factor
        )
        log.info("Using Token Server: %s", self.endpoint)

    def get_access_token(self) -> str:
        """Return the access token."""
        return self.session.get(self.endpoint, timeout=10).json()


session = TokenServer(settings.dinamis_sdk_token_server) \
    if settings.dinamis_sdk_token_server else OAuth2Session()


def _get_access_token():
    """Get an access token."""
    return session.get_access_token()


get_access_token = _get_access_token


def set_access_token_fn(func):
    """
    Set a custom access token accessor.

    Args:
        func: access token accessor

    """
    global get_access_token
    get_access_token = func
