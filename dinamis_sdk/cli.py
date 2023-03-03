import json
import os
from getpass import getpass

from .utils import settings_file, StorageCredentials

print("Visit \033[92mhttps://minio-dinamis.apps.okd.crocc.meso.umontpellier.fr/access-keys\033[0m"
      " to create or delete your credentials.")
credentials = StorageCredentials(
    access_key=getpass("\033[92mAccess key\033[0m: "),
    secret_key=getpass("\033[92mSecret key\033[0m: ")
)
with open(settings_file, 'w', encoding='UTF-8') as file:
    json.dump(credentials.dict(), file)
