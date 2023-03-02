"""
DINAMIS SDK
"""
from dinamis_sdk.s3 import sign_inplace  # noqa
from dinamis_sdk import auth  # noqa
import pkg_resources
__version__ = pkg_resources.require("dinamis-sdk")[0].version
