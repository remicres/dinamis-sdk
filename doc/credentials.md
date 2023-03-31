# Credentials

## Login

The credentials are then valid for 5 days. Every time 
`dinamis_sdk.sign_inplace` is called, the credentials are renewed for another 
5 days. After 5 days idle, you will have to log in again.

## Signed URLs

The signed URLs for STAC objects assets are valid during 7 days starting after 
`dinamis_sdk.sign_inplace` is called. 

!!! Info

    `dinamis_sdk.sign_inplace` can also be applied directly on a particular 
    `pystac.item`, `pystac.collection`, `pystac.asset` or any URL as `str`, 
    with the same outcome in term of expiry.
