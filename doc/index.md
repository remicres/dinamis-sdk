# Dinamis SDK for python

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

Python library for interacting with the prototype of DINAMIS Spatial Data
Infrastructure APIs.
The SDK and underlying APIs are part of a demonstrator for the next-gen 
platform which should be ready in 2024.

## Installation

```commandline
pip install dinamis-sdk
```

## Quickstart

This library assists with signing STAC items assets URLs from the DINAMIS SDI
prototype. The `sign` function operates directly on an HREF string, as well as 
several [PySTAC](https://github.com/stac-utils/pystac) objects: `Asset`, 
`Item`, and `ItemCollection`. In addition, the `sign` function accepts a 
[STAC API Client](https://pystac-client.readthedocs.io/en/stable/) 
`ItemSearch`, which performs a search and returns the resulting 
`ItemCollection` with all assets signed.

```python
import dinamis_sdk
import pystac_client

api = pystac_client.Client.open(
   'https://stacapi-dinamis.apps.okd.crocc.meso.umontpellier.fr',
   modifier=dinamis_sdk.sign_inplace,
)
```

Follow the instructions to authenticate.
Read the [credentials section](credentials) to know more about credential
expiry.

## Contribute

You can open issues or merge requests at 
[INRAE's gitlab](https://gitlab.irstea.fr/dinamis/dinamis-sdk).

## Terms of service 

Please read carefully the 
[terms of service](https://ids-dinamis.data-terra.org/web/guest/37) related to 
the involved products.

!!! Info

    For legal reasons, only France mainland Spot-6/7 Ortho (Direct Receiving 
    Station) are available.

## Contact

Rémi Cresson at INRAE dot fr
