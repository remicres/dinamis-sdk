"""Spot 6/7 STAC items retrieval test."""

import requests

import pystac_client

import dinamis_sdk

api = pystac_client.Client.open(
    "https://stacapi-cdos.apps.okd.crocc.meso.umontpellier.fr",
    modifier=dinamis_sdk.sign_inplace,
)
res = api.search(
    bbox=[-3.75, 30, 10, 60],
    datetime=["2017-01-01", "2022-12-31"],
    collections=["spot-6-7-drs"],
)
urls = [item.assets["src_xs"].href for item in res.items()]
print(f"{len(urls)} items found")
assert len(urls) > 1000

response = requests.get(urls[0], timeout=10)
assert response.status_code == 200
