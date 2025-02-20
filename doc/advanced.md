# Advanced use

## Environment variables

- `DINAMIS_SDK_TTL_MARGIN`: 
Every signed URL has a TTL, returned by the signing URL API (`expiry`).
To prevent the expiry of one signed URL during a long process, a margin of 
1800 seconds (30 minutes) is used by default. This duration can be changed 
setting this environment variable to a number of seconds. When one given 
URL has to be signed again, the cached URL will not be used when the 
previous TTL minus the margin is negative. 30 minutes should be enough 
for most processing, however feel free to increase this value to prevent 
your long process crashing, if it has started with one URL with a short TTL.

- `DINAMIS_SDK_URL_DURATION`: 
Signed URLs have a default duration set by the signing API endpoint (in 
general, a few hours). You can change the duration up to 6 days setting 
this environment variable, in seconds.

- `DINAMIS_SDK_BYPASS_AUTH_API`: 
Use this environment variable to use a different signing API endpoint, 
with no authentication mechanism.

- `DINAMIS_SDK_CONFIG_DIR`: 
The default config directory used to store authentication credentials (i.e. 
jwt tokens and API key) is located in the user config folder (In linux: 
`/home/user/.config/dinamis_sdk_auth`). Set this environment variable to 
set a different directory.

- `DINAMIS_SDK_ACCESS_KEY` and `DINAMIS_SDK_SECRET_KEY` can be used to 
set your API key from the environment.

- `DINAMIS_SDK_RETRY_TOTAL` and `DINAMIS_SDK_RETRY_BACKOFF` can be set to 
control the retry strategy of requests to the signing API endpoint.

## Get headers

For the developer it can be convenient just to grab headers (whatever the 
authentication method is) to use them is various API endpoints.

```python
import dinamis_sdk

headers = dinamis_sdk.get_headers()
```
