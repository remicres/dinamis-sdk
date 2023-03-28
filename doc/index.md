# DINAMIS-SDK

Ease the access to Very High Spatial Resolution imagery from DINAMIS.

<p align="center">
<img src="https://theia.sedoo.fr/wp-content-theia/uploads/sites/6/2020/05/Logo_DINAMIS_300px.png">
</p>

!!! Info

    This is a demonstrator for the next-gen platform which should be ready in 
    2024. Only France mainland Spot-6/7 Ortho (Direct Receiving Station) are
    provided.

## Installation

```commandline
pip install dinamis-sdk
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

Follow the instructions for the first connection.

!!! Info

    The credentials are then valid for 5 days. Every time 
    `dinamis_sdk.sign_inplace` is called, the credentials are renewed for 
    another 5 days. After 5 days idle, you will have to log in again.

The signed URLs for STAC objects assets are valid during 7 days starting after 
`dinamis_sdk.sign_inplace` is called. `dinamis_sdk.sign_inplace` can also be 
applied directly on a particular `pystac.item`, `pystac.collection`,
`pystac.asset` or any URL as `str`.
The API reference can be found 
[here](https://s3-signing-dinamis.apps.okd.crocc.meso.umontpellier.fr/docs).

## Example

The following demonstrates how to process remote COGs locally with your 
favorite tool.

!!! Warning

    To process remote COG files with the *vsicurl* driver, the following 
    software must be up-to-date:

    | Software | Minimum version |
    |----------|-----------------|
    | GDAL     | 3.4.1           |
    | QGIS     | 3.18 (Firenze)  |
    | OTB      | 8.1.1           |
    | PyOTB    | 1.5.4           |

Lets mosaic some XS images with [pyotb](https://pypi.org/project/pyotb/) over 
Camargue area:

```python
import pyotb

res = api.search(
    bbox=[4, 42.99, 5, 44.05],
    datetime=['2020-01-01', '2022-01-02']
)

vsi_urls = [f"/vsicurl/{r.assets['src_xs'].href}" for r in res.items()]
pyotb.Mosaic({"il": vsi_urls, "out": "raster.tif"})
```

## Terms of service 

[Link](https://ids-dinamis.data-terra.org/web/guest/37)

## Contact

Rémi Cresson at INRAE dot fr
