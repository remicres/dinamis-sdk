# Examples

## Processing COGs locally

The following demonstrates how to process remote COGs locally with your 
favorite tool.

### GDAL, OTB, PyOTB

Here the excellent [pyotb](https://pyotb.readthedocs.io/) is used, but the 
approach is similar with GDAL, OTB, GRASS, SAGA, etc.

To process remote COG files, we use the *vsicurl* driver.

!!! Warning

    The following software must be up-to-date:

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

### Rasterio

```python
import pyotb

res = api.search(
    bbox=[4, 42.99, 5, 44.05],
    datetime=['2020-01-01', '2022-01-02']
)

vsi_urls = [f"/vsicurl/{r.assets['src_xs'].href}" for r in res.items()]
pyotb.Mosaic({"il": vsi_urls, "out": "raster.tif"})
```
