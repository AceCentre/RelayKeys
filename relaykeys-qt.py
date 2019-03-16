# -*- coding: utf-8 -*-
import os
from time import sleep
from sys import exit, argv
import sys

# util modules
import logging
import argparse
from configparser import ConfigParser
import traceback

from relaykeysclient import RelayKeysClient

import PyHook3

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QApplication, QSystemTrayIcon, \
  QMessageBox, QLabel, QAction, QMenu, QDialog
from struct import pack, unpack
import win32api, win32con
import pythoncom
from threading import Timer, Thread
from queue import Queue, Empty as EmptyQueue

parser = argparse.ArgumentParser(description='Relay Keys qt client.')
parser.add_argument('--debug', dest='debug', action='store_const',
                    const=True, default=False,
                    help='set logger to debug level')
parser.add_argument('--config', '-c', dest='config',
                    default=None, help='Path to config file')
parser.add_argument('--url', '-u', dest='url', default=None,
                    help='rpc http url, default: http://localhost:5383/')
parser.add_argument('--togglekey', dest='togglekey', default=None,
                    help='A key to disable/enable relay keys: default: None')
parser.add_argument('--togglemods', dest='togglemods', default=None,
                    help='List of required modifiers for toggle key separated by comma, default: None')

modifiers_map = dict([
  (162, "LCTRL"),
  (163, "RCTRL"),
  (160, "LSHIFT"),
  (161, "RSHIFT"),
  (165, "RALT"),
  (164, "LALT"),
])

keysmap = dict([
  (65, "A"),
  (66, "B"),
  (67, "C"),
  (68, "D"),
  (69, "E"),
  (70, "F"),
  (71, "G"),
  (72, "H"),
  (73, "I"),
  (74, "J"),
  (75, "K"),
  (76, "L"),
  (77, "M"),
  (78, "N"),
  (79, "O"),
  (80, "P"),
  (81, "Q"),
  (82, "R"),
  (83, "S"),
  (84, "T"),
  (85, "U"),
  (86, "V"),
  (87, "W"),
  (88, "X"),
  (89, "Y"),
  (90, "Z"),
  (49, "1"),
  (50, "2"),
  (51, "3"),
  (52, "4"),
  (53, "5"),
  (54, "6"),
  (55, "7"),
  (56, "8"),
  (57, "9"),
  (48, "0"),
  (190, "PERIOD"),
  (188, "COMMA"),
  (186, "SEMICOLON"),
  (0xBD, "MINUS"), # VK_OEM_MINUS
  (187, "EQUALS"),
  (191, "SLASH"),
  (220, "BACKSLASH"),
  (222, "QUOTE"),
  (219, "LEFTBRACKET"),
  (221, "RIGHTBRACKET"),
  (13, "ENTER"),
  (32, "SPACE"),
  (8, "BACKSPACE"),
  (9, "TAB"),
  (445, "UNDERSCORE"),
  (33, "PAGEUP"),
  (34, "PAGEDOWN"),
  (37, "LEFTARROW"),
  (39, "RIGHTARROW"),
  (38, "UPARROW"),
  (40, "DOWNARROW"),
  (27, "ESCAPE"),
  (36, "HOME"),
  (35, "END"),
  (45, "INSERT"),
  (46, "DELETE"),
  (0x5B, "LGUI"),
  (0x5C, "RGUI"),
  (93, "APP"), # Applications key
  (20, "CAPSLOCK"),
  (112, "F1"),
  (113, "F2"),
  (114, "F3"),
  (115, "F4"),
  (116, "F5"),
  (117, "F6"),
  (118, "F7"),
  (119, "F8"),
  (120, "F9"),
  (121, "F10"),
  (122, "F11"),
  (123, "F12"),
  (0xC0, "BACKQUOTE"), # Keyboard Non-US # and ~
  (0x2C, "PRINTSCREEN"), # Keyboard PrintScreen, VK_SNAPSHOT
  (0x2B, "EXECUTE"), # VK_EXECUTE
  (0x2F, "HELP"), # VK_HELP
  (0x12, "MENU"), # VK_MENU
  (0x13, "PAUSE"), # VK_PAUSE
  (0x29, "SELECT"), # VK_SELECT
  (0xB2, "STOP"), # VK_MEDIA_STOP, Keyboard Stop
  (0xAD, "MUTE"), # VK_VOLUME_MUTE
  (0xAF, "VOLUP"), # VK_VOLUME_UP, Keyboard Volume Up
  (0xAE, "VOLDOWN"), # VK_VOLUME_DOWN, Keyboard Volume Down
  (0x03, "CANCEL"), # VK_CANCEL
  (0x0C, "CLEAR"), # VK_CLEAR, Keyboard Clear
  (0x21, "PRIOR"), # VK_PRIOR, Keyboard Prior
  (0x0D, "RETURN"), # VK_RETURN
  (0x6C, "SEPARATOR"), # VK_SEPARATOR
  (0x5F, "POWER"), # VK_SLEEP
  (0x60, "KP_0"), # VK_NUMPAD0
  (0x61, "KP_1"), # VK_NUMPAD1
  (0x62, "KP_2"), # VK_NUMPAD2
  (0x63, "KP_3"), # VK_NUMPAD3
  (0x64, "KP_4"), # VK_NUMPAD4
  (0x65, "KP_5"), # VK_NUMPAD5
  (0x66, "KP_6"), # VK_NUMPAD6
  (0x67, "KP_7"), # VK_NUMPAD7
  (0x68, "KP_8"), # VK_NUMPAD8
  (0x69, "KP_9"), # VK_NUMPAD9
  (0x6E, "KP_PERIOD"), # VK_DECIMAL
  (0x6A, "KP_MULTIPLY"), # keypad multiply, VK_MULTIPLY
  (0x6F, "KP_DIVIDE"), # keypad divide, VK_DIVIDE
  (0x6B, "KP_PLUS"),
  (0x6D, "KP_MINUS"),
  (0x03, "CANCEL"), # VK_CANCEL
 ])

class KeyboardStatusWidget (QWidget):
  updateStatusSignal = pyqtSignal(list, list, list)

  def __init__(self):
    super(KeyboardStatusWidget, self).__init__()
    self.updateStatusSignal.connect(self.onUpdateStatus)
    self.hlayout = QHBoxLayout()
    self.hlayout.setAlignment(Qt.AlignLeft)
    self.items = []
    self.hlayout.setContentsMargins(0, 0, 0, 0)
    self.setLayout(self.hlayout)

  def addPlusLabel (self):
    label = QLabel()
    label.setContentsMargins(5, 5, 5, 5)
    label.setAlignment(Qt.AlignVCenter)
    fontsize = 10
    label.setText("<font size='{fontsize}'>+</font>"
                 .format(fontsize=fontsize))
    item = QVBoxLayout()
    item.addWidget(label)
    self.items.append(item)
    self.hlayout.addLayout(item)

  def onUpdateStatus (self, keys, modifiers, unknown_keys):
    def layout_del_inner (layout):
      for i in reversed(range(layout.count())): 
        layout.itemAt(i).widget().setParent(None)
    for item in self.items:
      self.hlayout.removeItem(item)
      layout_del_inner(item)
    self.items = []
    for i in range(len(keys)):
      key = keys[i]
      label = QLabel()
      label.setContentsMargins(5, 5, 5, 5)
      label.setAlignment(Qt.AlignVCenter)
      fontsize = 10
      label.setText("<font style='font-weight:bold;' size='{fontsize}'>{text}</font>"
                   .format(text=key, fontsize=fontsize))
      item = QVBoxLayout()
      item.addWidget(label)
      self.items.append(item)
      self.hlayout.addLayout(item)
      if i + 1 != len(keys) or len(modifiers) > 0:
        self.addPlusLabel()
    
    for i in range(len(modifiers)):
      mod = modifiers[i]
      label = QLabel()
      label.setContentsMargins(5, 5, 5, 5)
      label.setAlignment(Qt.AlignVCenter)
      fontsize = 10
      label.setText("<font style='font-weight:bold;' size='{fontsize}'>{text}</font>"
                   .format(text=mod, fontsize=fontsize))
      item = QVBoxLayout()
      item.addWidget(label)
      self.items.append(item)
      self.hlayout.addLayout(item)
      if i + 1 != len(modifiers) or len(unknown_keys) > 0:
        self.addPlusLabel()
    
    for i in range(len(unknown_keys)):
      key = unknown_keys[i]
      label = QLabel()
      label.setContentsMargins(5, 5, 5, 5)
      label.setAlignment(Qt.AlignVCenter)
      fontsize = 10
      label.setText("<font style='font-weight:bold;color:darkred;' size='{fontsize}'>{text}</font>"
                   .format(text="??(0x{:02x})".format(key), fontsize=fontsize))
      item = QVBoxLayout()
      item.addWidget(label)
      self.items.append(item)
      self.hlayout.addLayout(item)
      if i + 1 != len(unknown_keys):
        self.addPlusLabel()

class Window (QDialog):
  showErrorMessageSignal = pyqtSignal(str)

  def __init__ (self, args, config):
    super(Window, self).__init__()
    clientconfig = config["client"]

    self.showErrorMessageSignal.connect(self.showErrorMessage)
    self._disabled = False
    self._keystate_update_timer = None
    self._keys = []
    self._modifiers = []
    self._unknown_keys = []
    self._toggle_key = args.togglekey if args.togglekey != None else clientconfig.get("togglekey", None)
    self._toggle_modifiers = (args.togglemods if args.togglemods != None else clientconfig.get("togglemods", "")).split(",")

    url = clientconfig.get("url", None) if args.url == None else args.url
    host = clientconfig.get("host", None)
    port = clientconfig.get("port", None)
    if url is None and not (host is None and port is None):
      self.client = RelayKeysClient(host=host, port=port,
                               username=clientconfig.get("username", None),
                               password=clientconfig.get("password", None))
    else:
      if url is None:
        url = "http://localhost:5383/"
      self.client = RelayKeysClient(url=url)
    self._client_queue = Queue(10)
    t = Thread(target=self.client_worker, args=(self._client_queue,))
    t.start()

    self.initKeyboardHook()
    
    #self.createTrayIcon()
    # icon = QIcon(':/.ico')
    # self.trayIcon.setIcon(icon)
    # self.setWindowIcon(icon)
    # self.trayIcon.show()

    # self.setWindowFlags(Qt.WindowStaysOnTopHint)
    self.keyboardStatusWidget = KeyboardStatusWidget()
    mainLayout = QVBoxLayout()
    mainLayout.addWidget(self.keyboardStatusWidget)
    self.setLayout(mainLayout)
    
    self.setWindowTitle("Relay Keys Display")
    self.resize(400, 250)

  def createTrayIcon (self):
    self.trayIconMenu = QMenu(self)
    self.trayIconMenu.addAction(QAction("Quit", self, triggered=self.onQuit))
    #self.trayIconMenu.addSeparator()
    self.trayIcon = QSystemTrayIcon(self)
    self.trayIcon.setContextMenu(self.trayIconMenu)

  def onQuit (self):
    app.quit()
    # exit(0)
  
  def closeEvent(self, event):
    self._client_queue.put(("EXIT",))

  def initKeyboardHook (self):
    hm = PyHook3.HookManager()
    hm.KeyDown = self.onKeyboardDown
    hm.KeyUp = self.onKeyboardUp
    hm.HookKeyboard()
    self._hookmanager = hm
    #pythoncom.PumpMessages()

  def showErrorMessage (self, msg):
    QMessageBox.critical(None, "MorseWriter Error", msg)

  def client_worker (self, queue):
    while True:
      data = queue.get(True)
      if data[0] == "EXIT":
        break
      elif data[0] == "keyevent":
        if not self.do_keyevent(*data[1:]):
          # free the queue, to avoid multiple error messages
          try:
            while True:
              queue.get(False)
          except EmptyQueue:
            pass
  
  def do_keyevent (self, key, modifiers, isdown):
    try:
      ret = self.client.keyevent(key, modifiers, isdown)
      if 'result' not in ret:
        logging.error("keyevent ({}, {}, {}) response error: {}".format(key, modifiers, isdown, ret.get("error", "undefined")))
        self.showErrorMessageSignal.emit("Failed to send the message!")
      else:
        logging.info("keyevent ({}, {}, {}) response: {}".format(key, modifiers, isdown, ret["result"]))
        return True
    except:
      logging.error("keyevent ({}, {}, {}) raise: {}".format(key, modifiers, isdown, traceback.format_exc()))
      self.showErrorMessageSignal.emit("Failed to send the message!")
    return False
  
  def keyevent (self, key, modifiers, isdown):
    self._client_queue.put(("keyevent", key, modifiers, isdown))

  def _keyboardToggleCheck (self, key):
    mods = self._modifiers
    if ((self._toggle_key is None and len(self._toggle_modifiers) > 0) or \
        key == self._toggle_key) and \
        len(self._toggle_modifiers) == len(mods):
      match = True
      for mod in self._toggle_modifiers:
        if mod not in mods:
          match = False
          break
      if match:
        self._disabled = not self._disabled
        self.keyboardStatusWidget.updateStatusSignal.emit(["DISABLED"], [], [])
        return True
    return None
    
  def onKeyboardDown (self, event):
    key = keysmap.get(event.KeyID, None)
    mod = modifiers_map.get(event.KeyID, None)
    if key is not None:
      if key not in self._keys:
        self._keys.append(key)
    elif mod is not None:
      if mod not in self._modifiers:
        self._modifiers.append(mod)
    elif event.KeyID not in self._unknown_keys:
      self._unknown_keys.append(event.KeyID)
    ret = self._keyboardToggleCheck(key)
    if ret is not None:
      return ret
    if self._disabled:
      return True
    self.updateKeyboardState()
    if key is not None:
      self.keyevent(key, self._modifiers, True)
      return False
    elif mod is not None:
      # set the modifiers
      self.keyevent(None, self._modifiers, False)
      return False
    return True
  
  def onKeyboardUp (self, event):
    key = keysmap.get(event.KeyID, None)
    mod = modifiers_map.get(event.KeyID, None)
    if key is not None and key in self._keys:
      self._keys.remove(key)
    elif mod is not None and mod in self._modifiers:
      self._modifiers.remove(mod)
    else:
      try:
        self._unknown_keys.remove(event.KeyID)
      except:
        pass
    if self._disabled:
      return True
    self.updateKeyboardState()
    if key is not None:
      self.keyevent(key, self._modifiers, False)
      return False
    elif mod is not None:
      # set the modifiers
      self.keyevent(None, self._modifiers, False)
      return False
    return True

  def onUpdateKeyState (self):
    """This update event handler is used to update shown state of keyboard
    """
    self.keyboardStatusWidget.updateStatusSignal.emit(self._keys, self._modifiers, self._unknown_keys)
    
  def updateKeyboardState (self):
    if self._keystate_update_timer != None:
        self._keystate_update_timer.cancel()
    self._keystate_update_timer = Timer(0.05, self.onUpdateKeyState)
    self._keystate_update_timer.start()


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
  app = QApplication(argv)
  try:
    QApplication.setQuitOnLastWindowClosed(True)
    window = Window(args, config)
    window.show()
    return app.exec_()
  except:
    raise
    #QMessageBox.critical(None, "MorseWriter Fatal Error", "{}".format(traceback.format_exc()))
    #return 1

if __name__ == '__main__':
  ret = main()
  exit(ret)
