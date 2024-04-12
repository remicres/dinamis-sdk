# DINAMIS SDK

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

Largely inspired from *Microsoft Planetary Computer SDK*, **Dinamis-SDK** is 
built on the STAC ecosystem to provide an easy access to remote sensing imagery
and thematic products of the **THEIA/DINAMIS data center of Montpellier**.

```python
import dinamis_sdk
import pystac_client

api = pystac_client.Client.open(
   'https://stacapi-cdos.apps.okd.crocc.meso.umontpellier.fr',
   modifier=dinamis_sdk.sign_inplace,
)
```

For more information read the 
[documentation](https://cdos-pub.pages.mia.inra.fr/dinamis-sdk).
