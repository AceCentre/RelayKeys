import argparse

# util modules
import logging
import os
import subprocess
import sys
from configparser import ConfigParser
from pathlib import Path
from sys import exit
from time import sleep

import pyperclip
from notifypy import Notify

from ..core.client import RelayKeysClient
from .keymap import *

parser = argparse.ArgumentParser(description="Relay keys daemon, BLEHID controller.")
parser.add_argument(
    "--debug",
    dest="debug",
    action="store_const",
    const=True,
    default=False,
    help="set logger to debug level",
)
parser.add_argument(
    "--config", "-c", dest="config", default=None, help="Path to config file"
)
parser.add_argument(
    "--url",
    "-u",
    dest="url",
    default=None,
    help="rpc http url, default: http://127.0.0.1:5383/",
)
parser.add_argument(
    "--delay",
    dest="delay",
    type=int,
    default=0,
    help="delay between each call, in miliseconds",
)
parser.add_argument(
    "--notify",
    dest="notify",
    action="store_const",
    const=True,
    default=False,
    help="Send response as notification",
)
parser.add_argument(
    "--copy",
    dest="copyresults",
    action="store_const",
    const=True,
    default=False,
    help="Send response to pasteboard",
)
parser.add_argument("-f", dest="macro", default=None, help="Path to macro file")
parser.add_argument(
    "commands",
    metavar="COMMAND",
    nargs="*",
    help="One or more commands, format: <cmdname>:<data>",
)


def parse_macro(file_arg):
    # if argument is file name without any path check it in macros folder
    if file_arg.find("/") == -1 and file_arg.find("\\") == -1:
        file_path = Path(__file__).resolve().parent.parent.parent.parent / "macros" / file_arg
        if not Path(file_path).is_file():
            print("Specified file doesn't exist in macros folder: ", file_path)
            return []
    elif Path(file_arg).is_file():  # otherwise check it as file_path
        file_path = file_arg
    else:
        print("Invalid path to macro file: ", file_arg)
        return []

    macro_commands = []

    with open(file_path) as file:
        for line in file.readlines():
            cmd = line.strip("\n")
            if cmd == "":
                continue
            else:
                macro_commands.append(cmd)

    return macro_commands


def send_notification(command_type, command, result):
    notification = Notify()
    notification.application_name = "Relaykeys"
    notification.title = ""
    notification.icon = str(Path(__file__).resolve().parent.parent.parent.parent / "assets" / "icons" / "logo.png")

    if result == "TIMEOUT" or result == "FAIL" or result == "No connection with dongle":
        notification.message = (
            f"Sending {command_type} failed. Check dongle connection status"
        )
    else:
        if command == "devname":
            notification.message = f"Connected to {result}."
        elif command == "devlist":
            notification.message = "Device list:\n" + "\n".join(result)
        elif command == "devadd":
            notification.message = (
                "Adding new device. Connect your device with Relaykeys dongle."
            )
        elif command == "devreset":
            notification.message = "Device list is cleared."
        elif command == "switch":
            notification.message = "Switching to next device."
        elif command.startswith("switch="):
            notification.message = 'Trying to switch to "{}"'.format(
                command.split("=")[1]
            )
        elif "devremove" in command:
            removed_device = command.split("=")[1]
            notification.message = f"{removed_device} was removed from device list."
        elif command == "get_mode":
            notification.message = f"Daemon running in {result} mode."
        elif command == "switch_mode":
            notification.message = "Switching daemon mode."
        elif command == "dongle_status":
            notification.message = f"Dongle status: {result}."

    notification.send()


def copy_return(command_type, command, result):
    if isinstance(result, list):
        result = ", " + ", ".join(result)
    pyperclip.copy(result)


def parse_commamd(cmd):
    """Parses a command provide from the command line.

    Parses a command found on the command line. I

    Args:
        cmd: The command, e.g. `paste` or `type:hello`

    Returns:
         a list of command, data
    """
    parts = cmd.split(":")
    data = ":".join(parts[1:])
    return (parts[0], data)


class CommandErrorResponse(BaseException):
    pass


def do_keyevent(client, key, modifiers, isdown):
    """Sends a key event to the daemon

    For example - press a key with modifiers - and note is the key down or up

    Args:
        client: the RPC client already created
        key:key (letter, number or one of the defined keycodes), modifiers, isDown:0/1

    Returns:
         client.keyevent object

    Raises:
        Logging error
    """
    try:
        ret = client.keyevent(key, modifiers, isdown)
        logging.info(
            f"keyevent ({key}, {modifiers}, {isdown}) response: {ret}"
        )
    except Exception as e:
        logging.error(
            f"keyevent ({key}, {modifiers}, {isdown}) response error: {str(e)}"
        )
        raise CommandErrorResponse()


def do_mousemove(client, right, down, wy, wx):
    """Sends a mouse move event to the daemon

    For example - move mouse right n pixels and down n pixels. To move left or up - use negative numbers.

    Args:
        client: the RPC client already created
        right: pixels to move right - or if left use negative number
        down: pixels to move down - or up - use a negative number

    Returns:
         client.keyevent object

    Raises:
        Logging error
    """
    try:
        ret = client.mousemove(right, down, wy, wx)
        logging.info(
            f"mousemove ({right}, {down}) response: {ret}"
        )
    except Exception as e:
        logging.error(
            f"mousemove ({right}, {down}) response error: {str(e)}"
        )
        raise CommandErrorResponse()


def do_mousebutton(client, btn, behavior=None):
    """Sends a mouse button event to the daemon

    For example - click left mouse button

    Args:
        client: the RPC client already created
        right: Button: L or R, M for middle. Scroll: F (Forward), B (Backward)
        behavior: click or doubleclick. Default is a Hold and Release for 0 secs.

    Returns:
         client.keyevent object

    Raises:
        Logging error
    """
    try:
        ret = client.mousebutton(btn, behavior)
        logging.info(
            f"mousebutton ({btn}, {behavior}) response: {ret}"
        )
    except Exception as e:
        logging.error(
            f"mousebutton ({btn}, {behavior}) response error: {str(e)}"
        )
        raise CommandErrorResponse()


def do_devicecommand(client, devcommand, notify=False, copyresults=False):
    try:
        ret = client.ble_cmd(devcommand)
        logging.info(
            f"devicecommand ({devcommand}) response : {ret}"
        )
        if notify:
            send_notification("device command", devcommand, ret)
            if devcommand.startswith("switch"):
                exe_path = Path(__file__).resolve().parent.parent.parent.parent / "scripts" / "poll_devname.exe"
                if exe_path.exists():
                    # run exe if builded
                    subprocess.Popen([str(exe_path)])
                else:
                    # run script if no exe
                    script_path = Path(__file__).resolve().parent.parent / "utils" / "device_poller.py"
                    subprocess.Popen(["python", str(script_path)])
        if copyresults:
            copy_return("daemon command", devcommand, ret)
    except Exception as e:
        logging.error(
            f"devicecommand ({devcommand}) response error: {str(e)}"
        )
        raise CommandErrorResponse()


def do_daemoncommand(client, command, notify=False, copyresults=False):
    try:
        ret = client.daemon(command)
        logging.info(f"daemoncommand ({command}) response : {ret}")
        if notify:
            send_notification("daemon command", command, ret)
        if copyresults:
            copy_return("daemon command", command, ret)
    except Exception as e:
        logging.error(
            f"daemoncommand ({command}) response error: {str(e)}"
        )
        raise CommandErrorResponse()


def do_main(args, config):
    url = config.get("url", None) if args.url == None else args.url
    host = config.get("host", None)
    port = config.get("port", None)
    if url is None and not (host is None and port is None):
        client = RelayKeysClient(
            host=host,
            port=port,
            username=config.get("username", None),
            password=config.get("password", None),
        )
    else:
        if url is None:
            url = "http://127.0.0.1:5383/"
        client = RelayKeysClient(url=url)

    delay = config.getint("delay", 0) if args.delay == 0 else args.delay

    commands_list = []
    if args.macro != None:
        commands_list += parse_macro(args.macro)
    commands_list += args.commands

    for cmd in commands_list:
        name, data = parse_commamd(cmd)
        if name == "type":

            def type_char(char):
                key, mods = char_to_keyevent_params(char)
                if key is not None:
                    do_keyevent(client, key, mods, True)
                    if delay > 0:
                        sleep(delay / 1000.0)
                    do_keyevent(client, key, mods, False)
                    if delay > 0:
                        sleep(delay / 1000.0)

            escapedict = {"t": "\t", "n": "\n", "r": "\r"}
            escaped = False
            for char in data:
                if char == "\\":
                    if not escaped:
                        escaped = True
                        continue
                    else:
                        escaped = False
                elif escaped:
                    escaped = False
                    if char in escapedict:
                        char = escapedict[char]
                    else:
                        type_char("\\")
                type_char(char)
        elif name == "paste":
            data = pyperclip.paste()
            for char in data:
                key, mods = char_to_keyevent_params(char)
                if key is not None:
                    do_keyevent(client, key, mods, True)
                    if delay > 0:
                        sleep(delay / 1000.0)
                    do_keyevent(client, key, mods, False)
                    if delay > 0:
                        sleep(delay / 1000.0)
        elif name == "keyevent":
            parts = data.split(",")
            if len(parts) < 2:
                raise ValueError(f"Not enough params for keyevent command: {cmd}")

            key = parts[0]
            if len(parts) == 2:
                modifiers = None
            elif len(parts) > 2:
                modifiers = parts[1:-1]
            try:
                isdown = int(parts[-1]) == 1
            except ValueError:
                raise ValueError(
                    f"Last param of keyevent command should be one of (0,1), in cmd: {cmd}"
                )

            do_keyevent(client, key, modifiers, isdown)
            if delay > 0:
                sleep(delay / 1000.0)
        elif name == "keypress":
            parts = data.split(",")
            key = parts[0]
            modifiers = parts[1:]
            do_keyevent(client, key, modifiers, True)
            if delay > 0:
                sleep(delay / 1000.0)
            do_keyevent(client, key, modifiers, False)
            if delay > 0:
                sleep(delay / 1000.0)
        elif name == "mousemove":
            parts = data.split(",")
            right = parts[0]
            down = parts[1]
            wy = parts[2] if len(parts) > 2 else 0
            wx = parts[3] if len(parts) > 3 else 0
            do_mousemove(client, right, down, wy, wx)
            if delay > 0:
                sleep(delay / 1000.0)
        elif name == "mousebutton":
            parts = data.split(",")
            btn = parts[0]
            behavior = None if len(parts) < 2 else parts[1]
            do_mousebutton(client, btn, behavior)
            if delay > 0:
                sleep(delay / 1000.0)
        elif name == "ble_cmd":
            parts = data.split(",")
            # print(parts)
            command = parts[0]
            do_devicecommand(client, command, args.notify, args.copyresults)
        elif name == "daemon":
            parts = data.split(",")
            command = parts[0]

            do_daemoncommand(client, command, args.notify, args.copyresults)
        elif name == "delay":
            logging.info(f"delay: {data}ms")
            delay_value = float(data)
            sleep(delay_value / 1000.0)
        else:
            raise ValueError(f"Unknown command: {cmd}")


def main():
    args = parser.parse_args()
    # init logger
    logger = logging.getLogger()
    logging.getLogger().addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)
    if args.debug:
        logger.setLevel(logging.DEBUG)
    config = ConfigParser()
    dirname = os.path.dirname(os.path.realpath(sys.argv[0]))
    if args.config is None:
        config.read(
            [
                os.path.expanduser("~/.relaykeys.cfg"),
                os.path.join(dirname, "relaykeys.cfg"),
            ]
        )
    else:
        config.read([args.config])
    if "client" not in config.sections():
        config["client"] = {}

    if "cli" not in config.sections():
        config["cli"] = {}

    if not load_keymap_file(config["cli"]):
        return

    return do_main(args, config["client"])


if __name__ == "__main__":
    ret = main()
    exit(ret)
