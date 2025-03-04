"""Settings from environment variables."""

import os
from pydantic_settings import BaseSettings
from pydantic.types import NonNegativeInt, PositiveInt, PositiveFloat
import appdirs  # type: ignore
from .utils import get_logger_for

log = get_logger_for(__name__)

# Constants
APP_NAME = "dinamis_sdk_auth"
MAX_URLS = 64
S3_STORAGE_DOMAIN = "meso.umontpellier.fr"
DEFAULT_SIGNING_ENDPOINT = (
    "https://s3-signing-cdos.apps.okd.crocc.meso.umontpellier.fr/"
)


class Settings(BaseSettings):
    """Environment variables."""

    dinamis_sdk_ttl_margin: NonNegativeInt = 1800
    dinamis_sdk_url_duration: NonNegativeInt = 0
    dinamis_sdk_config_dir: str = ""
    dinamis_sdk_access_key: str = ""
    dinamis_sdk_secret_key: str = ""
    dinamis_sdk_retry_total: PositiveInt = 10
    dinamis_sdk_retry_backoff_factor: PositiveFloat = 0.8
    dinamis_sdk_digning_disable_auth: bool = False
    dinamis_sdk_signing_endpoint: str = DEFAULT_SIGNING_ENDPOINT

    def model_post_init(self, __context):
        """Signing endpoint validation module."""
        if not self.dinamis_sdk_signing_endpoint.endswith("/"):
            self.dinamis_sdk_signing_endpoint = self.dinamis_sdk_signing_endpoint + "/"


ENV = Settings()


def get_config_path() -> str | None:
    """Get path to config directory (usually in ~/.config/)."""
    log.debug("Get config path")
    cfg_path = ENV.dinamis_sdk_config_dir or appdirs.user_config_dir(appname=APP_NAME)
    if not os.path.exists(cfg_path):
        try:
            os.makedirs(cfg_path)
            log.debug("Config dir created in %s", cfg_path)
        except PermissionError:
            log.warning("Unable to use config dir %s", cfg_path)
            cfg_path = None
    else:
        log.debug("Using existing config dir %s", cfg_path)
    return cfg_path
