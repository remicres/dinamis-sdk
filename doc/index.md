# DINAMIS-SDK

Ease the access to Very High Spatial Resolution imagery from DINAMIS.

```python
import dinamis_sdk
import pystac_client

api = pystac_client.Client.open(
   'https://stacapi-dinamis.apps.okd.crocc.meso.umontpellier.fr',
   modifier=dinamis_sdk.sign_inplace,
)
```

## Example

Mosaic some XS images with [pyotb](https://pypi.org/project/pyotb/) over Camargue area

```python
import pyotb
results = api.search(bbox=[4, 42.99, 5, 44.05], datetime=['2020-01-01', '2022-01-02'])
imgs = [f"/vsicurl/{res.assets['src_xs'].href}" for res in results.items()]
pyotb.Mosaic({"il": imgs, "out": "raster.tif"})
```