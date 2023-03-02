# DINAMIS-SDK

Ease the access to Very High Spatial Resolution imagery from DINAMIS.

## Installation

```commandline
pip install https://gitlab.irstea.fr/dinamis/dinamis-sdk/-/archive/main/dinamis-sdk-main.zip
```

## Quickstart

```python
import dinamis_sdk
import pystac_client

api = pystac_client.Client.open(
   'https://stacapi-dinamis.apps.okd.crocc.meso.umontpellier.fr',
   modifier=dinamis_sdk.sign_inplace,
)
```

To process the COG files remotely with the *vsicurl* driver, the following software must be up-to-date:

| Software | Minimum version |
|----------|-----------------|
| GDAL     | 3.4.1           |
| QGIS     | 3.18 (Firenze)  |
| OTB      | 8.1.1           |
 | PyOTB    | 1.5.4           |

### Example

Mosaic some XS images with [pyotb](https://pypi.org/project/pyotb/) over Camargue area

```python
import pyotb
results = api.search(bbox=[4, 42.99, 5, 44.05], datetime=['2020-01-01', '2022-01-02'])
imgs = [f"/vsicurl/{res.assets['src_xs'].href}" for res in results.items()]
pyotb.Mosaic({"il": imgs, "out": "raster.tif"})
```