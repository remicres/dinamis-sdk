"""Settings from environment variables."""

import os
from pydantic_settings import BaseSettings
from pydantic.types import NonNegativeInt, PositiveInt, PositiveFloat
import appdirs  # type: ignore
from .utils import get_logger_for

log = get_logger_for(__name__)


class Settings(BaseSettings):
    """Environment variables."""

    dinamis_sdk_ttl_margin: NonNegativeInt = 1800
    dinamis_sdk_url_duration: NonNegativeInt = 0
    dinamis_sdk_bypass_auth_api: str = ""  # Endpoint with no authentication.
    dinamis_sdk_config_dir: str = ""
    dinamis_sdk_access_key: str = ""
    dinamis_sdk_secret_key: str = ""
    dinamis_sdk_retry_total: PositiveInt = 10
    dinamis_sdk_retry_backoff_factor: PositiveFloat = 0.8


# Constants
APP_NAME = "dinamis_sdk_auth"
MAX_URLS = 64
S3_STORAGE_DOMAIN = "meso.umontpellier.fr"
SIGNING_ENDPOINT = "https://s3-signing-cdos.apps.okd.crocc.meso.umontpellier.fr/"
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
