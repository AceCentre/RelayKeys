# -*- coding: utf-8 -*-

#
# The control daemon for handling BLE HID
# communication with http-JSON-RPC
#


# To debug - without the correct hardware attached:
#   Run demoSerial.py 
#   Call this code with relayKeys.py --noserial 

import os, serial
from time import sleep
from sys import exit
import sys
import serial.tools.list_ports
from hashlib import sha256
from threading import Thread
from queue import Queue, Empty as QueueEmpty
import array as arr
from os import urandom
from math import floor

if os.name =='posix': # unix based OS
  from daemon import DaemonContext
  from lockfile.pidlockfile import PIDLockFile

# util modules
import logging
import argparse
from configparser import ConfigParser
import traceback

# rpc modules
from werkzeug.wrappers import Request, Response
from werkzeug.serving import make_server, BaseRequestHandler
from jsonrpc import JSONRPCResponseManager, Dispatcher
from jsonrpc.jsonrpc2 import JSONRPC20Response

from blehid import blehid_send_keyboardcode, blehid_init_serial, \
  blehid_send_movemouse, blehid_send_mousebutton, blehid_send_devicecommand

# from pygame.locals import *
# from pygame.compat import as_bytes
# BytesIO = pygame.compat.get_BytesIO()

#Use AT+BAUDRATE=115200 but make sure hardware flow control CTS/RTS works
DEFAULT_BAUD = 115200
# BAUD = 9600
nrfVID = '239A'
nrfPID = '8029'
RETRY_TIMEOUT=10
QUEUE_TIMEOUT=3

parser = argparse.ArgumentParser(description='Relay keys daemon, BLEHID controller.')
parser.add_argument('--noserial', dest='noserial', action='store_const',
                    const=True, default=False,
                    help='debug option to run the daemon with no hardware (with help of demoSerial.py')
parser.add_argument('--dev', dest='dev', default=None,
                    help='device to use as bluetooth serial')
parser.add_argument('--baud', dest='baud', default=None,
                    help='specify serial baud, default: {}'.format(DEFAULT_BAUD))
parser.add_argument('--debug', dest='debug', action='store_const',
                    const=True, default=False,
                    help='set logger to debug level')
parser.add_argument('--daemon', '-d', dest='daemon', action='store_const',
                    const=True, default=False,
                    help='Run as daemon, posfix specific')
parser.add_argument('--pidfile', dest='pidfile', default=None,
                    help='file to hold pid of daemon, posfix specific')
parser.add_argument('--logfile', dest='logfile', default=None,
                    help='file to hold pid of daemon, posfix specific')
parser.add_argument('--config', '-c', dest='config',
                    default=None, help='Path to config file')

class CommandException (BaseException):
  pass

class RPCServExitException (BaseException):
  pass

class AppExitException (BaseException):
  pass

class RequestHandler (BaseRequestHandler):
  def log(self, type, message, *args):
    # treat `info` logs as `debug
    lvl = logging.DEBUG
    if type == 'error':
      lvl = logging.ERROR
    logging.log(lvl, '%s - - [%s] %s\n' % (self.address_string(),
                                           self.log_date_time_string(),
                                           message % args))

def rpc_server_worker(host, port, username, password, queue):
  dispatcher = Dispatcher()
  srv = None
  # prehash password
  password = int(sha256(bytes(password, "utf8")).hexdigest(), 16)

  @dispatcher.add_method
  def actions (args):
    try:
      actionlist = args[0]
      for action in actionlist:
        if action[0] not in ('mousemove', 'mousebutton', 'keyevent'):
          raise ValueError('unknown action')
      queue.put((None, 'actions', actionlist), True)
      return "OK"
    except:
      return "UNEXPECTED_INPUT"

  @dispatcher.add_method
  def mousebutton (args):
    respqueue = Queue(1)
    queue.put((respqueue, "mousebutton") + tuple(args), True)
    try:
      return respqueue.get(True, 5)
    except QueueEmpty:
      return "TIMEOUT"
  
  @dispatcher.add_method
  def mousemove (args):
    respqueue = Queue(1)
    queue.put(("mousemove", respqueue) + tuple(args), True)
    try:
      return respqueue.get(True, 5)
    except QueueEmpty:
      return "TIMEOUT"
  
  @dispatcher.add_method
  def keyevent (args):
    key, modifiers, down = args
    respqueue = Queue(1)
    queue.put((respqueue, "keyevent", key, modifiers or [], down), True)
    try:
      return respqueue.get(True, 5)
    except QueueEmpty:
      return "TIMEOUT"

  @dispatcher.add_method
  def devicecommand (args):
    devcommand = args
    respqueue = Queue(1)
    queue.put((respqueue, "devicecommand", devcommand), True)
    try:
      return respqueue.get(True, 5)
    except QueueEmpty:
      return "TIMEOUT"

  
  @dispatcher.add_method
  def exit (args):
    respqueue = Queue(1)
    queue.put((respqueue, "exit"), True)
    try:
      respqueue.get(True, 5)
    except:
      pass
    raise RPCServExitException()

  @Request.application
  def app (request):
    # auth with simplified version of equal op (timing attack secure)
    if (username != "" or password != "") and \
       (getattr(request.authorization,"username","") != username or \
        int(sha256(bytes(getattr(request.authorization,"password",""), "utf8")).hexdigest(), 16) - \
        password != 0):
      json = JSONRPC20Response(error={"code":403, "message": "Invalid username or password!"}).json
      return Response(json, 403, mimetype='application/json')
    response = JSONRPCResponseManager.handle(request.data, dispatcher)
    return Response(response.json, mimetype='application/json')

  try:
    # response queue is used to notify result of attempt to run the server
    respqueue = queue.get()
    srv = make_server(host, port, app, request_handler=RequestHandler)
    logging.info("http-jsonrpc listening at {}:{}".format(host, port))
    queue.task_done() # let run_rpc_server return
    respqueue.put("SUCCESS")
    srv.serve_forever()
  except RPCServExitException:
    logging.info("Exit exception raised!")
  except:
    queue.task_done()
    respqueue.put("FAIL")
    logging.error(traceback.format_exc())

# run rpc server on another thread
def run_rpc_server (host, port, username, password):
  queue = Queue(10)
  respqueue = Queue(1)
  queue.put(respqueue)
  t = Thread(target=rpc_server_worker, args=(host, port, username, password,
                                             queue))
  t.daemon = True
  t.start()
  if respqueue.get(True) == "FAIL":
    return None
  return queue

def find_device_path (noserial, seldev):
  dev = None
  if noserial: 
    if os.name =='posix':
      serialdemofile = os.path.join(os.path.dirname(os.path.realpath(__file__)), '.serialDemo')
      if os.path.isfile(serialdemofile):
        with open(serialdemofile, 'r') as f:
          dev = f.read()
      else:
        logging.critical('no-serial is set to true.. Please make sure you have already run \'python resources\demoSerial.py\' from a different shell')
        exit(-1)
    elif (os.name=='nt'):
      dev = 'COM7' if seldev is None else seldev
  else:
    # Default names
    if (os.name=='posix'):
      dev = '/dev/ttyUSB0' if seldev is None else seldev
    else:
      dev = 'COM6' if seldev is None else seldev
      # Look for Adafruit CP2104 break out board or Feather nRF52. Use the first 
      # one found. Default is /dev/ttyUSB0 Or COM6 (Windows)
      # tty for Bluetooth device with baud
      # NB: Could be p.device with a suitable name we are looking for. Noticed some variation around this
    if seldev is None:
      for p in serial.tools.list_ports.comports():
        if "CP2104" in p.description:
          logging.debug('serial desc:'+ str(p))
          dev = p.device
          break
        elif "nRF52" in p.description:
          logging.debug('serial desc:'+ str(p))
          dev = p.device
          break
        elif nrfVID and nrfPID in p.hwid:
          logging.debug('serial desc:'+ str(p))
          dev = p.device
          break
  return dev

class DummySerial (object):
  def __init__ (self, devpath, baud, **kwargs):
    pass
  def __enter__ (self):
    return self
  def __exit__ (self, a, b, c):
    pass
  def write (self, data):
    print("{}".format(data))
  def flushInput (self):
    pass
  def readline (self):
    return "OK\n"

def do_main (args, config, interrupt=None):
  # actions queue
  queue = run_rpc_server(config.get("host", "localhost"),
                         config.getint("port", 5383),
                         config.get("username", ""),
                         config.get("password", ""))
  try: # remove password from memory
    del config["password"]
  except:
    pass
  if queue is None:
    logging.critical("Could not start rpc server")
    return -1 # exit the process
  quit = False
  while not quit:
    try:
      if interrupt is not None:
        interrupt()
      baud = args.baud if args.baud is not None else config.get("baud", DEFAULT_BAUD)
      seldev = args.dev if args.dev is not None else config.get("dev", None)
      noserial = True if args.noserial else config.getboolean("noserial", False)
      devicepath = find_device_path(noserial, seldev)
      if os.name == 'nt' and noserial:
        SerialCls = DummySerial
      else:
        SerialCls = serial.Serial
      with SerialCls(devicepath, baud, rtscts=1) as ser:
        logging.info("serial device opened: {}".format(devicepath))
        #logging.info("INIT MSG: {}".format(str(ser.readline(), "utf8")))
        blehid_init_serial(ser)
        # Six keys for USB keyboard HID report
        # uint8_t keys[6] = {0,0,0,0,0,0}
        keys = arr.array('B', [0, 0, 0, 0, 0, 0])
        try:
          while True:
            if interrupt is not None:
              interrupt()
            try:
              cmd = queue.get(True, QUEUE_TIMEOUT) # with timeout
              output = process_action(ser, keys, cmd[1:])
              if cmd[0] is not None:
                cmd[0].put(output)
              queue.task_done()
            except QueueEmpty:
              pass
        except AppExitException:
          quit = True
    except:
      logging.error(traceback.format_exc())
      logging.info("Will retry in {} seconds".format(RETRY_TIMEOUT))
      sleep(RETRY_TIMEOUT)
  logging.info("relaykeysd exit!")
  return 0


def process_action (ser, keys, cmd):
  try:
    if cmd[0] == "actions":
      outputs = []
      for action in cmd[1]:
        outputs.append(process_action(ser, keys, action))
      return ", ".join(outputs)
    if cmd[0] == "keyevent":
      key = cmd[1]
      modifiers = cmd[2]
      down = cmd[3]
      blehid_send_keyboardcode(ser, key, modifiers, down, keys)
    elif cmd[0] == "mousemove":
      right = int(cmd[1])
      down = int(cmd[2])
      wheely = int(cmd[3] if len(cmd) > 3 else 0)
      wheelx = int(cmd[4] if len(cmd) > 4 else 0)
      blehid_send_movemouse(ser, right, down, wheely, wheelx)
    elif cmd[0] == "mousebutton":
      btn = str(cmd[1]).lower() if cmd[1] is not None else None
      behavior = str(cmd[2]).lower() if len(cmd) > 2 and cmd[2] is not None else None
      if len(btn) > 1 or btn not in  "lrmbf0":
        raise CommandException("Unknown mousebutton: {}".format(btn))
      if behavior is not None and behavior not in ("press","click","doubleclick","hold"):
        raise CommandException("Unknown mousebutton behavior: {}".format(behavior))
      blehid_send_mousebutton(ser, btn, behavior)
    # response queue given by cmd
    return "SUCCESS"
  except:
    logging.error(traceback.format_exc())
    return "FAIL"
  if cmd[0] == "exit":
    raise AppExitException()

def init_logger (dirname, isdaemon, args, config):
  # init logger
  loggerformatter = logging.Formatter('%(asctime)-15s: %(message)s')
  logger = logging.getLogger()
  # logging stdout handler
  if not isdaemon:
    handler = logging.StreamHandler()
    handler.setFormatter(loggerformatter)
    logger.addHandler(handler)
  # logging file handler
  if args.logfile is None:
    logfile = config.get("logfile", None)
    if os.path.abspath(logfile) != logfile:
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
  if logfile is None and isdaemon: # disable logger
    logging.disable(sys.maxsize)

def mkpasswd(n, chars):
  ret = ""
  charsn=len(chars)
  while n > 0:
    index = int(floor((int.from_bytes(urandom(4), byteorder='little', signed=False) / 2**(8*4)) * charsn))
    ret += chars[index]
    n -= 1
  return ret
  
def main (interrupt=None):
  args = parser.parse_args()
  config = ConfigParser()
  dirname = os.path.dirname(os.path.realpath(sys.argv[0]))
  if args.config is None:
    configfile = None
    for afile in [ os.path.expanduser('~/.relaykeys.cfg'),
                    os.path.join(dirname, 'relaykeys.cfg') ]:
      if len(config.read([afile])) > 0:
        configfile = afile
        break
  else:
    if len(config.read([args.config])) == 0:
      raise ValueError("Could not read config file: {}".format(args.config))
    configfile = args.config
  if "server" not in config.sections():
    config["server"] = {}
  serverconfig = config["server"]
  if serverconfig.getboolean("rewritepasswordonce", False):
    serverconfig["password"] = mkpasswd(24, "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    del serverconfig["rewritepasswordonce"]
    if "client" in config.sections():
      config["client"]["password"] = serverconfig["password"]
    with open(configfile, "w") as f:
      config.write(f)
  isdaemon = args.daemon or serverconfig.getboolean("daemon", False) if os.name =='posix' else False
  if isdaemon:
    pidfile = os.path.realpath(args.pidfile or serverconfig.get("pidfile", None))
    with DaemonContext(working_directory=os.getcwd(),
                       pidfile=PIDLockFile(pidfile)):
      init_logger(dirname, True, args, serverconfig)
      return do_main(args, serverconfig, interrupt)
  else:
    init_logger(dirname, False, args, serverconfig)
    return do_main(args, serverconfig, interrupt)

  
# MAIN
if __name__ == '__main__':
  ret = main()
  exit(ret)
    
