# DINAMIS-SDK

Ease the access to Very High Spatial Resolution imagery from DINAMIS.

<p align="center">
<img src="https://theia.sedoo.fr/wp-content-theia/uploads/sites/6/2020/05/Logo_DINAMIS_300px.png">
</p>

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

Follow the instructions for the first connection.
The credentials are then valid for 5 days. Every time you use `dinamis_sdk.sign_inplace`, the credentials are renewed
for another 5 days without logging in again.

## Example

To process the COG files remotely with the *vsicurl* driver, the following software must be up-to-date:

| Software | Minimum version |
|----------|-----------------|
| GDAL     | 3.4.1           |
| QGIS     | 3.18 (Firenze)  |
| OTB      | 8.1.1           |
 | PyOTB    | 1.5.4           |

Mosaic some XS images with [pyotb](https://pypi.org/project/pyotb/) over Camargue area

```python
import pyotb

res = api.search(
    bbox=[4, 42.99, 5, 44.05],
    datetime=['2020-01-01', '2022-01-02']
)
imgs = [f"/vsicurl/{r.assets['src_xs'].href}" for r in res.items()]
pyotb.Mosaic({"il": imgs, "out": "raster.tif"})
```

## Access keys

It is also possible to use access keys for a permanent access.
Access keys can be provided to the library with the included configuration CLI:

```commandline
dinamis-sdk-cli 
```

The command above will ask you the access key ID and secret key in interactive mode. The credentials will be saved in 
the user's config directory.

> **Warning**
> Never enter credentials on insecure platforms (e.g. online notebooks, etc) since they are stored on disk.
> Use `dinamis-sdk-cli` from safe devices only.

## Signed URLs

The signed URLs for STAC objects assets are valid during 7 days starting when `dinamis_sdk.sign_inplace` has been 
called.
`dinamis_sdk.sign_inplace` can also directly be applied on a particular `pystac.item`, `pystac.collection`, 
`pystac.asset` or any URL as `str`.
The API reference can be found [here](https://s3-signing-dinamis.apps.okd.crocc.meso.umontpellier.fr/docs).

## Terms of service 

[Link](https://ids-dinamis.data-terra.org/web/guest/37)
