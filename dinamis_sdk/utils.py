"""Some helpers."""
import json
import logging
import os
import appdirs
from pydantic import BaseModel  # pylint: disable = no-name-in-module
import requests

# Env vars
ENV_TTL_MARGIN = "DINAMIS_SDK_TTL_MARGIN"
ENV_DURATION_SECS = "DINAMIS_SDK_DURATION_SECONDS"
ENV_BYPASS_API = "DINAMIS_SDK_BYPASS_API"

logging.basicConfig(level=os.environ.get("LOGLEVEL") or "INFO")
log = logging.getLogger("dinamis_sdk")


def _get_seconds(env_var_name: str, default: int = None) -> int:
    val = os.environ.get(env_var_name)
    if val:
        if val.isdigit():
            log.info(
                "Using %s = %s seconds",
                env_var_name,
                val
            )           
        return int(val)
    return default


# Signed TTL margin default to 1800 seconds (30 minutes), or env. var.
SIGNED_URL_TTL_MARGIN = _get_seconds(ENV_TTL_MARGIN, 1800)
SIGNED_URL_DURATION_SECONDS = _get_seconds(ENV_DURATION_SECS)

MAX_URLS = 64
S3_STORAGE_DOMAIN = "meso.umontpellier.fr"
S3_SIGNING_ENDPOINT = \
    "https://s3-signing-cdos.apps.okd.crocc.meso.umontpellier.fr/"

CFG_PTH = appdirs.user_config_dir(appname='dinamis_sdk_auth')
if not os.path.exists(CFG_PTH):
    try:
        os.makedirs(CFG_PTH)
        log.debug("Config path created in %s", CFG_PTH)
    except PermissionError:
        log.warning("Unable to create config path")
        CFG_PTH = None
else:
    log.debug("Config path already exist in %s", CFG_PTH)

JWT_FILE = os.path.join(CFG_PTH, ".token") if CFG_PTH else None
log.debug("JWT file is %s", JWT_FILE)

settings_file = os.path.join(CFG_PTH, ".settings") if CFG_PTH else None
log.debug("Settings file is %s", settings_file)


class StorageCredentials(BaseModel):  # pylint: disable = R0903
    """Credentials model."""

    access_key: str
    secret_key: str


CREDENTIALS = None
if settings_file and os.path.isfile(settings_file):
    try:
        with open(settings_file, encoding='UTF-8') as json_file:
            CREDENTIALS = StorageCredentials(**json.load(json_file))
    except FileNotFoundError:
        log.debug("Setting file %s does not exist", settings_file)


def retrieve_token_endpoint(s3_signing_endpoint: str = S3_SIGNING_ENDPOINT):
    """Retrieve the token endpoint from the s3 signing endpoint."""
    openapi_url = s3_signing_endpoint + "openapi.json"
    log.debug("Fetching OAuth2 endpoint from openapi url %s", openapi_url)
    res = requests.get(
        openapi_url,
        timeout=10,
    )
    res.raise_for_status()
    data = res.json()
    oauth2_defs = data["components"]["securitySchemes"]["OAuth2PasswordBearer"]
    return oauth2_defs["flows"]["password"]["tokenUrl"]


BYPASS_API = os.environ.get(ENV_BYPASS_API)
if BYPASS_API:
    S3_SIGNING_ENDPOINT = ENV_BYPASS_API

# Token endpoint is typically something like: https://keycloak-dinamis.apps.okd
# .crocc.meso.umontpellier.fr/auth/realms/dinamis/protocol/openid-connect/token
TOKEN_ENDPOINT = None if BYPASS_API else retrieve_token_endpoint()
# Auth base URL is typically something like: https://keycloak-dinamis.apps.okd.
# crocc.meso.umontpellier.fr/auth/realms/dinamis/protocol/openid-connect
AUTH_BASE_URL = None if BYPASS_API else TOKEN_ENDPOINT.rsplit('/', 1)[0]

# Token server (optional)
TOKEN_SERVER = os.environ.get("DINAMIS_SDK_TOKEN_SERVER")
