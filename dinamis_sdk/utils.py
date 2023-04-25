"""Some helpers."""
import appdirs
import json
import logging
import os
from pydantic import BaseModel  # pylint: disable = no-name-in-module

logging.basicConfig(level=os.environ.get("LOGLEVEL") or "INFO")
log = logging.getLogger("dinamis_sdk")

# Signed TTL margin default to 1800 seconds (30 minutes), or env. var.
ttl_margin_from_env = os.environ.get("DINAMIS_SDK_TTL_MARGIN")
if ttl_margin_from_env:
    if ttl_margin_from_env.isdigit():
        ttl_margin_from_env = int(ttl_margin_from_env)
        log.info(
            "Setting TTL margin from environment variable to %s seconds",
            ttl_margin_from_env
        )
SIGNED_URL_TTL_MARGIN = ttl_margin_from_env or 1800

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
        logging.debug("Setting file %s does not exist", settings_file)
