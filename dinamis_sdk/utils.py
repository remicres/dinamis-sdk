"""Some helpers."""
import os
import logging
import json
import appdirs
from pydantic import BaseModel  # pylint: disable = no-name-in-module

# Signed TTL margin default to 1800 seconds (30 minutes), or env. var.
SIGNED_URL_TTL_MARGIN = os.environ.get("DINAMIS_SDK_TTL_MARGIN") or 1800
logging.basicConfig(level=os.environ.get("LOGLEVEL") or "INFO")
log = logging.getLogger("dinamis_sdk")

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
