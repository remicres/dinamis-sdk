import sys
import dinamis_sdk

headers = dinamis_sdk.get_headers()
print(f'Got headers: {headers}')
assert headers
assert headers.get(sys.argv[1])
