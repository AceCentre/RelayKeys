# -*- coding: utf-8 -*-
import os
from time import sleep, time
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
  (0x0D, "ENTER"), # VK_RETURN, ENTER
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

char_keysmap = dict([
  (65, ("a","A")),
  (66, ("b","B")),
  (67, ("c","C")),
  (68, ("d","D")),
  (69, ("e","E")),
  (70, ("f","F")),
  (71, ("g","G")),
  (72, ("h","H")),
  (73, ("i","I")),
  (74, ("j","J")),
  (75, ("k","K")),
  (76, ("l","L")),
  (77, ("m","M")),
  (78, ("n","N")),
  (79, ("o","O")),
  (80, ("p","P")),
  (81, ("q","Q")),
  (82, ("r","R")),
  (83, ("s","S")),
  (84, ("t","T")),
  (85, ("u","U")),
  (86, ("v","V")),
  (87, ("w","W")),
  (88, ("x","X")),
  (89, ("y","Y")),
  (90, ("z","Z")),
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
  (190, "."),
  (188, ","),
  (186, ";"),
  (0xBD, "-"), # VK_OEM_MINUS
  (187, "="),
  (191, "/"),
  (220, "\\"),
  (222, "'"),
  (219, ("[","{")),
  (221, ("]","}")),
  (13, ""), # "ENTER"
  (32, ""), # "SPACE"
  (8, ""), # "BACKSPACE"
  (9, ""), # "TAB"
  (445, "_"), # "UNDERSCORE"
  (0xC0, "~"), # Keyboard Non-US # and ~
  (0x0D, ""), # VK_RETURN, ENTER
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
    self._last_mouse_pos = None

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

    self.initHooks()

    #self.createTrayIcon()
    # icon = QIcon(':/.ico')
    # self.trayIcon.setIcon(icon)
    # self.setWindowIcon(icon)
    # self.trayIcon.show()

    # self.setWindowFlags(Qt.WindowStaysOnTopHint)
    self.keyboardStatusWidget = KeyboardStatusWidget()
    mainLayout = QVBoxLayout()
    mainLayout.addWidget(self.keyboardStatusWidget)

    try:
      self._show_last_n_chars = int(clientconfig.get("show_last_n_chars", "20"), 10)
    except ValueError:
      self._show_last_n_chars = 0

    if self._show_last_n_chars > 0:
      self._last_n_chars = []
      self._show_last_n_chars_label = QLabel()
      label = self._show_last_n_chars_label
      label.setContentsMargins(5, 5, 5, 5)
      label.setAlignment(Qt.AlignVCenter)
      label.setAutoFillBackground(True)
      p = label.palette()
      p.setColor(label.backgroundRole(), Qt.white)
      label.setPalette(p)
      fontsize = 10
      label.setText("<font style='font-weight:bold;' size='{fontsize}'>{text}</font>"
                   .format(text="", fontsize=fontsize))
      mainLayout.addWidget(label)

    self.setLayout(mainLayout)
    self.setContentsMargins(0, 0, 0, 0)

    self.setWindowTitle("Relay Keys Display")
    self.resize(400, 250)

  def updateShowLastChars (self):
    label = self._show_last_n_chars_label
    if label is None:
      return
    fontsize = 10
    text = " ".join(self._last_n_chars)
    label.setText("<font style='font-weight:bold;' size='{fontsize}'>{text}</font>"
                    .format(text=text, fontsize=fontsize))

  def createTrayIcon (self):
    self.trayIconMenu = QMenu(self)
    self.trayIconMenu.addAction(QAction("Quit", self, triggered=self.onQuit))
    #self.trayIconMenu.addSeparator()
    self.trayIcon = QSystemTrayIcon(self)
    self.trayIcon.setContextMenu(self.trayIconMenu)

  def onQuit (self):
    self._client_queue.put(("EXIT",))
    app.quit()
    # exit(0)
  
  def closeEvent(self, event):
    self._client_queue.put(("EXIT",))

  def initHooks (self):
    hm = PyHook3.HookManager()
    hm.KeyDown = self.onKeyboardDown
    hm.KeyUp = self.onKeyboardUp
    hm.HookKeyboard()
    hm.MouseAll = self.onMouseEvent
    hm.HookMouse()
    self._hookmanager = hm
    #pythoncom.PumpMessages()

  def showErrorMessage (self, msg):
    QMessageBox.critical(None, "RelayKeys Error", msg)
    self._disabled = True

  def client_worker (self, queue):
    lasttime = time()
    while True:
      ctime = time()
      sleeptime = 0.050 - (ctime - lasttime)
      if sleeptime > 0:
        sleep(sleeptime)
      lasttime = ctime
      inputlist = []
      try:
        while True:
          inputlist.append(queue.get(False))
      except EmptyQueue:
        if len(inputlist) == 0:
          continue
        have_exit = len(list(filter(lambda a: a[0] == 'EXIT', inputlist))) > 0
        if have_exit:
          break
        # expecting the rest are actions
        # merge mousemove actions
        mousemove_list = tuple(filter(lambda a: a[0] == 'mousemove', inputlist))
        if len(mousemove_list) > 1:
          inputlist = list(filter(lambda a: a[0] != 'mousemove', inputlist))
          mousemove = [ 'mousemove' ]
          for i in range(1, 5):
            mousemove.append(sum(map(lambda a: a[i] if len(a) > i else 0, mousemove_list)))
          inputlist.append(tuple(mousemove))
        # send actions
        if not self.client_send_actions(inputlist):
          # an error occurred, empty out the queue
          try:
            while True:
              queue.get(False)
          except EmptyQueue:
            pass


  def client_send_actions (self, actions):
    try:
      ret = self.client.actions(actions)
      if 'result' not in ret:
        logging.error("actions {} response error: {}".format(", ".join(map(str, actions)), ret.get("error", "undefined")))
        self.showErrorMessageSignal.emit("Failed to send the message!")
      else:
        logging.info("actions {} response: {}".format(", ".join(map(str, actions)), ret["result"]))
        return True
    except:
      logging.error("actions {} raise: {}".format(", ".join(map(str, actions)), traceback.format_exc()))
      self.showErrorMessageSignal.emit("Failed to send the message!")
    return False

  def client_send_action (self, action, *args):
    try:
      func = getattr(self.client, action, None)
      if func == None:
        raise ValueError("unknown action: {}".format(action))
      ret = func(*args)
      if 'result' not in ret:
        logging.error("{} ({}) response error: {}".format(action, ", ".join(map(str, args)), ret.get("error", "undefined")))
        self.showErrorMessageSignal.emit("Failed to send the message!")
      else:
        logging.info("{} ({}) response: {}".format(action, ", ".join(map(str, args)), ret["result"]))
        return True
    except:
      logging.error("{} ({}) raise: {}".format(action, ", ".join(map(str, args)), traceback.format_exc()))
      self.showErrorMessageSignal.emit("Failed to send the message!")
    return False
  
  def send_action (self, action, *args):
    self._client_queue.put((action,) + args)

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
      if self._show_last_n_chars > 0:
        chr = char_keysmap.get(event.KeyID, None)
        if chr is not None and len(chr) > 0:
          if isinstance(chr, (tuple)):
            chr = chr[0] if len(chr) == 1 or \
              ("LSHIFT" not in self._modifiers and "RSHIFT" not in self._modifiers) else chr[1]
          while len(self._last_n_chars) >= self._show_last_n_chars:
            self._last_n_chars.pop(0)
          self._last_n_chars.append(chr)
          self.updateShowLastChars()
      self.send_action('keyevent', key, self._modifiers, True)
      return False
    elif mod is not None:
      # set the modifiers
      self.send_action('keyevent', None, self._modifiers, False)
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
      self.send_action('keyevent', key, self._modifiers, False)
      return False
    elif mod is not None:
      # set the modifiers
      self.send_action('keyevent', None, self._modifiers, False)
      return False
    return True

  def onMouseEvent (self, event):
    if self._disabled:
      return True
    if event.Message == PyHook3.HookConstants.WM_MOUSEMOVE:
      if self._last_mouse_pos is None:
        self._last_mouse_pos = event.Position
        return True
      dx, dy = event.Position[0] - self._last_mouse_pos[0], event.Position[1] - self._last_mouse_pos[1]
      self.send_action('mousemove', dx, dy)
    elif event.Message == PyHook3.HookConstants.WM_LBUTTONDOWN:
      self.send_action('mousebutton', 'l', 'press')
    elif event.Message == PyHook3.HookConstants.WM_LBUTTONUP:
      self.send_action('mousebutton', '0')
    elif event.Message == PyHook3.HookConstants.WM_LBUTTONDBLCLK:
      self.send_action('mousebutton', 'l', 'doubleclick')
    elif event.Message == PyHook3.HookConstants.WM_RBUTTONDOWN:
      self.send_action('mousebutton', 'r', 'press')
    elif event.Message == PyHook3.HookConstants.WM_RBUTTONUP:
      self.send_action('mousebutton', '0')
    elif event.Message == PyHook3.HookConstants.WM_RBUTTONDBLCLK:
      self.send_action('mousebutton', 'r', 'doubleclick')
    elif event.Message == PyHook3.HookConstants.WM_MBUTTONDOWN:
      self.send_action('mousebutton', 'm', 'press')
    elif event.Message == PyHook3.HookConstants.WM_MBUTTONUP:
      self.send_action('mousebutton', '0')
    elif event.Message == PyHook3.HookConstants.WM_MBUTTONDBLCLK:
      self.send_action('mousebutton', 'm', 'doubleclick')
    elif event.Message == PyHook3.HookConstants.WM_MOUSEWHEEL:
      self.send_action('mousemove', 0, 0, event.Wheel)
    return False

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
    #QMessageBox.critical(None, "RelayKeys Fatal Error", "{}".format(traceback.format_exc()))
    #return 1

if __name__ == '__main__':
  ret = main()
  exit(ret)
