import dinamis_sdk.auth as auth
from dinamis_sdk.s3 import sign_inplace
import pkg_resources
__version__ = pkg_resources.require("dinamis-sdk")[0].version
