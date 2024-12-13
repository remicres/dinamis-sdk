#!/usr/bin/env python

import pystac
import pystac_client
import requests

import dinamis_sdk

api = pystac_client.Client.open(
    "https://stacapi-cdos.apps.okd.crocc.meso.umontpellier.fr",
    modifier=dinamis_sdk.sign_inplace,
)
res = api.search(
    bbox=[3.75, 43.58, 3.95, 43.67],
    datetime=["2017-01-01", "2022-12-31"],
    collections=["super-sentinel-2-l2a"],
)
urls = [item.assets["img"].href for item in res.items()]
assert len(urls) == 672

# ItemCollection (bug #17)
ic: pystac.ItemCollection = pystac.item_collection.ItemCollection(res.items())
dinamis_sdk.sign_inplace(ic)

item = ic.items[0]
_, asset = next(iter(item.get_assets().items()))

response = requests.get(asset.href, timeout=5)
response.raise_for_status()
