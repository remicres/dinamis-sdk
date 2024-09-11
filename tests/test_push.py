import dinamis_sdk
import time

local_filename = "/tmp/toto.txt"

with open(local_filename, "w") as f:
    f.write("hello world")

pushed = dinamis_sdk.push(
    local_filename=local_filename,
    target_url="https://s3-data.meso.umontpellier.fr/sm1-gdc-tests/titi.txt"
)
print("Done")
