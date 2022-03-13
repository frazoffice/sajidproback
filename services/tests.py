# from square.client import Client
# from cachecontrol import CacheControl
# from deprecation import deprecated
# client = Client(
#     square_version='2022-02-16',)
#
# locations_api = client.locations
# result = locations_api.list_locations()
#
# if result.is_success():
#     print(result.body)
# elif result.is_error():
#     print(result.errors)
#
#




import requests

headers = {
    'Content-type': 'application/json',
    'Authorization': 'Bearer EAAAEIH7NTX39rv-7k7Q_B1kHxTlCudg9qgjz_DLgpfWjYVjsQ-wH2VNIiTpVnbf',
    'Square-Version': '2019-08-14'

}

data = """{
    "idempotency_key": "57d92322-d11e-48d6-be84-12072829db14",
    "amount_money": {
      "amount": 2000,
      "currency": "USD"
    },
    "source_id": "cnon:card-nonce-ok"

}"""
print(type(data))
response = requests.post('https://connect.squareupsandbox.com/v2/payments', headers=headers, data=data)


print(response.json())