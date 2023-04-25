# Advanced use

## Signed URLs time to live (TTL) margin

Every signed URL has a TTL, returned by the signing URL API (`expiry`).
To prevent the expiry of one signed URL during a long process, a margin of 
1800 seconds (30 minutes) is used by default. This duration can be changed 
setting the environment variable `DINAMIS_SDK_TTL_MARGIN` to a number of 
seconds. When one given URL has to be signed again, the cached URL will not be 
used when the previous TTL minus the margin is negative.
30 minutes should be enough for most processing, however feel free to increase 
this value to prevent your long process crashing, if it has started with one 
URL with a short TTL.