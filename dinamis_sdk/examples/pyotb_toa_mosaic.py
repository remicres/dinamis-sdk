"""TOA images mosaicing with pyotb."""
from pystac_client import Client
import pyotb
from dinamis_sdk import sign_inplace

api = Client.open(
    'https://stacapi-dinamis.apps.okd.crocc.meso.umontpellier.fr',
    modifier=sign_inplace
)

res = api.search(
    bbox=[4, 42.99, 5, 44.05],
    datetime=["2022-01-01", "2022-12-25"],
    collections=["spot-6-7-drs"]
)

urls = [f"/vsicurl/{r.assets['src_xs'].href}" for r in res.items()]
toa_images = [pyotb.OpticalCalibration({"in": url}) for url in urls]
mosa = pyotb.Mosaic({"il": toa_images})
mosa.write("toa_mosa.tif?&box=5000:5000:4096:4096")
