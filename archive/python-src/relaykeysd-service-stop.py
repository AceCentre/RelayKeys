import json

import requests

payload = {
    "method": "exit",
    "params": [[]],
    "jsonrpc": "2.0",
    "id": 0,
}
headers = {"content-type": "application/json"}
data = json.dumps(payload)
try:
    resp = requests.post("http://127.0.0.1:5383/", data, headers=headers, timeout=10)
except requests.exceptions.ConnectionError:
    print("Connection closed")
