# Collections

The following collections are currently available in the catalog:
- `spot-6-7-drs`: Spot-6/7 images
- `super-sentinel-2-l2a`: Sentinel-2 images enhanced to 1.5m


## Spot-6/7 

| Location         | Dates             |
|------------------|-------------------|
| France mainland  | From 2017 to 2022 |

Please read carefully the 
[terms of service](https://ids-dinamis.data-terra.org/web/guest/37) related to 
the involved products.

!!! Info

    For legal reasons, only France mainland Spot-6/7 Ortho (Direct Receiving 
    Station) are available.

## "Super" Sentinel-2 L2A 

| Location                          | Dates             |
|-----------------------------------|-------------------|
| Selected sites (see figure below) | From 2017 to 2022 |


This product consists in synthetic spectral bands (B2, B3, B4 and B8) enhanced 
at 1.5m using A.I. with available Spot-6/7 imagery.

| Site              | Bounding box                                   |
|-------------------|------------------------------------------------|
| Vienne-le-château | `[4.886140, 49.171417, 4.995230, 49.238478]`   |
| Montpellier       | `[3.696201, 43.547450, 4.036414, 43.754317]`   |
| Dune du pilat     | `[-1.286111, 44.498021, -1.124742, 44.629694]` |
| Lac de la gimone  | `[0.602124, 43.293268, 0.728970, 43.385851]`   |
| Lévignacq         | `[-1.259343, 43.941352, -1.088786, 44.065011]` |

<div align="center">
<img src="https://gitlab.irstea.fr/dinamis/dinamis-sdk/uploads/b1ec1a00ead8b5f7d76a92c159a489f6/super_s2_roi.jpg">
<p>Figure: super-sentinel-2 is currently produced on 4 small ROIs</p>
</div>