import asyncio
import time

class BLESerialWrapper(object):
    UART_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
    UART_RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
    UART_TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

    def __init__(self, ble_client):
        self.ble_client = ble_client
        self.receive_buff = b''
    
    async def init_receive(self):   
        await self.ble_client.start_notify(BLESerialWrapper.UART_TX_CHAR_UUID, self.receive_data)

    def __enter__(self):
        return self

    def __exit__(self, a, b, c):
        pass

    def flushInput(self):
        self.receive_buff = b''
    
    def flushOutput(self):
        pass

    async def write(self, data):
        await self.ble_client.write_gatt_char(BLESerialWrapper.UART_RX_CHAR_UUID, data)

    def receive_data(self, _: int, data: bytearray):
        self.receive_buff += data
    
    def read_all(self):
        ret_buffer = self.receive_buff
        self.receive_buff = b''
        return ret_buffer

    async def readline(self):
        start = 0
        end = 0
        #print("start readline")
        while True:
            if(end != len(self.receive_buff)):        
                if self.receive_buff[end] == 10:                    
                    line = self.receive_buff[start:end+1]
                    self.receive_buff = self.receive_buff[end+1::]
                    return line
                
                #print("iterate")
                end+=1
            else:
                #print("reached end, waiting")
                await asyncio.sleep(0.05)

class DummySerial (object):
    def __init__(self, devpath, baud, **kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, a, b, c):
        pass

    def write(self, data):
        print(f"{data}")

    def flushInput(self):
        pass

    def readline(self):
        return b"OK\n"
