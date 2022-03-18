nrfVID = '239A'
nrfPID = '8029'


import serial.tools.list_ports
ports = list(serial.tools.list_ports.comports())
for p in serial.tools.list_ports.comports():
    if (
        ("CP2104" in p.description)
        or "nRF52" in p.description
        or nrfVID
        and nrfPID in p.hwid
    ):
        dev = p.device
        break
print(dev)