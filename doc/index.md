# Dinamis SDK for python

<div align="center">
<div id="qr" style="display:inline-block; margin: auto; align: center; vertical-align: middle; height:3cm;" >
<img src="https://upload.wikimedia.org/wikipedia/fr/thumb/2/2a/Logo-INRAE_Transparent.svg/2560px-Logo-INRAE_Transparent.svg.png" style="height:1cm; padding:5px">
<img src="https://upload.wikimedia.org/wikipedia/commons/7/7f/Logo_IRD_2016_BLOC_FR_COUL.png" style="height:1cm; padding:5px">
<img src="https://theia.sedoo.fr/wp-content-theia/uploads/sites/6/2020/05/Logo_DINAMIS_300px.png" style="height:1cm; padding: 5px">
</div>
<br>
<a href="https://forgemia.inra.fr/cdos-pub/dinamis-sdk/-/releases">
<img src="https://forgemia.inra.fr/cdos-pub/dinamis-sdk/-/badges/release.svg">
</a>
<a href="https://forgemia.inra.fr/cdos-pub/dinamis-sdk/-/commits/main">
<img src="https://forgemia.inra.fr/cdos-pub/dinamis-sdk/badges/main/pipeline.svg">
</a>
<a href="LICENSE">
<img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg">
</a>
</div>

Python library for interacting with the prototype of DINAMIS Spatial Data
Infrastructure APIs.
The SDK and underlying APIs are part of a demonstrator for the next-gen 
platform which should be ready in 2024.

## Installation

```commandline
pip install dinamis-sdk
```

## Quickstart

This library assists with signing STAC items assets URLs from the [THEIA-MTP 
geospatial data center](https://home-cdos.apps.okd.crocc.meso.umontpellier.fr/).
The `sign_inplace` function operates directly on an HREF string, as well as 
several [PySTAC](https://github.com/stac-utils/pystac) objects: `Asset`, `Item`, and `ItemCollection`. 
In addition, the `sign_inplace` function accepts a [STAC API Client](https://pystac-client.readthedocs.io/en/stable/) 
`ItemSearch`, which performs a search and returns the resulting 
`ItemCollection` with all assets signed.
`sign_inplace()` can be used as a `modifier` in `pystac_client.Client` 
instances, as shown in the example below. Alternatively, `sign()` can be used 
to sign a single url.

```python
import dinamis_sdk
import pystac_client

api = pystac_client.Client.open(
   'https://stacapi-cdos.apps.okd.crocc.meso.umontpellier.fr',
   modifier=dinamis_sdk.sign_inplace,
)
```

Follow the instructions to authenticate.
Read the [credentials section](credentials) to know more about credentials.

## Contribute

You can open issues or merge requests at 
[INRAE's gitlab](https://forgemia.inra.fr/cdos-pub/dinamis-sdk).

## Contact

Rémi Cresson at INRAE dot fr
