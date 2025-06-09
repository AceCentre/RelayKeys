import functools
import json

import requests


class RelayKeysClient:
    def __init__(self, url=None, host=None, port=None, username=None, password=None):
        if url is None and host is None and port is None:
            # Default to localhost
            self.url = "http://127.0.0.1:5383/"
        elif url is None:
            if host is None or port is None:
                raise ValueError("url and host:port is not defined!")
            auth = f"{username}:{password}@" if username is not None else ""
            self.url = f"http://{auth}{host}:{port}/"
        else:
            self.url = url

        self.id = 1  # RPC ID counter

    def call(self, name, *args):
        payload = {
            "method": name,
            "params": [list(args)],  # Wrap args in a list as daemon expects single args parameter
            "jsonrpc": "2.0",
            "id": self.id,
        }
        self.id += 1  # Increment ID for next call

        headers = {"content-type": "application/json"}
        data = json.dumps(payload)
        resp = requests.post(self.url, data=data, headers=headers, timeout=10.00)

        # Check for HTTP errors
        if resp.status_code != 200:
            raise Exception(f"HTTP {resp.status_code}: {resp.text}")

        response = resp.json()

        # Check for JSON-RPC errors
        if "error" in response:
            raise Exception(f"RPC Error: {response['error']}")

        # Return just the result
        return response.get("result")

    def __getattr__(self, attr):
        # Don't intercept special attributes
        if attr.startswith('_') or attr in ['id', 'url']:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{attr}'")
        return functools.partial(self.call, attr)
