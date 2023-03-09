import serial.tools.list_ports
ports = list(serial.tools.list_ports.comports())

for p in serial.tools.list_ports.comports():
    print("name:", p.name, "desc:", p.description, "hwid:", p.hwid, "vid:", p.vid, "pid:", p.pid, "ser:", p.serial_number,"\r")


nrfVID = '239A'
nrfPIDs = ['8029', '8051']

for p in serial.tools.list_ports.comports():
    if ("CP2104" in p.description):
        print('Found CP2104')
    elif ("nRF52" in p.description):
        print('Found nrf52')
    elif (p.vid == nrfVID and p.pid.upper() in nrfPIDs):
        print('Found device with VID:', nrfVID, 'and PID:', p.pid)
    elif (nrfVID in p.hwid.upper()):
        print('Found nrfVID in hwid')
    
input("Press enter to continue...")
