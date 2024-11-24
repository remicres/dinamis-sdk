"""Settings from environment variables."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Holds settings."""

    dinamis_sdk_ttl_margin: int = 1800
    dinamis_sdk_url_duration: int = 0
    dinamis_sdk_bypass_api: str = ""
    dinamis_sdk_token_server: str = ""
    dinamis_sdk_settings_dir: str = ""
    dinamis_sdk_access_key: str = ""
    dinamis_sdk_secret_key: str = ""
