# Credentials

There is two ways of authenticating to the THEIA-MTP Geospatial data 
infrastructure:

- OAuth2
- API key

## OAuth2

The credentials are retrieved using the device code flow on the first call of 
`dinamis_sdk.sign_inplace()`. Just follow the instructions, i.e. click on the 
HTTP link, or scan the QR-code.

The credentials are valid for 5 days. Every time `dinamis_sdk.sign_inplace()` 
is called, the credentials are renewed for another 5 days. After 5 days idle, 
you will have to log in again.

## API key

Use `dinamis_cli` to register an API key, that will be created and stored into 
your local home directory.

```commandline
dinamis_cli register
```

Just follow the instructions to login a single time, then the API key can be 
used forever on your local computer. You can duplicate the API key file on 
other computers.

You can delete the API key any time with:

```commandline
dinamis_cli delete
```

## Signed URLs expiry

The signed URLs for STAC objects assets are valid during 7 days starting after 
`dinamis_sdk.sign_inplace` is called. 

!!! Info

    `dinamis_sdk.sign_inplace()` can also be applied directly on a particular 
    `pystac.item`, `pystac.collection`, `pystac.asset` or any URL as `str`, 
    with the same outcome in term of expiry.

!!! Warning

    Do no confuse credentials validity with images URL token validity.
    Both have different lifecycle. To read how to ask for longer 
    URLs time-to-live, please read the API reference of 
    `dinamis_sdk.sign_inplace()`.
