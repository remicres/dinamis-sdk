"""TOA images mosaicing with pyotb."""
from pystac_client import Client
import pyotb
from dinamis_sdk import sign_inplace

api = Client.open(
    'https://stacapi-dinamis.apps.okd.crocc.meso.umontpellier.fr',
    modifier=sign_inplace
)

year = 2022
bbox = [4, 42.99, 5, 44.05]
res = api.search(bbox=bbox, datetime=[f'{year}-01-01', f'{year}-12-25'])
urls = [f"/vsicurl/{r.assets['src_xs'].href}" for r in res.items()]
toa_images = [pyotb.OpticalCalibration({"in": url}) for url in urls]
mosa = pyotb.Mosaic({"il": toa_images})
mosa.write("toa_mosa.tif?&box=5000:5000:4096:4096")
