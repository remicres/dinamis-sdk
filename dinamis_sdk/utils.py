"""
Some helpers.
"""
import os
import logging
import appdirs
import json
from pydantic import BaseModel

SIGNED_URL_TTL_MARGIN = 1800  # 30 minutes
logging.basicConfig(level=os.environ.get("LOGLEVEL") or "INFO")
log = logging.getLogger("dinamis_sdk")

cfg_pth = appdirs.user_config_dir(appname='dinamis_sdk_auth')
if not os.path.exists(cfg_pth):
    try:
        os.makedirs(cfg_pth)
        log.debug("Config path created in %s", cfg_pth)
    except PermissionError:
        log.warning("Unable to create config path")
        cfg_pth = None
else:
    log.debug("Config path already exist in %s", cfg_pth)

jwt_file = os.path.join(cfg_pth, "token") if cfg_pth else None
log.debug("JWT file is %s", jwt_file)

settings_file = os.path.join(cfg_pth, "settings") if cfg_pth else None
log.debug("Settings file is %s", settings_file)

class StorageCredentials(BaseModel):
    access_key: str
    secret_key: str

credentials = None
if settings_file and os.path.isfile(settings_file):
    try:
        with open(settings_file, encoding='UTF-8') as json_file:
            credentials = StorageCredentials(**json.load(json_file))
    except FileNotFoundError as file_err:
        logging.debug("Setting file %s does not exist", settings_file)