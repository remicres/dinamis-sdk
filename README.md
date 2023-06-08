# DINAMIS SDK

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

Largely inspired from *Microsoft Planetary Computer SDK*, **Dinamis-SDK** is 
built on the STAC ecosystem and provides easy access to open-data Spot-6/7 
imagery in COG format.

```python
import dinamis_sdk
import pystac_client

api = pystac_client.Client.open(
   'https://stacapi-dinamis.apps.okd.crocc.meso.umontpellier.fr',
   modifier=dinamis_sdk.sign_inplace,
)
```

For more information read the 
[documentation](https://dinamis.gitlab.irstea.page/dinamis-sdk).
