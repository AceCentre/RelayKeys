# -*- coding: utf-8 -*-
import os
from time import sleep
from sys import exit
import sys

# util modules
import logging
import argparse
from configparser import ConfigParser
import traceback
import pyperclip

from relaykeysclient import RelayKeysClient

parser = argparse.ArgumentParser(description='Relay keys daemon, BLEHID controller.')
parser.add_argument('--debug', dest='debug', action='store_const',
                    const=True, default=False,
                    help='set logger to debug level')
parser.add_argument('--config', '-c', dest='config',
                    default=None, help='Path to config file')
parser.add_argument('--url', '-u', dest='url', default=None,
                    help='rpc http url, default: http://localhost:5383/')
parser.add_argument('--delay', dest='delay', type=int, default=0,
                    help='delay between each call, in miliseconds')
parser.add_argument('commands', metavar='COMMAND', nargs='+',
                    help='One or more commands, format: <cmdname>:<data>')

def parse_commamd (cmd):
  parts = cmd.split(":")
  data = ":".join(parts[1:])
  return (parts[0], data)

class CommandErrorResponse (BaseException):
  pass

def do_keyevent (client, key, modifiers, isdown):
  ret = client.keyevent(key, modifiers, isdown)
  if 'result' not in ret:
    logging.error("keyevent ({}, {}, {}) response error: {}".format(key, modifiers, isdown, ret.get("error", "undefined")))
    raise CommandErrorResponse()
  else:
    logging.info("keyevent ({}, {}, {}) response: {}".format(key, modifiers, isdown, ret["result"]))

def do_mousemove (client, right, down):
  ret = client.mousemove(right, down)
  if 'result' not in ret:
    logging.error("mousemove ({}, {}) response error: {}".format(right, down, ret.get("error", "undefined")))
    raise CommandErrorResponse()
  else:
    logging.info("mousemove ({}, {}) response: {}".format(right, down, ret["result"]))

def do_mousebutton (client, btn, behavior=None):
  ret = client.mousebutton(btn, behavior)
  if 'result' not in ret:
    logging.error("mousebutton ({}, {}) response error: {}".format(btn, behavior, ret.get("error", "undefined")))
    raise CommandErrorResponse()
  else:
    logging.info("mousebutton ({}, {}) response: {}".format(btn, behavior, ret["result"]))

def do_devicecommand(client, devcommand):
  ret = client.devicecommand(devcommand)
  if 'result' not in ret:
    logging.error("devicecommand ({}) response error: {}".format(devcommand, ret.get("error", "undefined")))
    raise CommandErrorResponse()
  else:
    logging.info("devicecommand ({}) response : {}".format(devcommand, ret["result"]))


nonchars_key_map = {
  "\r": (None, None),
  "\t": ("TAB", []),
  " ": ("SPACE", []),
  "`": ("BACKQUOTE", []),
  "~": ("BACKQUOTE", ["LSHIFT"]),
  "!": ("1", ["LSHIFT"]),
  "@": ("2", ["LSHIFT"]),
  "#": ("3", ["LSHIFT"]),
  "$": ("4", ["LSHIFT"]),
  "%": ("5", ["LSHIFT"]),
  "^": ("6", ["LSHIFT"]),
  "&": ("7", ["LSHIFT"]),
  "*": ("8", ["LSHIFT"]),
  "(": ("9", ["LSHIFT"]),
  ")": ("0", ["LSHIFT"]),
  "_": ("MINUS", ["LSHIFT"]),
  "+": ("EQUALS", ["LSHIFT"]),
  "-": ("MINUS", []),
  "=": ("EQUALS", []),
  ";": ("SEMICOLON", []),
  ":": ("SEMICOLON", ["LSHIFT"]),
  "[": ("LEFTBRACKET", []),
  "{": ("LEFTBRACKET", ["LSHIFT"]),
  "]": ("RIGHTBRACKET", []),
  "}": ("RIGHTBRACKET", ["LSHIFT"]),
  "\\": ("BACKSLASH", []),
  "|": ("BACKSLASH", ["LSHIFT"]),
  "\n": ("RETURN", ["LSHIFT"]),
  ",": ("COMMA", []),
  ".": ("PERIOD", []),
  "<": ("COMMA", ["LSHIFT"]),
  ">": ("PERIOD", ["LSHIFT"]),
  "/": ("SLASH", []),
  "?": ("SLASH", ["LSHIFT"]),
}
def char_to_keyevent_params (char):
  ret = nonchars_key_map.get(char, None)
  if ret is not None:
    return ret
  return (char.upper(), ["LSHIFT"] if char.upper() == char else [])
    
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
      url = "http://localhost:5383/"
    client = RelayKeysClient(url=url)
  delay = config.getint("delay", 0) if args.delay == 0 else args.delay
  for cmd in args.commands:
    name, data = parse_commamd(cmd)
    if name == "type":
      for char in data:
        key, mods = char_to_keyevent_params(char)
        if key is not None:
          do_keyevent(client, key, mods, True)
          if delay > 0:
            sleep(delay/1000.0)
          do_keyevent(client, key, mods, False)
          if delay > 0:
            sleep(delay/1000.0)
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
      do_mousemove(client, right, down)
      if delay > 0:
        sleep(delay/1000.0)
    elif name == "mousebutton":
      parts = data.split(",")
      btn = parts[0]
      behavior = None if len(parts) < 2 else parts[1]
      do_mousebutton(client, btn, behavior)
      if delay > 0:
        sleep(delay/1000.0)
    elif name == "device-cmd":
      parts = data.split(",")
      print(parts)
      command = parts[0]
      do_devicecommand(client,command)
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
  return do_main(args, config["client"])

if __name__ == '__main__':
  ret = main()
  exit(ret)
