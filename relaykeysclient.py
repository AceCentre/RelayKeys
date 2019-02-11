import requests
import json
import functools

class RelayKeysClient (object):
  def __init__ (self, url=None, host=None, port=None,
                username=None, password=None):
    if (host is None or port is None) and url is None:
      raise ValueError("url and host:port is not defined!")
    if url is None:
      auth = "{}:{}@".format(username, password) if username is not None else ""
      self.url = "http://{}{}:{}/".format(auth, host, port)
    else:
      self.url = url

  def call (self, name, *args):
    payload = {
        "method": name,
        "params": [args],
        "jsonrpc": "2.0",
        "id": 0,
    }
    headers = {'content-type': 'application/json'}
    return requests.post(self.url, data=json.dumps(payload),
                         headers=headers).json()

  def __getattr__ (self, attr):
    return functools.partial(self.call, attr)
