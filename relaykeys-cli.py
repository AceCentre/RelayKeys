# -*- coding: utf-8 -*-
import os
from time import sleep
from sys import exit
import sys
from pathlib import Path
import json

# util modules
import logging
import argparse
from configparser import ConfigParser
import traceback
import pyperclip

from relaykeysclient import RelayKeysClient

from notifypy import Notify

from cli_keymap import *

parser = argparse.ArgumentParser(description='Relay keys daemon, BLEHID controller.')
parser.add_argument('--debug', dest='debug', action='store_const',
                    const=True, default=False,
                    help='set logger to debug level')
parser.add_argument('--config', '-c', dest='config',
                    default=None, help='Path to config file')
parser.add_argument('--url', '-u', dest='url', default=None,
                    help='rpc http url, default: http://127.0.0.1:5383/')
parser.add_argument('--delay', dest='delay', type=int, default=0,
                    help='delay between each call, in miliseconds')
parser.add_argument('--notify', dest='notify', action='store_const',
                    const=True, default=False, help='Send response as notification')
parser.add_argument('--copy', dest='copy_return', action='store_const',
                    const=True, default=False, help='Send response to pasteboard')
parser.add_argument('-f', dest='macro',
                    default=None, help='Path to macro file')
parser.add_argument('commands', metavar='COMMAND', nargs='*',
                    help='One or more commands, format: <cmdname>:<data>')

def parse_macro(file_arg):
  # if argument is file name without any path check it in macros folder
  if file_arg.find('/') == -1 and file_arg.find('/') == -1:
    file_path = Path(__file__).resolve().parent / "macros" / file_arg 
    if not Path(file_path).is_file():
      print("Specified file doesn't exist in macros folder: ", file_path)
      return []
  elif Path(file_arg).is_file(): # otherwise check it as file_path
    file_path = file_arg
  else:
      print("Invalid path to macro file: ", file_arg)
      return []
  
  macro_commands = []

  with open(file_path, "r") as file:
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
  notification.title = command_type + " response" 
  if isinstance(result, list):
    result = "\n" + "\n".join(result)
  notification.message = command + " : " + result

  
  notification.send()

def copy_return(command_type, command, result):
  if isinstance(result, list):
    result = "\n" + "\n".join(result)
  pyperclip.copy(result)


def parse_commamd (cmd):
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

class CommandErrorResponse (BaseException):
  pass

def do_keyevent (client, key, modifiers, isdown):
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
  ret = client.keyevent(key, modifiers, isdown)
  if 'result' not in ret:
    logging.error("keyevent ({}, {}, {}) response error: {}".format(key, modifiers, isdown, ret.get("error", "undefined")))
    raise CommandErrorResponse()
  else:
    logging.info("keyevent ({}, {}, {}) response: {}".format(key, modifiers, isdown, ret["result"]))

def do_mousemove (client, right, down, wy, wx):
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
  ret = client.mousemove(right, down, wy, wx)
  if 'result' not in ret:
    logging.error("mousemove ({}, {}) response error: {}".format(right, down, ret.get("error", "undefined")))
    raise CommandErrorResponse()
  else:
    logging.info("mousemove ({}, {}) response: {}".format(right, down, ret["result"]))

def do_mousebutton (client, btn, behavior=None):
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
  ret = client.mousebutton(btn, behavior)
  if 'result' not in ret:
    logging.error("mousebutton ({}, {}) response error: {}".format(btn, behavior, ret.get("error", "undefined")))
    raise CommandErrorResponse()
  else:
    logging.info("mousebutton ({}, {}) response: {}".format(btn, behavior, ret["result"]))

def do_devicecommand(client, devcommand, notify=False,copyresults=False):
  ret = client.ble_cmd(devcommand)
  if 'result' not in ret:
    logging.error("devicecommand ({}) response error: {}".format(devcommand, ret.get("error", "undefined")))
    raise CommandErrorResponse()
  else:
    logging.info("devicecommand ({}) response : {}".format(devcommand, ret["result"]))
    if notify:
      send_notification("device command", devcommand, ret["result"])
    if copyresults:
      output_copy("daemon command", command, ret["result"])

def do_daemoncommand(client, command, notify=False,copyresults=False):
  ret = client.daemon(command)
  if 'result' not in ret:
    logging.error("daemoncommand ({}) response error: {}".format(command, ret.get("error", "undefined")))
    raise CommandErrorResponse()
  else:
    logging.info("daemoncommand ({}) response : {}".format(command, ret["result"]))
    if notify:
      send_notification("daemon command", command, ret["result"])
    if copyresults:
      output_copy("daemon command", command, ret["result"])

def do_main (args, config):
  url = config.get("url", None) if args.url == None else args.url
  host = config.get("host", None)
  port = config.get("port", None)
  if url is None and not (host is None and port is None):
    client = RelayKeysClient(host=host, port=port,
                             username=config.get("username", None),
                             password=config.get("password", None))
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
      def type_char (char):
        key, mods = char_to_keyevent_params(char)
        if key is not None:
          do_keyevent(client, key, mods, True)
          if delay > 0:
            sleep(delay/1000.0)
          do_keyevent(client, key, mods, False)
          if delay > 0:
            sleep(delay/1000.0)
      escapedict = { "t": "\t", "n": "\n", "r": "\r" }
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
            sleep(delay/1000.0)
          do_keyevent(client, key, mods, False)
          if delay > 0:
            sleep(delay/1000.0)
    elif name == "keyevent":
      parts = data.split(",")
      if len(parts) < 2:
        raise ValueError("Not enough params for keyevent command: {}".format(cmd))
      key = parts[0]
      try:
        isdown = int(parts[-1]) == 1
      except ValueError:
        raise ValueError("Last param of keyevent command should be one of (0,1), in cmd: {}".format(cmd))
      modifiers = parts[1:]
      do_keyevent(client, key, modifiers, isdown)
      if delay > 0:
        sleep(delay/1000.0)
    elif name == "keypress":
      parts = data.split(",")
      key = parts[0]
      modifiers = parts[1:]
      do_keyevent(client, key, modifiers, True)
      if delay > 0:
        sleep(delay/1000.0)
      do_keyevent(client, key, modifiers, False)
      if delay > 0:
        sleep(delay/1000.0)
    elif name == "mousemove":
      parts = data.split(",")
      right = parts[0]
      down = parts[1]
      wy = parts[2] if len(parts) > 2 else 0
      wx = parts[3] if len(parts) > 3 else 0
      do_mousemove(client, right, down, wy, wx)
      if delay > 0:
        sleep(delay/1000.0)
    elif name == "mousebutton":
      parts = data.split(",")
      btn = parts[0]
      behavior = None if len(parts) < 2 else parts[1]
      do_mousebutton(client, btn, behavior)
      if delay > 0:
        sleep(delay/1000.0)
    elif name == "ble_cmd":      
      parts = data.split(",")
      #print(parts)
      command = parts[0]
      do_devicecommand(client,command,args.notify,args.copyresults)
    elif name == "daemon":
      parts = data.split(",")      
      command = parts[0]

      do_daemoncommand(client,command,args.notify,args.copyresults)
    elif name == "delay":
      logging.info("delay: {}ms".format(data))
      delay_value = float(data)
      sleep(delay_value/1000.0)
    else:
      raise ValueError("Unknown command: {}".format(cmd))


def main ():
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
    config.read([
      os.path.expanduser('~/.relaykeys.cfg'),
      os.path.join(dirname, 'relaykeys.cfg'),
    ])
  else:
    config.read([args.config])
  if "client" not in config.sections():
    config["client"] = {}

  if "cli" not in config.sections():
    config["cli"] = {}
  
  if not load_keymap_file(config["cli"]):
    return
   
  return do_main(args, config["client"])

if __name__ == '__main__':
  ret = main()
  exit(ret)
