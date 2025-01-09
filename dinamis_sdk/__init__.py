"""Dinamis SDK module."""

# flake8: noqa
import pkg_resources

__version__ = "0.3.8"
from dinamis_sdk.s3 import (
    sign,
    sign_inplace,
    sign_urls,
    sign_item,
    sign_asset,
    sign_item_collection,
    sign_url_put,
)  # noqa
from dinamis_sdk import auth  # noqa
from dinamis_sdk.upload import push
