from pathlib import Path
from time import sleep, time

from notifypy import Notify

from ..core.client import RelayKeysClient

client = RelayKeysClient(url="http://127.0.0.1:5383/")


def send_devname_notification(device_name):
    notification = Notify()
    notification.application_name = "Relaykeys"
    notification.title = ""
    notification.icon = str(Path(__file__).resolve().parent / "resources" / "logo.png")
    notification.message = f"Connected to {device_name}."

    notification.send()


polling_start_timestamp = time()
timeout_sec = 40

while True:
    if time() - polling_start_timestamp > timeout_sec:
        break  # timeout

    ret = client.ble_cmd("devname")
    if "result" in ret:
        devname = ret["result"]
        if devname != "NONE":
            send_devname_notification(devname)
            break

    sleep(2)
