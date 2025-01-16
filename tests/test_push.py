#!/usr/bin/env python

import requests

import dinamis_sdk

LOCAL_FILENAME = "/tmp/toto.txt"

with open(LOCAL_FILENAME, "w") as f:
    f.write("hello world")

TARGET_URL = "https://s3-data.meso.umontpellier.fr/sm1-gdc-tests/titi.txt"

dinamis_sdk.push(local_filename=LOCAL_FILENAME, target_url=TARGET_URL)
print("push OK")

signed_url = dinamis_sdk.sign(TARGET_URL)
print("sign OK")

res = requests.get(signed_url, stream=True, timeout=10)
assert res.status_code == 200, "Get NOK"
print("get OK")


print("Done")
