import dinamis_sdk
import pystac_client
import pystac

api = pystac_client.Client.open(
   'https://stacapi-cdos.apps.okd.crocc.meso.umontpellier.fr',
   modifier=dinamis_sdk.sign_inplace,
)
res = api.search(
    bbox=[3.75, 43.58, 3.95, 43.67],
    datetime=["2017-01-01", "2022-12-31"],
    collections=["super-sentinel-2-l2a"]
)
urls = [item.assets['img'].href for item in res.items()]
assert len(urls) == 672

# ItemCollection (bug #17)
ic = pystac.item_collection.ItemCollection(res.items())
dinamis_sdk.sign_inplace(ic)