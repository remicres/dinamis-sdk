"""Dinamis SDK module."""
import pkg_resources
__version__ = pkg_resources.require("dinamis-sdk")[0].version
from dinamis_sdk.s3 import (
    sign,
    sign_inplace,
    sign_urls,
    sign_item,
    sign_asset,
    sign_item_collection
)  # noqa
from dinamis_sdk import auth  # noqa
