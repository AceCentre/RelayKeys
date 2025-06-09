import asyncio
import time


class BLESerialWrapper:
    UART_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
    UART_RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
    UART_TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

    def __init__(self, ble_client):
        self.ble_client = ble_client
        self.receive_buff = b""
        self.timeout_val = 3

    async def init_receive(self):
        await self.ble_client.start_notify(
            BLESerialWrapper.UART_TX_CHAR_UUID, self.receive_data
        )

    def __enter__(self):
        return self

    def __exit__(self, a, b, c):
        pass

    def flushInput(self):
        self.receive_buff = b""

    def flushOutput(self):
        pass

    async def write(self, data):
        await self.ble_client.write_gatt_char(BLESerialWrapper.UART_RX_CHAR_UUID, data)

    def receive_data(self, _: int, data: bytearray):
        self.receive_buff += data

    def read_all(self):
        ret_buffer = self.receive_buff
        self.receive_buff = b""
        return ret_buffer

    async def readline(self):
        start = 0
        end = 0
        start_time = time.time()
        # print("start readline")
        while True:
            if end != len(self.receive_buff):
                if self.receive_buff[end] == 10:
                    line = self.receive_buff[start : end + 1]
                    self.receive_buff = self.receive_buff[end + 1 : :]
                    return line

                # print("iterate")
                end += 1
            else:
                # print("reached end, waiting")
                await asyncio.sleep(0.05)
                # timeout check
                if (time.time() - start_time) > self.timeout_val:
                    return b""


class DummySerial:
    def __init__(self, devpath, baud, **kwargs):
        self.devpath = devpath
        self.baud = baud
        self.command_responses = {
            b"AT\r\n": b"OK\n",
            b"ATE=0\r\n": b"OK\n",
            b"AT+BLEHIDEN=1\r\n": b"OK\n",
            b"ATZ\r\n": b"OK\n",
            b"AT+PRINTDEVLIST\r\n": b"Dummy Device 1\nDummy Device 2\nDummy Device 3\nOK\n",
            b"AT+BLECURRENTDEVICENAME\r\n": b"DummyDevice\nOK\n",
            b"AT+BLEHIDKEYBOARD=": b"OK\n",
            b"AT+BLEHIDMOUSEMOVE=": b"OK\n",
            b"AT+BLEHIDMOUSEBUTTON=": b"OK\n",
        }
        print(f"DummySerial initialized on {devpath} at {baud} baud")

    def __enter__(self):
        return self

    def __exit__(self, a, b, c):
        pass

    def write(self, data):
        print(f"TX: {data}")
        # Simulate some processing time
        import time

        time.sleep(0.01)

    def flushInput(self):
        pass

    def flushOutput(self):
        pass

    def readline(self):
        # Return appropriate response based on last command
        return b"OK\n"

    def read_all(self):
        return b"Dummy Device 1\nDummy Device 2\nDummy Device 3\n"


def get_serial(device_path, baud_rate, use_dummy=False):
    """Get a serial connection, either real or dummy"""
    if use_dummy:
        return DummySerial(device_path, baud_rate)
    else:
        import serial
        return serial.Serial(device_path, baud_rate, timeout=1)
