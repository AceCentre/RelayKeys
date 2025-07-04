#
# The control daemon for handling BLE HID
# communication with http-JSON-RPC
#


# To debug - without the correct hardware attached:
#   Run demoSerial.py
#   Call this code with relayKeys.py --noserial

import array as arr
import os
import sys
from hashlib import sha256
from math import floor
from os import urandom
from queue import Empty as QueueEmpty
from queue import Queue
from sys import exit
from threading import Thread
from time import sleep
from typing import List

import serial
import serial.tools.list_ports

if os.name == "posix":  # unix based OS
    from daemon import DaemonContext
    from lockfile.pidlockfile import PIDLockFile

# util modules
import argparse

# ble mode dependencies
import asyncio
import logging
import traceback
from configparser import ConfigParser

from bleak import BleakClient, BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from bleak.exc import BleakError
from jsonrpc import Dispatcher, JSONRPCResponseManager
from jsonrpc.jsonrpc2 import JSONRPC20Response
from werkzeug.serving import WSGIRequestHandler as BaseRequestHandler
from werkzeug.serving import make_server

# rpc modules
from werkzeug.wrappers import Request, Response

from .serial_wrappers import BLESerialWrapper, DummySerial

UART_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
UART_RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
UART_TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

import json

import requests

from .blehid import (
    blehid_get_at_response,
    blehid_get_device_list,
    blehid_get_mode,
    blehid_init_serial,
    blehid_send_add_device,
    blehid_send_clear_device_list,
    blehid_send_get_device_name,
    blehid_send_keyboardcode,
    blehid_send_mousebutton,
    blehid_send_movemouse,
    blehid_send_remove_device,
    blehid_send_switch_command,
    blehid_switch_mode,
)

# from pygame.locals import *
# from pygame.compat import as_bytes
# BytesIO = pygame.compat.get_BytesIO()

# Use AT+BAUDRATE=115200 but make sure hardware flow control CTS/RTS works
DEFAULT_BAUD = 115200
# BAUD = 9600
nrfVID = "239A"
nrfPIDs = ["8029", "810B", "8051"]
devName = "NONE"
devList: List[str] = []
RETRY_TIMEOUT = 10
QUEUE_TIMEOUT = 3

ble_mode = False
daemon_quit = False
serial_loop_opened = False

parser = argparse.ArgumentParser(description="Relay keys daemon, BLEHID controller.")
parser.add_argument(
    "--noserial",
    dest="noserial",
    action="store_const",
    const=True,
    default=False,
    help="debug option to run the daemon with no hardware (with help of demoSerial.py",
)
parser.add_argument(
    "--dev", dest="dev", default=None, help="device to use as bluetooth serial"
)
parser.add_argument(
    "--baud",
    dest="baud",
    default=None,
    help=f"specify serial baud, default: {DEFAULT_BAUD}",
)
parser.add_argument(
    "--debug",
    dest="debug",
    action="store_const",
    const=True,
    default=False,
    help="set logger to debug level",
)
parser.add_argument(
    "--ble_mode",
    dest="ble_mode",
    action="store_const",
    const=True,
    default=False,
    help="choosing work in ble mode",
)
parser.add_argument(
    "--daemon",
    "-d",
    dest="daemon",
    action="store_const",
    const=True,
    default=False,
    help="Run as daemon, posfix specific",
)
parser.add_argument(
    "--pidfile",
    dest="pidfile",
    default=None,
    help="file to hold pid of daemon, posfix specific",
)
parser.add_argument(
    "--logfile", dest="logfile", default=None, help="file to log messages too"
)
parser.add_argument(
    "--config", "-c", dest="config", default=None, help="Path to config file"
)


class CommandException(BaseException):
    pass


class RPCServExitException(BaseException):
    pass


class AppExitException(BaseException):
    pass


class RequestHandler(BaseRequestHandler):
    def log(self, type, message, *args):
        # treat `info` logs as `debug
        lvl = logging.DEBUG
        if type == "error":
            lvl = logging.ERROR
        logging.log(
            lvl,
            f"{self.address_string()} - - [{self.log_date_time_string()}] {message % args}\n",
        )


def rpc_server_worker(host, port, username, password, queue):
    dispatcher = Dispatcher()
    srv = None
    # prehash password
    password = int(sha256(bytes(password, "utf8")).hexdigest(), 16)

    @dispatcher.add_method
    def actions(args):
        global serial_loop_opened
        if not serial_loop_opened:
            return "No connection with dongle"

        try:
            global devName
            global devList

            actionlist = args[0]

            for action in actionlist:

                if action[0] not in ("mousemove", "mousebutton", "keyevent", "ble_cmd"):

                    raise ValueError("unknown action")

            respqueue = Queue(1)
            queue.put((respqueue, "actions", actionlist), True)
            try:
                return respqueue.get(True, 5)
            except QueueEmpty:
                return "TIMEOUT"

        except:
            return "UNEXPECTED_INPUT"

    @dispatcher.add_method
    def mousebutton(args):
        global serial_loop_opened
        if not serial_loop_opened:
            return "No connection with dongle"

        respqueue = Queue(1)
        queue.put((respqueue, "mousebutton") + tuple(args), True)
        try:
            return respqueue.get(True, 5)
        except QueueEmpty:
            return "TIMEOUT"

    @dispatcher.add_method
    def mousemove(args):
        global serial_loop_opened
        if not serial_loop_opened:
            return "No connection with dongle"

        respqueue = Queue(1)
        queue.put((respqueue, "mousemove") + tuple(args), True)
        try:
            return respqueue.get(True, 5)
        except QueueEmpty:
            return "TIMEOUT"

    @dispatcher.add_method
    def keyevent(args):
        global serial_loop_opened
        if not serial_loop_opened:
            return "No connection with dongle"

        key, modifiers, down = args
        respqueue = Queue(1)
        queue.put((respqueue, "keyevent", key, modifiers or [], down), True)
        try:
            return respqueue.get(True, 5)
        except QueueEmpty:
            return "TIMEOUT"

    @dispatcher.add_method
    def ble_cmd(args):
        global serial_loop_opened
        if not serial_loop_opened:
            return "No connection with dongle"

        devcommand = args[0]
        respqueue = Queue(1)
        queue.put((respqueue, "ble_cmd", devcommand), True)
        try:
            return respqueue.get(True, 5)
        except QueueEmpty:
            return "TIMEOUT"

    @dispatcher.add_method
    def daemon(args):
        global ble_mode, serial_loop_opened

        command = args[0]
        if command == "get_mode":
            if ble_mode:
                return "BLE serial"
            else:
                return "Hardware serial"
        elif command == "switch_mode":
            ble_mode = not ble_mode
            if serial_loop_opened:
                queue.put((None, "break_loop"), True)

            return "OK"
        elif command == "dongle_status":
            if serial_loop_opened:
                respqueue = Queue(1)
                queue.put((respqueue, "check_dongle"), True)
                try:
                    response = respqueue.get(True, 5)
                    if response == "OK":
                        return "Connected"
                except QueueEmpty:
                    pass

            return "No connection"

    @dispatcher.add_method
    def exit(args):
        respqueue = Queue(1)
        queue.put((respqueue, "exit"), True)
        try:
            respqueue.get(True, 5)
        except:
            pass
        raise RPCServExitException()

    @Request.application
    def app(request):
        # auth with simplified version of equal op (timing attack secure)
        if (username != "" or password != "") and (
            getattr(request.authorization, "username", "") != username
            or int(
                sha256(
                    bytes(getattr(request.authorization, "password", ""), "utf8")
                ).hexdigest(),
                16,
            )
            - password
            != 0
        ):
            json = JSONRPC20Response(
                error={"code": 403, "message": "Invalid username or password!"}
            ).json
            return Response(json, 403, mimetype="application/json")
        response = JSONRPCResponseManager.handle(request.data, dispatcher)
        return Response(response.json, mimetype="application/json")

    try:
        # response queue is used to notify result of attempt to run the server
        respqueue = queue.get()
        srv = make_server(host, port, app, request_handler=RequestHandler)
        logging.info(f"http-jsonrpc listening at {host}:{port}")
        queue.task_done()  # let run_rpc_server return
        respqueue.put("SUCCESS")
        srv.serve_forever()
    except RPCServExitException:
        logging.info("Exit exception raised!")
    except:
        queue.task_done()
        respqueue.put("FAIL")
        logging.error(traceback.format_exc())


# run rpc server on another thread


def run_rpc_server(host, port, username, password):
    queue = Queue(10)
    respqueue = Queue(1)
    queue.put(respqueue)
    t = Thread(target=rpc_server_worker, args=(host, port, username, password, queue))
    t.daemon = True
    t.start()
    if respqueue.get(True) == "FAIL":
        return None
    return queue


def shutdown_server():
    payload = {
        "method": "exit",
        "params": [[]],
        "jsonrpc": "2.0",
        "id": 0,
    }
    headers = {"content-type": "application/json"}
    data = json.dumps(payload)
    try:
        requests.post("http://127.0.0.1:5383/", data, headers=headers, timeout=10)
    except requests.exceptions.ConnectionError:
        print("Connection closed")


def find_device_path(noserial, seldev):
    dev = None
    if noserial:
        if os.name == "posix":
            serialdemofile = os.path.join(
                os.path.dirname(os.path.realpath(__file__)), ".serialDemo"
            )
            if os.path.isfile(serialdemofile):
                with open(serialdemofile) as f:
                    dev = f.read()
            else:
                logging.critical(
                    "no-serial is set to true.. Please make sure you have already run 'python resources\\demoSerial.py' from a different shell"
                )
                exit(-1)
        elif os.name == "nt":
            dev = "COM7" if seldev is None else seldev
    else:
        if seldev != None:
            logging.debug("port from config: " + seldev)
            for p in serial.tools.list_ports.comports():
                if seldev == p.device:
                    dev = seldev
                    logging.debug("specified port present")
                    break

            if dev == None:
                logging.debug("specified port wasn't found")

        if dev == None:
            logging.debug("Starting automatic search of port")
            for p in serial.tools.list_ports.comports():
                if "CP2104" in p.description:
                    logging.debug("serial desc:" + str(p))
                    dev = p.device
                elif "nRF52" in p.description:
                    logging.debug("serial desc:" + str(p))
                    dev = p.device
                elif p.vid == nrfVID and p.pid.upper() in nrfPIDs:
                    logging.debug("serial desc:" + str(p))
                    dev = p.device
                elif nrfVID in p.hwid.upper():
                    logging.debug("serial desc:" + str(p))
                    dev = p.device

    return dev


def do_main(args, config, interrupt=None):
    global ble_mode, daemon_quit

    # actions queue
    queue = run_rpc_server(
        config.get("host", "127.0.0.1"),
        config.getint("port", 5383),
        config.get("username", ""),
        config.get("password", ""),
    )
    try:  # remove password from memory
        del config["password"]
    except:
        pass
    if queue is None:
        logging.critical("Could not start rpc server")
        return -1  # exit the process

    ble_mode = True if args.ble_mode else False

    while not daemon_quit:
        if not ble_mode:
            asyncio.run(hardware_serial_loop(queue, args, config, interrupt))
        else:
            try:
                asyncio.run(ble_serial_loop(queue, args, config, interrupt))
            except asyncio.CancelledError:
                pass

    logging.info("relaykeysd exit!")
    return 0


async def hardware_serial_loop(queue, args, config, interrupt):
    global daemon_quit, serial_loop_opened

    try:
        if interrupt is not None:
            interrupt()
        baud = args.baud if args.baud is not None else config.get("baud", DEFAULT_BAUD)
        seldev = args.dev if args.dev is not None else config.get("dev", None)
        noserial = True if args.noserial else config.getboolean("noserial", False)
        devicepath = find_device_path(noserial, seldev)
        if devicepath == None:
            raise serial.serialutil.SerialException("No port found")
        if os.name == "nt" and noserial:
            SerialCls = DummySerial
        else:
            SerialCls = serial.Serial
        with SerialCls(devicepath, baud, rtscts=0, timeout=2) as ser:

            logging.info(f"serial device opened: {devicepath}")
            serial_loop_opened = True

            # logging.info("INIT MSG: {}".format(str(ser.readline(), "utf8")))
            await blehid_init_serial(ser)

            keys = arr.array("B", [0, 0, 0, 0, 0, 0, 0, 0])

            # Get intial ble device List
            await process_action(ser, keys, ["ble_cmd", "devlist"])
            # Get intial ble device name
            await process_action(ser, keys, ["ble_cmd", "devname"])

            try:
                while True:
                    if interrupt is not None:
                        interrupt()
                    try:
                        # with timeout
                        cmd = queue.get(True, QUEUE_TIMEOUT)
                        if cmd[1] == "exit":
                            daemon_quit = True
                            break
                        elif cmd[1] == "break_loop":
                            logging.info("Breaking hardware serial loop")
                            break
                        else:
                            output = await process_action(ser, keys, cmd[1:])
                            if cmd[0] is not None:
                                cmd[0].put(output)
                            queue.task_done()
                            if output == "FAIL":
                                break
                    except QueueEmpty:
                        pass
            except (SystemExit, KeyboardInterrupt):
                shutdown_server()
                daemon_quit = True

            serial_loop_opened = False
    except serial.serialutil.SerialException:
        serial_loop_opened = False
        logging.error(traceback.format_exc())
        logging.info(f"Will retry in {RETRY_TIMEOUT} seconds")
        sleep(RETRY_TIMEOUT)


async def ble_serial_loop(queue, args, config, interrupt):
    global daemon_quit, serial_loop_opened

    def match_nus_uuid(device: BLEDevice, adv: AdvertisementData):
        print("services of scanned device: ", adv)

        if adv.local_name == "AceRK":  # UART_SERVICE_UUID.lower() in adv.service_uuids:
            return True
        return False

    def handle_disconnect(_: BleakClient):
        print("Device was disconnected.")
        """
        # cancelling all tasks effectively ends the program        
        
        for task in asyncio.all_tasks():
            task.cancel()   
        """

    if interrupt is not None:
        interrupt()
    device = await BleakScanner.find_device_by_filter(match_nus_uuid)

    if device != None:
        try:
            async with BleakClient(
                device, disconnected_callback=handle_disconnect
            ) as client:
                ser = BLESerialWrapper(client)
                await ser.init_receive()

                keys = arr.array("B", [0, 0, 0, 0, 0, 0, 0, 0])

                print("Device connected.")
                serial_loop_opened = True

                try:
                    while True:
                        if interrupt is not None:
                            interrupt()
                        try:
                            # with timeout
                            cmd = queue.get(True, QUEUE_TIMEOUT)
                            if cmd[1] == "exit":
                                daemon_quit = True
                                break
                            elif cmd[1] == "break_loop":
                                logging.info("Breaking BLE serial loop")
                                return
                            else:
                                output = await process_action(ser, keys, cmd[1:])
                                if cmd[0] is not None:
                                    cmd[0].put(output)
                                queue.task_done()

                                # checking if connection present
                                if not client.is_connected:
                                    print("client lost connection")
                                    raise BleakError
                        except QueueEmpty:
                            pass
                except (SystemExit, KeyboardInterrupt):
                    shutdown_server()
                    daemon_quit = True

                serial_loop_opened = False
        except (
            asyncio.exceptions.TimeoutError,
            asyncio.exceptions.InvalidStateError,
            BleakError,
            OSError,
        ):
            serial_loop_opened = False
            logging.error(traceback.format_exc())
    else:
        logging.error("Device not found")

    if not daemon_quit:
        logging.info(f"Will retry in {RETRY_TIMEOUT} seconds")
        sleep(RETRY_TIMEOUT)


async def process_action(ser, keys, cmd):
    try:
        if cmd[0] == "actions":
            outputs = []
            for action in cmd[1]:
                outputs.append(await process_action(ser, keys, action))
            return ", ".join(outputs)

        if cmd[0] == "keyevent":
            key = cmd[1]
            modifiers = cmd[2]
            down = cmd[3]
            await blehid_send_keyboardcode(ser, key, modifiers, down, keys)

        elif cmd[0] == "mousemove":
            right = int(cmd[1])
            down = int(cmd[2])
            wheely = int(cmd[3] if len(cmd) > 3 else 0)
            wheelx = int(cmd[4] if len(cmd) > 4 else 0)
            await blehid_send_movemouse(ser, right, down, wheely, wheelx)

        elif cmd[0] == "mousebutton":
            btn = str(cmd[1]).lower() if cmd[1] is not None else None
            behavior = (
                str(cmd[2]).lower() if len(cmd) > 2 and cmd[2] is not None else None
            )
            if len(btn) > 1 or btn not in "lrmbf0":
                raise CommandException(f"Unknown mousebutton: {btn}")
            if behavior is not None and behavior not in (
                "press",
                "click",
                "doubleclick",
                "hold",
            ):
                raise CommandException(f"Unknown mousebutton behavior: {behavior}")
            await blehid_send_mousebutton(ser, btn, behavior)

        elif cmd[0] == "ble_cmd":

            if cmd[1] == "switch" or cmd[1].startswith("switch="):
                await blehid_send_switch_command(ser, cmd[1])

            elif cmd[1] == "devname":
                return await blehid_send_get_device_name(ser, cmd[1])

            elif cmd[1] == "devlist":
                return await blehid_get_device_list(ser, cmd[1])

            elif cmd[1] == "devadd":
                await blehid_send_add_device(ser, cmd[1])

            elif cmd[1] == "devreset":
                await blehid_send_clear_device_list(ser, cmd[1])

            elif cmd[1].split("=")[0] == "devremove":
                await blehid_send_remove_device(ser, cmd[1])

            elif cmd[1] == "get_mode":
                return await blehid_get_mode(ser)

            elif cmd[1] == "switch_mode":
                await blehid_switch_mode(ser)

            elif cmd[1] == "keyboard_release":
                print("keyboard relase")
                for i in range(0, 8):
                    keys[i] = 0
                await blehid_send_keyboardcode(ser, None, [], False, keys)

        elif cmd[0] == "check_dongle":
            return await blehid_get_at_response(ser)

        # response queue given by cmd
        return "SUCCESS"
    except:
        logging.error(traceback.format_exc())
        return "FAIL"
    if cmd[0] == "exit":
        raise AppExitException()


def init_logger(dirname, isdaemon, args, config):
    # init logger
    loggerformatter = logging.Formatter("%(asctime)-15s: %(message)s")
    logger = logging.getLogger()
    # logging stdout handler
    if not isdaemon:
        handler = logging.StreamHandler()
        handler.setFormatter(loggerformatter)
        logger.addHandler(handler)
    # logging file handler
    if args.logfile is None:
        logfile = config.get("logfile", None)
        if logfile is not None and os.path.abspath(logfile) != logfile:
            logfile = os.path.join(dirname, logfile)
    else:
        logfile = args.logfile
    if logfile is not None:
        handler = logging.FileHandler(logfile)
        handler.setFormatter(loggerformatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    if args.debug or config.getboolean("debug", False):
        logger.setLevel(logging.DEBUG)
    if logfile is None and isdaemon:  # disable logger
        logging.disable(sys.maxsize)


def mkpasswd(n, chars):
    ret = ""
    charsn = len(chars)
    while n > 0:
        index = int(
            floor(
                (
                    int.from_bytes(urandom(4), byteorder="little", signed=False)
                    / 2 ** (8 * 4)
                )
                * charsn
            )
        )
        ret += chars[index]
        n -= 1
    return ret


def main(interrupt=None):
    args = parser.parse_args()
    config = ConfigParser()
    dirname = os.path.dirname(os.path.realpath(sys.argv[0]))
    if args.config is None:
        configfile = None
        for afile in [
            os.path.expanduser("~/.relaykeys.cfg"),
            os.path.join(dirname, "relaykeys.cfg"),
        ]:
            if len(config.read([afile])) > 0:
                configfile = afile
                break
    else:
        if len(config.read([args.config])) == 0:
            raise ValueError(f"Could not read config file: {args.config}")
        configfile = args.config
    if "server" not in config.sections():
        config["server"] = {}
    serverconfig = config["server"]
    if serverconfig.getboolean("rewritepasswordonce", False):
        serverconfig["password"] = mkpasswd(
            24, "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        )
        del serverconfig["rewritepasswordonce"]
        if "client" in config.sections():
            config["client"]["password"] = serverconfig["password"]
        with open(configfile, "w") as f:
            config.write(f)
    isdaemon = (
        args.daemon or serverconfig.getboolean("daemon", False)
        if os.name == "posix"
        else False
    )
    if isdaemon:
        pidfile = os.path.realpath(args.pidfile or serverconfig.get("pidfile", None))
        with DaemonContext(working_directory=os.getcwd(), pidfile=PIDLockFile(pidfile)):
            init_logger(dirname, True, args, serverconfig)
            return do_main(args, serverconfig, interrupt)
    else:
        init_logger(dirname, False, args, serverconfig)
        return do_main(args, serverconfig, interrupt)


# MAIN
if __name__ == "__main__":
    ret = main()
    exit(ret)
