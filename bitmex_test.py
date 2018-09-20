import requests
import base64
import uuid
import APIKeyAuthWithExpires

clOrdID = base64.b64encode(uuid.uuid4().bytes).decode('utf8').rstrip('=\n')
postdict = {
    'symbol': "XBTUSD",
    'orderQty': "800",
    'price': "1365",
    'clOrdID': clOrdID
}
session = requests.Session()
auth = APIKeyAuthWithExpires.APIKeyAuthWithExpires("34DRwq1MqqWm8--POSUhEl9A", "txfKD1Je6GJqJyOqEr7UnJC8ebPURzFzUNuZsJz2Pp-V8hau")
req = requests.Request("POST", "http://testnet.bitmex.com/api/v1/order", json=postdict, auth=auth, params=None)
prepped = session.prepare_request(req)
response = session.send(prepped)
# Make non-200s throw
response.raise_for_status()
print(response)