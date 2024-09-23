
# QGIS

The principle is to retrieve the signed URLs and use them to open remote
rasters in QGIS.

## Retrieve the signed URL

We begin with importing `pystac_client` and `dinamis_sdk` and 
instantiate a STAC client ready to be used with your DINAMIS account:

```python
from pystac_client import Client
from dinamis_sdk import sign_inplace

api = Client.open(
    'https://stacapi-cdos.apps.okd.crocc.meso.umontpellier.fr', 
    modifier=sign_inplace
)
```
From the set or results `res`, we can print the *src_xs* and *src_pan* assets 
URLs:

```python
for item in res.items():
    print(f"Links for {item.id}:")
    print(item.assets['src_xs'].href)
    print(item.assets['src_pan'].href)
```

## Open COG files in QGIS

To open one COG in QGIS, follow these steps:

- Copy one link
- In QGIS: *Layer* > *Add layer* > *Add raster layer*
- In *Source type*, select *Protocol: HTTP(S), cloud, etc*
- Paste the copied link in the *url* field

You can then process the remote COGs as any raster with your favorite tool 
from QGIS.

!!! Warning

    QGIS must be at least **3.18 (Firenze)** to open remote COG files provided 
    by Dinamis-SDK prototype.
