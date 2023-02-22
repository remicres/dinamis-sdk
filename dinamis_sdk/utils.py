import os
import logging

logging.basicConfig(level=os.environ.get("LOGLEVEL") or "INFO")
log = logging.getLogger(__name__)
