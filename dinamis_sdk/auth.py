"""
Module dedicated to OAuth2 client side implementations
"""
import datetime
import io
import json
import os
import time
from abc import abstractmethod
from typing import Dict
import requests
from pydantic import BaseModel, Field
import qrcode
from .utils import log, jwt_file


class JWT(BaseModel):
    """JWT model"""
    access_token: str = Field(alias="access_token")
    expires_in: int = Field(alias="expires_in")
    refresh_token: str = Field(alias="refresh_token")
    refresh_expires_in: int = Field(alias="refresh_expires_in")
    token_type: str = Field(alias="token_type")


class DeviceGrantResponse(BaseModel):
    """Device grant login response model"""
    verification_uri_complete: str = Field(alias="verification_uri_complete")
    device_code: str = Field(alias="device_code")
    expires_in: int = Field(alias="expires_in")
    interval: int = Field(alias="interval")


class GrantMethodBase:
    """Base class for grant methods"""
    headers: Dict[str, str] = {"Content-Type": "application/x-www-form-urlencoded"}
    keycloak_server_url = "https://keycloak-dinamis.apps.okd.crocc.meso.umontpellier.fr/auth"
    keycloak_realm = "dinamis"
    base_url = f"{keycloak_server_url}/realms/{keycloak_realm}/protocol/openid-connect"
    token_endpoint = f"{base_url}/token"
    client_id: str

    @abstractmethod
    def get_first_token(self) -> JWT:
        """
        Provide the first used token.

        Returns:
            JWT

        """
        raise NotImplementedError

    @property
    def data_base(self) -> Dict[str, str]:
        """
        Base payload.
        """
        return {
            "client_id": self.client_id,
            "scope": "offline_access"
        }

    def refresh_token(self, old_jwt: JWT) -> JWT:
        """
        Refresh the token.

        :return: JWT

        """
        log.debug("Refreshing token")
        assert old_jwt, "JWT is empty"
        data = self.data_base.copy()
        data.update({"refresh_token": old_jwt.refresh_token, "grant_type": "refresh_token"})
        ret = requests.post(self.token_endpoint, headers=self.headers, data=data, timeout=10)
        if ret.status_code == 200:
            log.debug(ret.text)
            return JWT(**ret.json())
        raise ConnectionError("Unable to refresh token")


class DeviceGrant(GrantMethodBase):
    """Device grant method"""
    client_id = "gdal"

    def get_first_token(self) -> JWT:
        """
        Get the first token

        Returns:
            JWT token

        """
        device_endpoint = f"{self.base_url}/auth/device"

        log.debug("Getting token using device authorization grant")
        ret = requests.post(device_endpoint, headers=self.headers, data=self.data_base, timeout=10)
        if ret.status_code == 200:
            response = DeviceGrantResponse(**ret.json())
            verif_url_comp = response.verification_uri_complete
            log.info("Open the following URL in your browser to grant access:")
            log.info("\033[92m%s\033[0m",verif_url_comp)

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
    """
    Class to start an OAuth2 session
    """

    def __init__(self, grant_type: GrantMethodBase = DeviceGrant):
        """

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

        Params:
            now: date of now

        """
        self.jwt_issuance = now
        if jwt_file:
            try:
                with open(jwt_file, 'w', encoding='UTF-8') as file:
                    json.dump(self.jwt.dict(), file)
                log.debug("Token saved in %s", jwt_file)
            except IOError as io_err:
                log.warning("Unable to save token (%s)", io_err)

    def refresh_if_needed(self):
        """
        Refresh the token if ttl is too short.

        """
        ttl_margin_seconds = 30
        now = datetime.datetime.now()
        jwt_expires_in = datetime.timedelta(seconds=self.jwt.expires_in)
        access_token_ttl = (self.jwt_issuance + jwt_expires_in - now).total_seconds()
        log.debug("access_token_ttl is %s", access_token_ttl)
        if access_token_ttl >= ttl_margin_seconds:
            # Token is still valid
            return
        if access_token_ttl < ttl_margin_seconds:
            # Access token in not valid, but refresh might be
            try:
                self.jwt = self.grant.refresh_token(self.jwt)
            except ConnectionError as con_err:
                log.warning(
                    "Unable to refresh token (reason: %s). Renewing initial authentication.",
                    con_err
                )
                self.jwt = self.grant.get_first_token()
        else:
            self.jwt = self.grant.get_first_token()
        self.save_token(now)

    def get_access_token(self) -> str:
        """
        Get the access token.

        Returns:
            access token

        """
        if not self.jwt:
            # First JWT initialisation
            if jwt_file and os.path.isfile(jwt_file):
                log.debug("Trying to grab credentials from %s", jwt_file)
                try:
                    with open(jwt_file, encoding='UTF-8') as json_file:
                        self.jwt = self.grant.refresh_token(JWT(**json.load(json_file)))
                        if self.jwt:
                            log.debug("Credentials from %s still valid", jwt_file)
                except Exception as error:
                    log.warning("Warning: can't use token from file %s (%s)", jwt_file, error)
            if not self.jwt:
                # if JWT is still None, we use the grant method
                self.jwt = self.grant.get_first_token()
                self.save_token(datetime.datetime.now())

        self.refresh_if_needed()

        return self.jwt.access_token


session = OAuth2Session()


def _get_access_token():
    return session.get_access_token()


get_access_token = _get_access_token


def set_access_token_fn(func):
    """
    Set a custom access token accessor

    Params:
        func: access token accessor

    """
    global get_access_token
    get_access_token = func
