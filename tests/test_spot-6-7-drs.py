import dinamis_sdk
import pystac_client

api = pystac_client.Client.open(
   'https://stacapi-dinamis.apps.okd.crocc.meso.umontpellier.fr',
   modifier=dinamis_sdk.sign_inplace,
)
res = api.search(
    bbox=[-3.75, 30, 10, 60],
    datetime=["2017-01-01", "2022-12-31"],
    collections=["spot-6-7-drs"]
)
urls = [item.assets['src_xs'].href for item in res.items()]
print(len(urls))
assert len(urls) > 1000

