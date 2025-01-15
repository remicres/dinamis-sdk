"""HTTP connections with various methods."""

from typing import Dict
from ast import literal_eval
from pydantic import BaseModel, ConfigDict
from .utils import get_logger_for, create_session
from .oauth2 import OAuth2Session
from .model import ApiKey
from .settings import ENV, SIGNING_ENDPOINT


log = get_logger_for(__name__)


class BareConnectionMethod(BaseModel):
    """Bare connection method, no extra headers."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    endpoint: str = SIGNING_ENDPOINT

    def get_headers(self) -> Dict[str, str]:
        """Get the headers."""
        return {}

    def model_post_init(self, __context):
        """Post initialization."""
        if not self.endpoint.lower().startswith(("http://", "https://")):
            raise ValueError(f"{self.endpoint} must start with http[s]://")
        if not self.endpoint.endswith("/"):
            self.endpoint += "/"
        return self.endpoint


class OAuth2ConnectionMethod(BareConnectionMethod):
    """OAuth2 connection method."""

    oauth2_session: OAuth2Session = OAuth2Session()

    def get_headers(self):
        """Return the headers."""
        return {"authorization": f"bearer {self.oauth2_session.get_access_token()}"}


class ApiKeyConnectionMethod(BareConnectionMethod):
    """API key connection method."""

    api_key: ApiKey

    def get_headers(self):
        """Return the headers."""
        return self.api_key.to_dict()


class HTTPSession:
    """HTTP session class."""

    def __init__(self, timeout=10):
        """Initialize the HTTP session."""
        self.session = create_session(
            retry_total=ENV.dinamis_sdk_retry_total,
            retry_backoff_factor=ENV.dinamis_sdk_retry_backoff_factor,
        )
        self.timeout = timeout
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self._method = None

    def get_method(self):
        """Get method."""
        log.debug("Get method")
        if not self._method:
            # Lazy instantiation
            self.prepare_connection_method()
        return self._method

    def prepare_connection_method(self):
        """Set the connection method."""
        # Custom server without authentication method
        if ENV.dinamis_sdk_bypass_auth_api:
            self._method = BareConnectionMethod(
                endpoint=ENV.dinamis_sdk_bypass_auth_api
            )

        # API key method
        elif api_key := ApiKey.grab():
            self._method = ApiKeyConnectionMethod(api_key=api_key)

        # OAuth2 method
        else:
            self._method = OAuth2ConnectionMethod()

    def post(self, route: str, params: Dict):
        """Perform a POST request."""
        method = self.get_method()
        url = f"{method.endpoint}{route}"
        headers = {**self.headers, **method.get_headers()}
        log.debug("POST to %s", url)
        response = self.session.post(url, params=params, headers=headers, timeout=10)
        try:
            response.raise_for_status()
        except Exception as e:
            log.error(literal_eval(response.text))
            raise e

        return response


session = HTTPSession()


def get_headers():
    """Return the headers."""
    return session.get_method().get_headers()
