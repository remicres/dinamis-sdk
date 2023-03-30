# Dinamis-SDK

Ease the access to Very High Spatial Resolution imagery from Dinamis.


<div align="center">
<div id="qr" style="display:inline-block; margin: auto; align: center; vertical-align: middle; height:3cm;" >
<img src="https://upload.wikimedia.org/wikipedia/fr/thumb/2/2a/Logo-INRAE_Transparent.svg/2560px-Logo-INRAE_Transparent.svg.png" style="height:1.5cm; padding:5px">
<img src="https://theia.sedoo.fr/wp-content-theia/uploads/sites/6/2020/05/Logo_DINAMIS_300px.png" style="height:1.75cm; padding: 5px">
</div>
<br>
<a href="https://gitlab.irstea.fr/dinamis/dinamis-sdk/-/releases">
<img src="https://gitlab.irstea.fr/dinamis/dinamis-sdk/-/badges/release.svg">
</a>
<a href="https://gitlab.irstea.fr/dinamis/dinamis-sdk/-/commits/main">
<img src="https://gitlab.irstea.fr/dinamis/dinamis-sdk/badges/main/pipeline.svg">
</a>
<a href="LICENSE">
<img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg">
</a>

</div>

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

## Credentials expiry

### Login

The credentials are then valid for 5 days. Every time 
`dinamis_sdk.sign_inplace` is called, the credentials are renewed for another 
5 days. After 5 days idle, you will have to log in again.

### Signed URLs

The signed URLs for STAC objects assets are valid during 7 days starting after 
`dinamis_sdk.sign_inplace` is called. `dinamis_sdk.sign_inplace` can also be 
applied directly on a particular `pystac.item`, `pystac.collection`,
`pystac.asset` or any URL as `str`.

### Processing remote COGs locally

The following demonstrates how to process remote COGs locally with your 
favorite tool.

The following example performs the **mosaic of XS images** with 
[pyotb](https://pypi.org/project/pyotb/) over the Camargue area:

```python
import pyotb

res = api.search(
    bbox=[4, 42.99, 5, 44.05],
    datetime=['2020-01-01', '2022-01-02']
)

vsi_urls = [f"/vsicurl/{r.assets['src_xs'].href}" for r in res.items()]
pyotb.Mosaic({"il": vsi_urls, "out": "raster.tif"})
```

See this [section](#examples.html) for more examples.

### Opening remote COGs in QGIS

From the set or results `res`, we can print the *src_xs* and *src_pan* assets 
URLs:

```python
for item in res.items():
    print(f"Links for {item.id}:")
    print(item.assets['src_xs'].href)
    print(item.assets['src_pan'].href)
```

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

## Additional resources

### API

- [STAC API swagger UI](https://stacapi-dinamis.apps.okd.crocc.meso.umontpellier.fr/api.html)
- [URL signing API swagger UI](https://s3-signing-dinamis.apps.okd.crocc.meso.umontpellier.fr/docs)

### Documentation

- [PySTAC documentation](https://pystac.readthedocs.io/en/stable/api/pystac.html)
- [PySTAC-Client documentation](https://pystac-client.readthedocs.io/en/stable/)
- More information about the [STAC specification](https://stacspec.org/en/about/stac-spec/)

## Contribute

You can open issues or merge requests at 
[INRAE's gitlab](https://gitlab.irstea.fr/dinamis/dinamis-sdk).

## Terms of service 

Please read carefully the 
[terms of service](https://ids-dinamis.data-terra.org/web/guest/37) related to 
the involved products (Spot-6/7, France Mainland, Direct Receiving Station).

## Contact

Rémi Cresson at INRAE dot fr
