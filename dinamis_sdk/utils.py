"""
Some helpers.
"""
import os
import logging

SIGNED_URL_TTL_MARGIN = 1800  # 30 minutes
logging.basicConfig(level=os.environ.get("LOGLEVEL") or "INFO")
log = logging.getLogger("dinamis_sdk")
