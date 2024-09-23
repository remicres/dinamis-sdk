# Examples

To process remote COG files, the following software must be up-to-date:

| Software | Minimum version |
|----------|-----------------|
| GDAL     | 3.4.1           |
| OTB      | 8.1.2           |
| PyOTB    | 1.5.4           |

All examples begin with importing `pystac_client` and `dinamis_sdk` and 
instantiate a STAC client ready to be used with your DINAMIS account:

```python
from pystac_client import Client
from dinamis_sdk import sign_inplace

api = Client.open(
    'https://stacapi-cdos.apps.okd.crocc.meso.umontpellier.fr', 
    modifier=sign_inplace
)
```

## TOA Mosaic with pyotb

[Source code :fontawesome-brands-gitlab:](https://gitlab.irstea.fr/dinamis/
dinamis-sdk/-/tree/main/dinamis_sdk/examples/pyotb_toa_mosaic.py){ .md-button }

We first perform a STAC search over the camargue area in the year 2022:

```python
res = api.search(
    bbox=[4, 42.99, 5, 44.05], 
    datetime=["2022-01-01", "2022-12-25"],
    collections=["spot-6-7-drs"]
)
```

Then, we append the */vsicurl/* suffix to XS images assets URLs to tell GDAL 
(the underlying raster reader of OTB) that it's a 
[virtual file](https://gdal.org/user/virtual_file_systems.html).
After that, we use the OTB
[`Mosaic`](https://www.orfeo-toolbox.org/CookBook/Applications/app_Mosaic.html)
application to mosaic all XS channels.

```python
urls = [f"/vsicurl/{r.assets['src_xs'].href}" for r in res.items()]
```

Then we build our image processing pipeline with pyotb:

```python
toa_images = [pyotb.OpticalCalibration({"in": url}) for url in urls]
mosa = pyotb.Mosaic({"il": toa_images})
```

At this point, nothing has been processed yet! We still don't have downloaded 
a single pixel of the remote images. We just have built our pipeline, by
declaring some pyob objects connected together. Let's write a subset of the 
output image:

```python
mosa.write("toa_mosa.tif?&box=5000:5000:4096:4096")
```

This action will trigger all the pipeline, and subsequently, the download of 
the needed chunks of remote COG files.

Your can open the resulting *toa_mosa.tif* in QGIS:

![img](images/toa_mosa.jpg)


## NDVI loss with pyotb

[Source code :fontawesome-brands-gitlab:](https://gitlab.irstea.fr/dinamis/
dinamis-sdk/-/tree/main/dinamis_sdk/examples/pyotb_ndvi_loss.py){ .md-button }

The following example show how to compute an NDVI loss over a given extent.
The result is a raster of the NDVI loss between the two specified years.

We use [pyotb](https://pypi.org/project/pyotb/) to process locally the remote 
COGs. This python package uses OTB to chain various applications and perform 
common operations on remote sensing imagery.

```python
import pyotb
```

Not lets create a function to grab some images over a given bounding box, and 
return the resulting mosaic:

```python
def mosa(year):
    res = api.search(
        bbox=[4, 42.99, 5, 44.05], 
        datetime=[f"{year}-01-01", f"{year}-12-25"],
        collections=["spot-6-7-drs"]
    )

    urls = [f"/vsicurl/{r.assets['src_xs'].href}" for r in res.items()]
    return pyotb.Mosaic({"il": urls})
```

As you can see, we first perform a search with the STAC client to find all 
images intersecting the input bounding box. Then, we append the */vsicurl/*
suffix to XS images assets URLs. After that, we mosaic all XS images and return
the pyotb object performing this step (that can be used later with other pyotb 
or OTB objects, or numpy). Note that, at this point, no processing has been 
done so far, we just are building our pipeline, and we don't have executed it
yet.

Then we create another function to compute the NDVI:

```python
def ndvi(xs):
    return pyotb.BandMath({"il": [xs], "exp": "(im1b4-im1b1)/(im1b4+im1b1)"})
```

We can now compute two NDVI mosaics for each year:

```python
ndvi_22 = ndvi(mosa("2022"))
ndvi_21 = ndvi(mosa("2021"))
```

One last step consist in interpolating the values of the second NDVI mosaic 
over the first one. This is done using the OTB 
[`Superimpose`](https://www.orfeo-toolbox.org/CookBook/Applications/app_Superimpose.html) 
application:

```python
delta_ndvi = ndvi_22 - pyotb.Superimpose({"inr": ndvi_22, "inm": ndvi_21})
```

Finally, we can write the output in a file, using an 
[OTB extended filename](https://www.orfeo-toolbox.org/CookBook/ExtendedFilenames.html)
to write only a subset of the generated image.

```python
delta_ndvi.write("/data/raster_dndvi.tif?&box=5000:5000:4096:4096")
```

Your can open the resulting *raster_dndvi.tif* in QGIS:

![img](images/ndvi_loss.jpg)

## Metadata fetching with RasterIO

[Source code :fontawesome-brands-gitlab:](https://gitlab.irstea.fr/dinamis/
dinamis-sdk/-/tree/main/dinamis_sdk/examples/rio_metadata.py){ .md-button }

We start by importing RasterIO:

```python
import rasterio.features
import rasterio.warp
```

Like the precedent examples, we perform a STAC search over the camargue area 
during year 2022:

```python
year = 2022
bbox = [4, 42.99, 5, 44.05]
res = api.search(bbox=bbox, datetime=[f'{year}-01-01', f'{year}-12-25'])
```

We then loop over the STAC search results and fetch the metadata:

```python
for item in res.items():
    url =  item.assets["src_xs"].href
    with rasterio.open(url) as dataset:

        # Read the dataset's valid data mask as a ndarray.
        mask = dataset.dataset_mask()

        # Extract feature shapes and values from the array.
        for geom, val in rasterio.features.shapes(
                mask, transform=dataset.transform
        ):

            # Transform shapes from the dataset's own coordinate
            # reference system to CRS84 (EPSG:4326).
            geom = rasterio.warp.transform_geom(
                dataset.crs, 'EPSG:4326', geom, precision=6
            )

            # Print GeoJSON shapes to stdout.
            print(geom)
```

Which gives us:

```commandline
{'type': 'Polygon', 'coordinates': [[[3.605665, 44.238903], [3.59992, 
    43.695427], [4.323908, 43.689027], [4.336583, 44.23244], [3.605665, 
    44.238903]]]}
{'type': 'Polygon', 'coordinates': [[[3.608484, 43.752071], [3.603541, 
    43.283354], [4.321619, 43.276958], [4.332442, 43.74562], [3.608484, 
    43.752071]]]}
{'type': 'Polygon', 'coordinates': [[[4.931147, 43.761708], [4.912681, 
    43.209428], [5.64274, 43.194017], [5.668244, 43.746143], [4.931147, 
    43.761708]]]}
{'type': 'Polygon', 'coordinates': [[[4.26721, 44.244389], [4.255021, 
    43.693245], [4.984805, 43.682379], [5.004077, 44.233414], [4.26721, 
    44.244389]]]}
```

!!! Note

    As you have noticed, RasterIO transforms the input URLs, there is no need 
    to append the */vsicurl/* prefix.