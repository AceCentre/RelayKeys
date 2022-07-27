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

from pynput import mouse, keyboard

from PyQt5.QtCore import pyqtSignal, Qt, pyqtSlot, QObject, QThread, QUrl, QTimer, QSize
from PyQt5.QtGui import QIcon, QDesktopServices, QPainter, QPixmap, QFont
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, \
    QVBoxLayout, QHBoxLayout, QGridLayout, QStackedLayout, \
    QMessageBox, QLabel, QAction, QMenu, QDialog, QAbstractButton, QPushButton, QFileDialog, QScrollArea, QFrame
    
from threading import Timer, Thread
from queue import Queue, Empty as EmptyQueue

import types

from pathlib import Path

# this import is only to support 'type' command in macrofiles
from cli_keymap import *
#import importlib
#relaykeys_cli = importlib.import_module("relaykeys-cli")

parser = argparse.ArgumentParser(description='Relay Keys qt client.')
parser.add_argument('--debug', dest='debug', action='store_const',
                    const=True, default=False,
                    help='set logger to debug level')
parser.add_argument('--config', '-c', dest='config',
                    default=None, help='Path to config file')
parser.add_argument('--url', '-u', dest='url', default=None,
                    help='rpc http url, default: http://127.0.0.1:5383/')

devList = []

macros_folder = str(Path(__file__).resolve().parent / "macros")

modifiers_map = dict([
    (keyboard.Key.ctrl_l, "LCTRL"),
    (keyboard.Key.ctrl_r, "RCTRL"),
    (keyboard.Key.shift_l, "LSHIFT"),
    (keyboard.Key.shift_r, "RSHIFT"),
    (keyboard.Key.alt_r, "RALT"),
    (keyboard.Key.alt_l, "LALT"),
    (keyboard.Key.cmd_l, "LMETA"),
    (keyboard.Key.cmd_r, "RMETA"),
])

keysmap_printable = dict([
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
    (0xBD, "MINUS"),  # VK_OEM_MINUS
    (187, "EQUALS"),
    (191, "SLASH"),
    (220, "BACKSLASH"),
    (222, "QUOTE"),
    (219, "LEFTBRACKET"),
    (221, "RIGHTBRACKET"),
    (445, "UNDERSCORE"),
    (0xC0, "BACKQUOTE"),  # Keyboard Non-US # and ~
    (0x60, "0"),  # VK_NUMPAD0 in numlock mode
    (0x61, "1"),  # VK_NUMPAD1 in numlock mode
    (0x62, "2"),  # VK_NUMPAD2 in numlock mode
    (0x63, "3"),  # VK_NUMPAD3 in numlock mode
    (0x64, "4"),  # VK_NUMPAD4 in numlock mode
    (0x65, "5"),  # VK_NUMPAD5 in numlock mode
    (0x66, "6"),  # VK_NUMPAD6 in numlock mode
    (0x67, "7"),  # VK_NUMPAD7 in numlock mode
    (0x68, "8"),  # VK_NUMPAD8 in numlock mode
    (0x69, "9"),  # VK_NUMPAD9 in numlock mode
    (0x6E, "PERIOD"),  # VK_DECIMAL in numlock mode# 
    (0x6A, "KP_MULTIPLY"),  # keypad multiply, VK_MULTIPLY
    (0x6F, "KP_DIVIDE"),  # keypad divide, VK_DIVIDE
    (0x6B, "KP_PLUS"),
    (0x6D, "KP_MINUS"),
    (12, "KP_5_DIS"),  # keypad 5 doesn't have any function when numlock disabled    
])

if os.name == 'posix':

	keysmap_non_printable = dict([
		(keyboard.Key.enter,  "ENTER"),
		(keyboard.Key.space,  "SPACE"),
		(keyboard.Key.backspace,  "BACKSPACE"),
		(keyboard.Key.tab,  "TAB"),
		(keyboard.Key.page_up,  "PAGEUP"),
		(keyboard.Key.page_down,  "PAGEDOWN"),
		(keyboard.Key.left,  "LEFTARROW"),
		(keyboard.Key.right,  "RIGHTARROW"),
		(keyboard.Key.up,  "UPARROW"),
		(keyboard.Key.down,  "DOWNARROW"),
		(keyboard.Key.esc,  "ESCAPE"),
		(keyboard.Key.home,  "HOME"),
		(keyboard.Key.end,  "END"), 
		(keyboard.Key.caps_lock,  "CAPSLOCK"),
		(keyboard.Key.f1, "F1"),
		(keyboard.Key.f2, "F2"),
		(keyboard.Key.f3, "F3"),
		(keyboard.Key.f4, "F4"),
		(keyboard.Key.f5, "F5"),
		(keyboard.Key.f6, "F6"),
		(keyboard.Key.f7, "F7"),
		(keyboard.Key.f8, "F8"),
		(keyboard.Key.f9, "F9"),
		(keyboard.Key.f10, "F10"),
		(keyboard.Key.f11, "F11"),
		(keyboard.Key.f12, "F12"),
		(keyboard.Key.media_volume_mute, "MUTE"),  # VK_VOLUME_MUTE
		(keyboard.Key.media_volume_up, "VOLUP"),  # VK_VOLUME_UP, Keyboard Volume Up
		(keyboard.Key.media_volume_down, "VOLDOWN"),  # VK_VOLUME_DOWN, Keyboard Volume Down
	])

else:

	keysmap_non_printable = dict([
		(keyboard.Key.enter,  "ENTER"),
		(keyboard.Key.space,  "SPACE"),
		(keyboard.Key.backspace,  "BACKSPACE"),
		(keyboard.Key.tab,  "TAB"),
		(keyboard.Key.page_up,  "PAGEUP"),
		(keyboard.Key.page_down,  "PAGEDOWN"),
		(keyboard.Key.left,  "LEFTARROW"),
		(keyboard.Key.right,  "RIGHTARROW"),
		(keyboard.Key.up,  "UPARROW"),
		(keyboard.Key.down,  "DOWNARROW"),
		(keyboard.Key.esc,  "ESCAPE"),
		(keyboard.Key.home,  "HOME"),
		(keyboard.Key.end,  "END"),
		(keyboard.Key.insert,  "INSERT"),
		(keyboard.Key.delete,  "DELETE"),
		#(keyboard.Key,  "APP"),  # Applications key
		(keyboard.Key.caps_lock,  "CAPSLOCK"),
		(keyboard.Key.num_lock,  "NUMLOCK"),
		(keyboard.Key.f1, "F1"),
		(keyboard.Key.f2, "F2"),
		(keyboard.Key.f3, "F3"),
		(keyboard.Key.f4, "F4"),
		(keyboard.Key.f5, "F5"),
		(keyboard.Key.f6, "F6"),
		(keyboard.Key.f7, "F7"),
		(keyboard.Key.f8, "F8"),
		(keyboard.Key.f9, "F9"),
		(keyboard.Key.f10, "F10"),
		(keyboard.Key.f11, "F11"),
		(keyboard.Key.f12, "F12"),
		(keyboard.Key.print_screen, "PRINTSCREEN"),  # Keyboard PrintScreen, VK_SNAPSHOT
		#(keyboard.Key., "EXECUTE"),  # VK_EXECUTE
		#(keyboard.Key., "HELP"),  # VK_HELP
		#(keyboard.Key., "MENU"),  # VK_MENU
		(keyboard.Key.pause, "PAUSE"),  # VK_PAUSE
		#(keyboard.Key., "SELECT"),  # VK_SELECT
		#(keyboard.Key., "STOP"),  # VK_MEDIA_STOP, Keyboard Stop
		(keyboard.Key.media_volume_mute, "MUTE"),  # VK_VOLUME_MUTE
		(keyboard.Key.media_volume_up, "VOLUP"),  # VK_VOLUME_UP, Keyboard Volume Up
		(keyboard.Key.media_volume_down, "VOLDOWN"),  # VK_VOLUME_DOWN, Keyboard Volume Down
		#(keyboard.Key., "CANCEL"),  # VK_CANCEL
		#(keyboard.Key., "CLEAR"),  # VK_CLEAR, Keyboard Clear
		#(keyboard.Key., "PRIOR"),  # VK_PRIOR, Keyboard Prior
		#(keyboard.Key., "ENTER"),  # VK_RETURN, ENTER
		#(keyboard.Key., "SEPARATOR"),  # VK_SEPARATOR
		#(keyboard.Key., "POWER"),  # VK_SLEEP
		#(keyboard.Key., "CANCEL")  # VK_CANCEL
	])

char_keysmap = dict([
    (65, ("a", "A")),
    (66, ("b", "B")),
    (67, ("c", "C")),
    (68, ("d", "D")),
    (69, ("e", "E")),
    (70, ("f", "F")),
    (71, ("g", "G")),
    (72, ("h", "H")),
    (73, ("i", "I")),
    (74, ("j", "J")),
    (75, ("k", "K")),
    (76, ("l", "L")),
    (77, ("m", "M")),
    (78, ("n", "N")),
    (79, ("o", "O")),
    (80, ("p", "P")),
    (81, ("q", "Q")),
    (82, ("r", "R")),
    (83, ("s", "S")),
    (84, ("t", "T")),
    (85, ("u", "U")),
    (86, ("v", "V")),
    (87, ("w", "W")),
    (88, ("x", "X")),
    (89, ("y", "Y")),
    (90, ("z", "Z")),
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
    (0xBD, "-"),  # VK_OEM_MINUS
    (187, "="),
    (191, "/"),
    (220, "\\"),
    (222, "'"),
    (219, ("[", "{")),
    (221, ("]", "}")),
    (13, ""),  # "ENTER"
    (32, ""),  # "SPACE"
    (8, ""),  # "BACKSPACE"
    (9, ""),  # "TAB"
    (445, "_"),  # "UNDERSCORE"
    (0xC0, "~"),  # Keyboard Non-US # and ~
    (0x0D, ""),  # VK_RETURN, ENTER
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

    def addPlusLabel(self):
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

    def onUpdateStatus(self, keys, modifiers, unknown_keys):
        def layout_del_inner(layout):
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

class DeviceEntryWidget(QFrame):
    def __init__(self, devname, deleteDeviceFunction):
        super(QFrame, self).__init__()
        self.setStyleSheet("background-color: rgb(255,255,255)")
        deviceEntryLayout = QHBoxLayout(self)        
        self.device_name = devname
        self.deleteDeviceFunction = deleteDeviceFunction

        deviceNameLabel = QLabel()        
        deviceNameLabel.setText("<font size='5'>{}</font>".format(self.device_name))

        # push button option
        deleteDeviceSwitch = QPushButton()
        deleteDeviceSwitch.setIcon(QIcon("resources/delete_icon.png"))
        deleteDeviceSwitch.setIconSize(QSize(35,35))
        deleteDeviceSwitch.setFlat(True)        
        deleteDeviceSwitch.clicked.connect(self.sendDeleteCommand)
        deleteDeviceSwitch.setFocusPolicy(Qt.NoFocus)

        deviceEntryLayout.addWidget(deviceNameLabel)
        deviceEntryLayout.addStretch()
        deviceEntryLayout.addWidget(deleteDeviceSwitch)
    
    def sendDeleteCommand(self):
        self.deleteDeviceFunction(self.device_name)

class DeviceListWidget(QFrame):
    def __init__(self, deleteDeviceFunction):
        super(QFrame, self).__init__()        

        self.deviceListLayout = QVBoxLayout(self)

        self.deviceWidgetsList = []
        self.deleteDeviceFunction = deleteDeviceFunction

        self.setStyleSheet("DeviceEntryWidget {border: 2px solid}")

    def addDevice(self, devname):
        deviceEntry = DeviceEntryWidget(devname, self.deleteDeviceFunction)
        self.deviceWidgetsList.append(deviceEntry)

        self.deviceListLayout.insertWidget(len(self.deviceWidgetsList)-1, deviceEntry)
        
        if self.deviceListLayout.count() == 1:
            self.deviceListLayout.addStretch()
    
    def clearList(self):
        while self.deviceListLayout.count():
            item = self.deviceListLayout.takeAt(0)
            widget = item.widget()
            print(item)
            if widget is not None:
                widget.deleteLater()
        self.deviceWidgetsList = []

class Window (QMainWindow):
    showErrorMessageSignal = pyqtSignal(str)    
    addDeviceListSignal = pyqtSignal(str)
    clearDeviceListSignal = pyqtSignal()
    switchDeviceSignal = pyqtSignal()
    toggleRecordSignal = pyqtSignal()
    setDongleLabelSignal = pyqtSignal(str)
    setDaemonLabelSignal = pyqtSignal(str)
    updateDeviceLabelSignal = pyqtSignal(str)

    def __init__(self, args, config):
        self.devList = []
        super(Window, self).__init__()
        clientconfig = config["client"]

        self.setStyleSheet("QPushButton {font: 18px}")
        self.app_obj = QApplication.instance()
        
        self.showErrorMessageSignal.connect(self.showErrorMessage)
        self._keyboard_disabled = False
        self._mouse_disabled = True
        self._keystate_update_timer = None
        self._keys = []
        self._modifiers = []
        self._unknown_keys = []
        self._keyboard_toggle_key = clientconfig.get("keyboard_togglekey", "A")
        self._keyboard_toggle_modifiers = clientconfig.get(
            "keyboard_togglemods", "LALT").split(",")
        self._mouse_toggle_key = clientconfig.get("mouse_togglekey", "S")
        self._mouse_toggle_modifiers = clientconfig.get(
            "mouse_togglemods", "LALT").split(",")
        self._last_mouse_pos = None
        self._last_mouse_calltime = 0
        self._curBleDeviceName = '---'
        self._macroBuffer = []
        self._recordMacroStatus = False

        self.daemon_mode = ""
        self.dongle_status = ""

        url = clientconfig.get("url", None) if args.url == None else args.url
        host = clientconfig.get("host", None)
        port = clientconfig.get("port", None)
        if url is None and not (host is None and port is None):
            self.client = RelayKeysClient(host=host, port=port,
                                          username=clientconfig.get(
                                              "username", None),
                                          password=clientconfig.get("password", None))
        else:
            if url is None:
                url = "http://127.0.0.1:5383/"
            self.client = RelayKeysClient(url=url)
        
        # loading ketmap for supporting type command in macros
        if "cli" not in config.sections():
            config["cli"] = {}  
        if not load_keymap_file(config["cli"]):
            return

        self._client_queue = Queue(64)
        t = Thread(target=self.client_worker, args=(self._client_queue,))
        t.start()

        self.initHooks()

        # self.createTrayIcon()
        # icon = QIcon(':/.ico')
        # self.trayIcon.setIcon(icon)
        # self.setWindowIcon(icon)
        # self.trayIcon.show()

        # self.setWindowFlags(Qt.WindowStaysOnTopHint)

        # dock layout for switching tabs
        dockWidget = QWidget()
        dockLayout = QVBoxLayout(dockWidget)
        dockLayout.setContentsMargins(0, 0, 0, 0)
        dockWidget.setStyleSheet("QPushButton {min-width: 100px; min-height: 100px;}")

        capturePageSwtich = QPushButton()
        capturePageSwtich.setText('Capture')
        capturePageSwtich.clicked.connect(lambda: self.switchTab(0))
        capturePageSwtich.setFocusPolicy(Qt.NoFocus)
        
        macroPageSwtich = QPushButton()
        macroPageSwtich.setText('Macro')
        macroPageSwtich.clicked.connect(lambda: self.switchTab(1))        
        macroPageSwtich.setFocusPolicy(Qt.NoFocus)
        
        connectionPageSwtich = QPushButton()
        connectionPageSwtich.setText('Connection')
        connectionPageSwtich.clicked.connect(lambda: self.switchTab(2))        
        connectionPageSwtich.setFocusPolicy(Qt.NoFocus)
        
        devicePageSwtich = QPushButton()
        devicePageSwtich.setText('Devices')
        devicePageSwtich.clicked.connect(lambda: self.switchTab(3))        
        devicePageSwtich.setFocusPolicy(Qt.NoFocus)

        dockLayout.addWidget(capturePageSwtich)
        dockLayout.addWidget(macroPageSwtich)
        dockLayout.addWidget(connectionPageSwtich)
        dockLayout.addWidget(devicePageSwtich)
        dockLayout.addStretch()        

        # Capture tab
        captureTab = QWidget()        
        captureTabLayout = QVBoxLayout(captureTab)

        captureTab.setStyleSheet("QPushButton {min-width: 250px; min-height: 50px;}")

        self.deviceNameCaptureTab = QLabel()
        # mouse and keyboard controls layout
        inputControlBar = QGridLayout()
        
        # keyboard section        
        self.keyboardControlLabel = QLabel()
        
        keyboardToggleButton = QPushButton()        
        keyboardToggleButton.setText('Toggle: {}'.format(self.getShortcutText(
            self._keyboard_toggle_key, self._keyboard_toggle_modifiers)))
        keyboardToggleButton.setToolTip('Keyboard disable toggle')
        keyboardToggleButton.clicked.connect(self.didClickKeyboardToggle)
        keyboardToggleButton.setFocusPolicy(Qt.NoFocus)       

        # mouse section
        self.mouseControlLabel = QLabel()

        mouseToggleButton = QPushButton()
        mouseToggleButton.setText('Toggle: {}'.format(
            self.getShortcutText(self._mouse_toggle_key, self._mouse_toggle_modifiers)))
        mouseToggleButton.setToolTip('Mouse disable toggle')        
        mouseToggleButton.clicked.connect(self.didClickMouseToggle)
        mouseToggleButton.setFocusPolicy(Qt.NoFocus)

        self.updateTogglesStatus()

        inputControlBar.addWidget(self.keyboardControlLabel, 0, 0)
        inputControlBar.addWidget(self.mouseControlLabel, 0, 1)
        inputControlBar.addWidget(keyboardToggleButton, 1, 0)        
        inputControlBar.addWidget(mouseToggleButton, 1, 1)
        
        captureTabLayout.addWidget(self.deviceNameCaptureTab)
        captureTabLayout.addLayout(inputControlBar)        
        

        self.keyboardStatusWidget = KeyboardStatusWidget()
        captureTabLayout.addWidget(self.keyboardStatusWidget)

        try:
            self._show_last_n_chars = int(
                clientconfig.get("show_last_n_chars", "20"), 10)
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
            captureTabLayout.addWidget(label)             

        # macro controls tab
        macroTab = QWidget()
        macroTabLayout = QVBoxLayout(macroTab)
        macroTab.setStyleSheet("QPushButton {min-width: 250px; min-height: 50px;}")
        
        self.macroRecordSwitch = QPushButton()
        self.macroRecordSwitch.setText('Start recording macro')
        self.macroRecordSwitch.setToolTip('Start recording new macro')
        self.macroRecordSwitch.clicked.connect(self.toggleMacroRecord)
        self.macroRecordSwitch.setFocusPolicy(Qt.NoFocus)
        
        replayMacroSwitch = QPushButton()
        replayMacroSwitch.setText('Replay last macro')
        replayMacroSwitch.setToolTip('Replay last macro')
        replayMacroSwitch.clicked.connect(self.replayLastMacro)
        replayMacroSwitch.setFocusPolicy(Qt.NoFocus)
        
        executeMacroSwitch = QPushButton()
        executeMacroSwitch.setText('Run macro file')
        executeMacroSwitch.setToolTip('Run macro file')
        executeMacroSwitch.clicked.connect(self.loadMacroFile)
        executeMacroSwitch.setFocusPolicy(Qt.NoFocus)
                
        self.macroStatusLabel = QLabel()
        self.macroStatusLabel.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.updateMacroStatusLabel("Idle")

        self.toggleRecordSignal.connect(self.toggleMacroRecord)

        macroTabLayout.addWidget(self.macroRecordSwitch)
        macroTabLayout.addWidget(replayMacroSwitch)
        macroTabLayout.addWidget(executeMacroSwitch)
        macroTabLayout.addWidget(self.macroStatusLabel)

        #connection tab
        connectionTab = QWidget()
        connectionTabLayout = QVBoxLayout(connectionTab)

        connectionTab.setStyleSheet("QPushButton {min-width: 250px; min-height: 50px;}")

        # device controls section
        bleControlBar = QGridLayout()

        self.deviceNameConnTab = QLabel()   
        
        self.updateDeviceLabelSignal.connect(self.updateDeviceNameLabel)
        self.updateDeviceNameLabel(self._curBleDeviceName)
        self.deviceNameConnTab.setAlignment(Qt.AlignBottom)

        
        bleConnectionSwitch = QPushButton()
        bleConnectionSwitch.setText('Switch device')
        bleConnectionSwitch.setToolTip('Swicth ble device connection')
        bleConnectionSwitch.clicked.connect(self.sendBleToggleCommand)
        bleConnectionSwitch.setFocusPolicy(Qt.NoFocus)

        self.switchDeviceSignal.connect(self.sendBleToggleCommand)        
       
        bleControlBar.addWidget(self.deviceNameConnTab, 0, 0, 1, 2)
        bleControlBar.addWidget(bleConnectionSwitch, 1, 0)

        # daemon controls section
        daemonControlBar = QGridLayout()

        self.daemonStatusLabel = QLabel()
        self.dongleStatusLabel = QLabel()

        self.setDaemonLabelSignal.connect(self.daemonStatusLabel.setText)
        self.setDongleLabelSignal.connect(self.dongleStatusLabel.setText)
        

        daemonControlBar.addWidget(self.daemonStatusLabel, 0, 0)
        daemonControlBar.addWidget(self.dongleStatusLabel, 0, 1)

        daemonModeSwitch = QPushButton()
        daemonModeSwitch.setText('Switch mode')
        daemonModeSwitch.setToolTip('Switch daemon mode')
        daemonModeSwitch.clicked.connect(self.switchDaemonMode)
        daemonModeSwitch.setFocusPolicy(Qt.NoFocus)
        daemonControlBar.addWidget(daemonModeSwitch, 1, 0)        

        self.updateStatusTimer = QTimer()
        self.updateStatusTimer.timeout.connect(self.updateStatusCallback)
        self.updateStatusTimer.setInterval(5000)
        self.updateStatusTimer.start()

        self.updateStatusCallback()
      
        connectionTabLayout.addLayout(bleControlBar)
        connectionTabLayout.addLayout(daemonControlBar)
        connectionTabLayout.addStretch()

        # devices tab
        devicesTab = QWidget()
        devicesTabLayout = QHBoxLayout(devicesTab)

        devicesTab.setStyleSheet("QPushButton {min-width: 100px; min-height: 50px;}")

        # device list custom widget
        self.deviceList = DeviceListWidget(self.removeDeviceCommand)
        self.addDeviceListSignal.connect(self.deviceList.addDevice)
        self.clearDeviceListSignal.connect(self.deviceList.clearList)

        scrollAreaContainer = QScrollArea()
        scrollAreaContainer.setFrameStyle(QFrame.WinPanel | QFrame.Sunken)
        scrollAreaContainer.setLineWidth(3)        
        scrollAreaContainer.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollAreaContainer.setWidget(self.deviceList)
        scrollAreaContainer.setWidgetResizable(True)

        # device controls Bar
        deviceControlsBar = QVBoxLayout()

        addDeviceSwitch = QPushButton()
        addDeviceSwitch.setText('Add device')
        addDeviceSwitch.setToolTip('Add new device to list')
        addDeviceSwitch.clicked.connect(self.addDeviceButtonClicked)
        addDeviceSwitch.setFocusPolicy(Qt.NoFocus)

        refreshListSwitch = QPushButton()
        refreshListSwitch.setText('Refresh list')
        refreshListSwitch.setToolTip('Refresh devices list')
        refreshListSwitch.clicked.connect(self.refreshDeviceListButtonClicked)
        refreshListSwitch.setFocusPolicy(Qt.NoFocus)

        resetListSwitch = QPushButton()
        resetListSwitch.setText('Reset device list')
        resetListSwitch.setToolTip('Remove all devices from list')
        resetListSwitch.clicked.connect(self.resetDeviceListButtonClicked)
        resetListSwitch.setFocusPolicy(Qt.NoFocus)
        
        deviceControlsBar.addWidget(addDeviceSwitch)
        deviceControlsBar.addWidget(refreshListSwitch)
        deviceControlsBar.addWidget(resetListSwitch)
        deviceControlsBar.addStretch()

        devicesTabLayout.addWidget(scrollAreaContainer)
        devicesTabLayout.addLayout(deviceControlsBar)

        # layout for displaying tabs
        self.tabLayout = QStackedLayout()
        self.tabLayout.addWidget(captureTab)
        self.tabLayout.addWidget(macroTab)
        self.tabLayout.addWidget(connectionTab)
        self.tabLayout.addWidget(devicesTab)

        mainWidget = QWidget(self)        
        mainLayout = QHBoxLayout(mainWidget)
        mainLayout.addWidget(dockWidget)
        mainLayout.addLayout(self.tabLayout)  

        self.setCentralWidget(mainWidget)

        self.setContentsMargins(0, 0, 0, 0)

        self.setWindowTitle("Relay Keys Display")
        self.resize(625, 435)

        # Help Menu
        userMenu = self.menuBar()        
        helpMenu = userMenu.addMenu("&Help") 

        helpMenuGitHubDoc = QAction("Git Hub Docs", self)
        helpMenuGitHubDoc.triggered.connect(self.openGitHubUrl)
        helpMenu.addAction(helpMenuGitHubDoc)

        helpMenuAceCentre = QAction("Ace Centre", self)
        helpMenuAceCentre.triggered.connect(self.openAceCentreUrl)
        helpMenu.addAction(helpMenuAceCentre)
        
        self.send_action('ble_cmd', 'devname')
        self.send_action('ble_cmd', 'devlist')

    def didShowWindow(self):
        pass

    @pyqtSlot()
    def switchTab(self, tab_index):
        self.tabLayout.setCurrentIndex(tab_index)

    @pyqtSlot()
    def readBleDeviceName(self):
        self.send_action('ble_cmd', 'devname')

    @pyqtSlot()
    def sendBleToggleCommand(self):
        self.send_action('ble_cmd', 'switch')

    @pyqtSlot()
    def didClickKeyboardToggle(self):
        self._keyboard_disabled = not self._keyboard_disabled
        self.keyboardStatusWidget.updateStatusSignal.emit([], [], [])
        self.updateTogglesStatus()

    @pyqtSlot()
    def didClickMouseToggle(self):
        self._mouse_disabled = not self._mouse_disabled
        self.updateTogglesStatus()

    @pyqtSlot()
    def toggleMacroRecord(self):
        self._recordMacroStatus = not self._recordMacroStatus
        if self._recordMacroStatus:
            self.updateMacroStatusLabel("Recording new macro")
            self.macroRecordSwitch.setText('Stop recording macro')
            self._macroBuffer = []
        else:
            self.macroRecordSwitch.setText('Start recording macro')
            self.saveMacro()
            self.updateMacroStatusLabel("Idle")

    @pyqtSlot()
    def replayLastMacro(self):
        if self._recordMacroStatus or len(self._macroBuffer) == 0:
            return

        # remember previous states and disable sending keyboard and mouse actions while executing macro
        keyboard_state_tmp = self._keyboard_disabled    
        mouse_state_tmp = self._mouse_disabled
        self._keyboard_disabled = True
        self._mouse_disabled = True

        self.updateMacroStatusLabel("Replaying last macro")
        self.app_obj.processEvents()
        self.executeMacroBuffer()
        self.updateMacroStatusLabel("Idle")

        # return previous states
        self._keyboard_disabled = keyboard_state_tmp
        self._mouse_disabled = mouse_state_tmp

    @pyqtSlot()
    def loadMacroFile(self):
        if self._recordMacroStatus:
            return

        # remember previous states and disable sending keyboard and mouse actions while executing macro
        keyboard_state_tmp = self._keyboard_disabled    
        mouse_state_tmp = self._mouse_disabled
        self._keyboard_disabled = True
        self._mouse_disabled = True

        file_path = QFileDialog.getOpenFileName(self, 'Open File', macros_folder, "Text files (*.txt)")[0]
        file_name = file_path[file_path.rfind('/')+1:]

        if file_path != '':            
            self._macroBuffer = []
            with open(file_path, "r") as file:
                for line in file.readlines():
                    cmd = line.strip("\n")
                    if cmd == "":
                        continue
                    else:
                        self._macroBuffer.append(cmd)
            
            self.updateMacroStatusLabel("Running {}".format(file_name))
            self.app_obj.processEvents()
            self.executeMacroBuffer()
            self.updateMacroStatusLabel("Idle")
            
        
        # return previous states
        self._keyboard_disabled = keyboard_state_tmp
        self._mouse_disabled = mouse_state_tmp

    @pyqtSlot()
    def switchDaemonMode(self):
        self.client_send_action("daemon", "switch_mode")
        self.updateStatusCallback()

    @pyqtSlot()
    def updateStatusCallback(self):        
        self.send_action("daemon", "get_mode")
        self.send_action("daemon", "dongle_status")
        self.send_action('ble_cmd', 'devname')

    def getShortcutText(self, key, modifiers):
        return " + ".join((key, ) + tuple(modifiers))

    def updateMacroStatusLabel(self, text):
        self.macroStatusLabel.setText("<font size='5' style='font-weight:bold;'>Macro status: </font><font size='5'>{}</font>".format(text))

    def updateDeviceNameLabel(self, text):
        self.deviceNameCaptureTab.setText("<font size='5' style='font-weight:bold;'>Cur Device: </font><font size='5'>{}</font>".format(text))
        self.deviceNameConnTab.setText("<font size='5' style='font-weight:bold;'>Cur Device: </font><font size='5'>{}</font>".format(text))

    #Menu Functions

    def openGitHubUrl(self):
        url = QUrl('https://acecentre.github.io/RelayKeys/')
        if not QDesktopServices.openUrl(url):
            QMessageBox.warning(self, 'Open Url', 'Could not open url')

    def openAceCentreUrl(self):
        url = QUrl('https://acecentre.org.uk/')
        if not QDesktopServices.openUrl(url):
            QMessageBox.warning(self, 'Open Url', 'Could not open url')
        
    def resetDeviceListButtonClicked(self):
        self.send_action('ble_cmd', 'devreset')

    def refreshDeviceListButtonClicked(self):
        self.send_action('ble_cmd', 'devlist')

    def removeDeviceButtonClicked(self):
        action = self.sender()
        self.send_action('ble_cmd', 'devremove=' + action.text()[2:])
    
    def removeDeviceCommand(self, devname):
        self.send_action('ble_cmd', 'devremove=' + devname[2:])

    def addDeviceUpdateDialog(self, found):

        self.send_action('ble_cmd', 'devlist')

        if self.oldDevList != self.devList and len(self.devList):
            self.BLEStatusLabel.setText("New Device Added") 
            
            self.addBLEDeviceOK.setEnabled(True)
            self.workerBLE.stop()
            self.BLEthread.quit()
            self.BLEthread.wait()
            self.send_action('ble_cmd', 'devname')

        if self.addBLEDialog.isVisible() == False:
            self.workerBLE.stop()
            self.BLEthread.quit()
            self.BLEthread.wait()
            self.send_action('ble_cmd', 'devname')

    def addDeviceButtonClicked(self):

        class BLEWorker(QObject):
            finished = pyqtSignal()
            progress = pyqtSignal(int)
            def __init__(self):
                super(BLEWorker, self).__init__()
                self._isRunning = True

            def run(self):
                
                while self._isRunning:
                    sleep(1)
                    self.progress.emit(2)

            def stop(self):
                self._isRunning = False

        self.send_action('ble_cmd', 'devadd')

        self.oldDevList = self.devList
        self.devList = []        

        self.addBLEDialog = QDialog(self)
        
        self.addBLEDialog.setWindowTitle("Add New BLE Device")

        self.BLElayout = QVBoxLayout()

        self.BLEStatusLabel = QLabel()
        self.BLElayout.addWidget(self.BLEStatusLabel)

        bleControlBar = QHBoxLayout()

        self.addBLEDeviceOK = QPushButton()
        self.addBLEDeviceOK.setText("OK")
        self.addBLEDeviceOK.clicked.connect(self.addBLEDialog.accept)

        self.addBLEDeviceCancel = QPushButton()
        self.addBLEDeviceCancel.setText("Cancel")
        self.addBLEDeviceCancel.clicked.connect(self.addBLEDialog.reject)
        
        bleControlBar.addWidget(self.addBLEDeviceOK)
        bleControlBar.addWidget(self.addBLEDeviceCancel)

        self.BLElayout.addLayout(bleControlBar)

        self.BLEStatusLabel.setText("Waiting for device...")

        self.addBLEDialog.setLayout(self.BLElayout)

        self.addBLEDialog.resize(400, 125)

        self.BLEthread = QThread()
        self.workerBLE = BLEWorker()
        
        self.workerBLE.moveToThread(self.BLEthread)

        self.BLEthread.started.connect(self.workerBLE.run)
        self.workerBLE.finished.connect(self.BLEthread.quit)
        self.workerBLE.finished.connect(self.workerBLE.deleteLater)
        self.BLEthread.finished.connect(self.BLEthread.deleteLater)
        self.workerBLE.progress.connect(self.addDeviceUpdateDialog)
        
        self.addBLEDeviceOK.setEnabled(False)

        self.BLEthread.start()
        
        self.BLEthread.finished.connect(
            lambda: self.addBLEDeviceOK.setEnabled(True)
        )

        self.addBLEDialog.exec()

    def updateTogglesStatus(self):
        fontsize = 5
        self.keyboardControlLabel.setText("<font style='color: {color}; font-weight:bold;' size='{fontsize}'>{text}</font>"
                                          .format(text="Keyboard Disabled" if self._keyboard_disabled else "Keyboard Enabled", fontsize=fontsize,
                                                  color="#777" if self._keyboard_disabled else "#222"))
        self.mouseControlLabel.setText("<font style='color: {color}; font-weight:bold;' size='{fontsize}'>{text}</font>"
                                       .format(text="Mouse Disabled" if self._mouse_disabled else "Mouse Enabled", fontsize=fontsize,
                                               color="#777" if self._mouse_disabled else "#222"))

    def updateShowLastChars(self):
        label = self._show_last_n_chars_label
        if label is None:
            return
        fontsize = 10
        text = " ".join(self._last_n_chars)
        label.setText("<font style='font-weight:bold;' size='{fontsize}'>{text}</font>"
                      .format(text=text, fontsize=fontsize))
    
    """
    def createTrayIcon(self):
        self.trayIconMenu = QMenu(self)
        self.trayIconMenu.addAction(
            QAction("Quit", self, triggered=self.onQuit))
        # self.trayIconMenu.addSeparator()
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)
    """

    """
    def onQuit(self):
        self._client_queue.put(("EXIT",))
        self._keyboard_listener.stop()
        self._mouse_listener.stop()
        app.quit()
        # exit(0)
    """

    def closeEvent(self, event):
        self._client_queue.put(("EXIT",))
        self._keyboard_listener.stop()
        self._mouse_listener.stop()

    def initHooks(self):
        self._keyboard_listener = keyboard.Listener(on_press=self.onKeyboardDown, on_release=self.onKeyboardUp)
        self._keyboard_listener.start()
        self._mouse_listener = mouse.Listener(on_move=self.mouse_on_move, on_click=self.mouse_on_click, on_scroll=self.mouse_on_scroll)
        self._mouse_listener.start()

    def showErrorMessage(self, msg):
        QMessageBox.critical(None, "RelayKeys Error", msg)
        self._keyboard_disabled = True

    def client_worker(self, queue):
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
                    queue.task_done()
            except EmptyQueue:
                if len(inputlist) == 0:
                    continue
                have_exit = len(
                    list(filter(lambda a: a[0] == 'EXIT', inputlist))) > 0
                if have_exit:
                    break
                # expecting the rest are actions
                # merge mousemove actions
                mousemove_list = tuple(
                    filter(lambda a: a[0] == 'mousemove', inputlist))
                if len(mousemove_list) > 1:
                    inputlist = list(
                        filter(lambda a: a[0] != 'mousemove', inputlist))
                    mousemove = ['mousemove']
                    for i in range(1, 5):
                        mousemove.append(
                            sum(map(lambda a: a[i] if len(a) > i else 0, mousemove_list)))
                    inputlist.append(tuple(mousemove))
                # send actions
                if not self.client_send_actions(inputlist):
                    # an error occurred, empty out the queue
                    try:
                        while True:
                            queue.get(False)
                            queue.task_done()
                    except EmptyQueue:
                        pass

    def client_send_actions(self, actions):
        try:
            filtred_actions = []

            for action in actions:
                if action[0] == "ble_cmd":
                    ble_cmd_ret = self.client_send_action("ble_cmd", action[1])
                    if ble_cmd_ret == False or  ble_cmd_ret == "FAIL" or ble_cmd_ret == "TIMEOUT" or ble_cmd_ret == "No connection with dongle":
                        continue        

                    if action[1] == "devname":
                        self._curBleDeviceName = ble_cmd_ret
                        self.updateDeviceLabelSignal.emit(self._curBleDeviceName)
                    elif action[1] == "devlist":
                        self.clearDeviceListSignal.emit()
                        self.devList = []                                                        
                        for device in ble_cmd_ret:
                            if 'Device found in list - ' not in device \
                                and 'Disconnected - Device already present in list' not in device \
                                and 'ERROR:' not in device \
                                and 'OK' not in device \
                                and 'SUCCESS' not in device:
                                self.addDeviceListSignal.emit(device)
                                self.devList.append(device)
                    elif action[1] == "devreset":
                            self.clearDeviceListSignal.emit()
                            self.devList = []                    
                    elif 'devremove' in action[1]:                        
                        self.send_action('ble_cmd', 'devlist')
                        self.send_action('ble_cmd', 'devname')
                    

                elif action[0] == "daemon":                    
                    daemon_ret = self.client_send_action("daemon", action[1])
                    if daemon_ret == False or daemon_ret == "FAIL" or daemon_ret == "TIMEOUT" or daemon_ret == "No connection with dongle":
                        continue                    
                    
                    if action[1] == "get_mode":
                        self.daemon_mode = daemon_ret
                        self.setDaemonLabelSignal.emit("<font size='5' style='font-weight:bold;'>Daemon: </font><font size='5'>{0}.</font>".format(self.daemon_mode))                        
                    elif action[1] == "dongle_status":
                        self.dongle_status = daemon_ret                        
                        self.setDongleLabelSignal.emit("<font size='5' style='font-weight:bold;'>Dongle: </font><font size='5'>{0}.</font>".format(self.dongle_status))                        
                        if self.dongle_status != "Connected":
                            self._curBleDeviceName = "NONE"
                            self.updateDeviceLabelSignal.emit(self._curBleDeviceName)
            
                else:
                    filtred_actions.append(action)

            if len(filtred_actions) == 0:
                return True
                            
            ret = self.client.actions(filtred_actions)
            if 'result' not in ret:
                logging.error("actions {} response error: {}".format(
                    ", ".join(map(str, actions)), ret.get("error", "undefined")))
                self.showErrorMessageSignal.emit("Failed to send the message!")
            else:
                if ret["result"] == "FAIL" or ret["result"] == "TIMEOUT" or ret["result"] == "No connection with dongle":
                    return False               

                logging.info("actions {} response: {}".format(
                    ", ".join(map(str, filtred_actions)), ret["result"]))
                return True
        except:
            logging.error("actions {} raise: {}".format(
                ", ".join(map(str, actions)), traceback.format_exc()))
            self.showErrorMessageSignal.emit("Failed to send the message!")
        return False

    def client_send_action(self, action, *args):
        try:
            func = getattr(self.client, action, None)
            if func == None:
                raise ValueError("unknown action: {}".format(action))
            ret = func(*args)
            if 'result' not in ret:
                logging.error("{} ({}) response error: {}".format(
                    action, ", ".join(map(str, args)), ret.get("error", "undefined")))
                # self.showErrorMessageSignal.emit("Failed to send the message!")
            else:
                logging.info("{} ({}) response: {}".format(
                    action, ", ".join(map(str, args)), ret["result"]))
                return ret["result"]
        except:
            logging.error("{} ({}) raise: {}".format(
                action, ", ".join(map(str, args)), traceback.format_exc()))
            # self.showErrorMessageSignal.emit("Failed to send the message!")
        return False

    def send_action(self, action, *args):
        # capture actions if recording
        if self._recordMacroStatus:            
            self.appendMacroCommand(action, args)

        self._client_queue.put((action,) + args)

    def checkShortcutTrigger(self, key, mods, tkey, tmods):
        match = False
        if ((tkey is None and len(tmods) > 0) or key == tkey) and \
                len(tmods) == len(mods):
            match = True
            for tmod in tmods:
                if tmod not in mods:
                    match = False
                    break
            return match

    def _keyboardToggleCheck(self, key):
        if self.checkShortcutTrigger(key, self._modifiers, self._keyboard_toggle_key, self._keyboard_toggle_modifiers):
            self._keyboard_disabled = not self._keyboard_disabled
            self.keyboardStatusWidget.updateStatusSignal.emit([], [], [])
            self.updateTogglesStatus()
            return False
        elif self.checkShortcutTrigger(key, self._modifiers, self._mouse_toggle_key, self._mouse_toggle_modifiers):
            self._mouse_disabled = not self._mouse_disabled
            self.updateTogglesStatus()
            return False
        return None

    def onKeyboardDown(self, key_ev):
        key = None
        mod = None
        if(isinstance(key_ev, keyboard.KeyCode)):            
            key = keysmap_printable.get(key_ev.vk, None)            
        else:           
           key = keysmap_non_printable.get(key_ev, None)
           mod = modifiers_map.get(key_ev, None)

        if key is not None:
            if key not in self._keys:
                self._keys.append(key)
        elif mod is not None:
            if mod not in self._modifiers:
                self._modifiers.append(mod)
        elif key_ev not in self._unknown_keys:
            self._unknown_keys.append(key_ev)

        # check shortcuts combinations
        if len(self._keys) != 0 and len(self._modifiers) != 0:
            if self._modifiers[0] == "LSHIFT" and self._keys[0] == "ESCAPE":                
                self.toggleRecordSignal.emit()
                return
            if self._modifiers[0] == "LALT" and self._keys[0] == "N":                
                self.switchDeviceSignal.emit()
                return
        
        ret = self._keyboardToggleCheck(key)
        if ret is not None:
            return
        if self._keyboard_disabled:
            return

        self.updateKeyboardState()
        if key is not None:
            if isinstance(key_ev, keyboard.KeyCode) and self._show_last_n_chars > 0:
                chr = char_keysmap.get(key_ev.vk, None)
                if chr is not None and len(chr) > 0:
                    if isinstance(chr, (tuple)):
                        chr = chr[0] if len(chr) == 1 or \
                            ("LSHIFT" not in self._modifiers and "RSHIFT" not in self._modifiers) else chr[1]
                    while len(self._last_n_chars) >= self._show_last_n_chars:
                        self._last_n_chars.pop(0)
                    self._last_n_chars.append(chr)
                    self.updateShowLastChars()
            self.send_action('keyevent', key, self._modifiers, True)            
        elif mod is not None:
            # set the modifiers
            self.send_action('keyevent', None, self._modifiers, False)            

    def onKeyboardUp(self, key_ev):
        key = None
        mod = None
        if(isinstance(key_ev, keyboard.KeyCode)):            
            key = keysmap_printable.get(key_ev.vk, None)
        else:           
           key = keysmap_non_printable.get(key_ev, None)
           mod = modifiers_map.get(key_ev, None)

        if key is not None and key in self._keys:
            self._keys.remove(key)
        elif mod is not None and mod in self._modifiers:
            self._modifiers.remove(mod)
        else:
            try:
                self._unknown_keys.remove(key_ev)
            except:
                pass
        if self._keyboard_disabled:
            return
        self.updateKeyboardState()
        if key is not None:
            self.send_action('keyevent', key, self._modifiers, False)            
        elif mod is not None:
            # set the modifiers
            self.send_action('keyevent', None, self._modifiers, False)        

    def mouse_on_move(self, x, y):        
        if not self._mouse_disabled:
            if self._last_mouse_pos is None:
                self._last_mouse_pos = [x, y]                
                return True
            if time() - self._last_mouse_calltime >0.100:
                dx = x - self._last_mouse_pos[0]
                dy = y - self._last_mouse_pos[1]

                self.send_action('mousemove', dx, dy)
                self._last_mouse_pos = [x, y]

                self._last_mouse_calltime = time()
    
    def mouse_on_click(self, x, y, button, pressed):
        if not self._mouse_disabled:
            if button == mouse.Button.left and pressed:
                self.send_action('mousebutton', 'l', 'press')
            elif button == mouse.Button.left and not pressed:
                self.send_action('mousebutton', '0')
            #elif event.Message == PyHook3.HookConstants.WM_LBUTTONDBLCLK:
            #    self.send_action('mousebutton', 'l', 'doubleclick')                
            elif button == mouse.Button.right and pressed:
                self.send_action('mousebutton', 'r', 'press')
            elif button == mouse.Button.right and not pressed:
                self.send_action('mousebutton', '0')
            #elif event.Message == PyHook3.HookConstants.WM_RBUTTONDBLCLK:
            #    self.send_action('mousebutton', 'r', 'doubleclick')
            elif button == mouse.Button.middle and pressed:
                self.send_action('mousebutton', 'm', 'press')
            elif button == mouse.Button.middle and not pressed:
                self.send_action('mousebutton', '0')
            #elif event.Message == PyHook3.HookConstants.WM_MBUTTONDBLCLK:
            #    self.send_action('mousebutton', 'm', 'doubleclick')
    
    def mouse_on_scroll(self, x, y, dx, dy):        
        if not self._mouse_disabled:
            self.send_action('mousemove', 0, 0, dy, dx)

    def onUpdateKeyState(self):
        """This update event handler is used to update shown state of keyboard
        """
        self.keyboardStatusWidget.updateStatusSignal.emit(
            self._keys, self._modifiers, self._unknown_keys)

    def updateKeyboardState(self):
        if self._keystate_update_timer != None:
            self._keystate_update_timer.cancel()
        self._keystate_update_timer = Timer(0.05, self.onUpdateKeyState)
        self._keystate_update_timer.start()


    def appendMacroCommand(self, action, args):        
        recorded_cmd = action + ":"
        if action == "keyevent":
            recorded_cmd += str(args[0]) + ","
            if len(args[1])==0:
                recorded_cmd += "None,"
            else:
                recorded_cmd += ",".join(args[1]) + ","
            recorded_cmd += str(int(args[2]))
        elif action == "mousemove":
            for arg in args:
                recorded_cmd += str(arg) + ","
            recorded_cmd = recorded_cmd[0:-1]
        elif action == "mousebutton":
            recorded_cmd += ",".join(args)
        else:
            return
        
        self._macroBuffer.append(recorded_cmd)
    
    def saveMacro(self):
        if len(self._macroBuffer) == 0:
            return
        
        # remember previous states and disable sending keyboard and mouse actions while saving
        keyboard_state_tmp = self._keyboard_disabled    
        mouse_state_tmp = self._mouse_disabled
        self._keyboard_disabled = True
        self._mouse_disabled = True

        file_path = QFileDialog.getSaveFileName(self, 'Save File', macros_folder, "Text files (*.txt)")[0]
        if file_path != '':
            with open(file_path, "w") as file:            
                for line in self._macroBuffer:
                    file.write(line)
                    file.write('\n')
        
        
        # return previous states
        self._keyboard_disabled = keyboard_state_tmp
        self._mouse_disabled = mouse_state_tmp

    def executeMacroBuffer(self):        
        for command in self._macroBuffer:
            parts = command.split(":")
            cmd_type = parts[0]
            cmd_args = parts[1].split(",")
            
            if cmd_type == "keyevent":
                key = cmd_args[0]
                modifiers = []                
                if cmd_args[1] != "None":
                    modifiers = cmd_args[1:-1]
                event = bool(int(cmd_args[-1]))
                
                self.send_action("keyevent", key, modifiers, event)
            elif cmd_type == "keypress":
                #print("keypress args", cmd_args) #temp
                key = cmd_args[0]
                modifiers = []                
                if len(cmd_args) > 1:
                    modifiers = cmd_args[1:]
                
                self.send_action("keyevent", key, modifiers, True)
                sleep(0.05)
                self.send_action("keyevent", key, modifiers, False)

            elif cmd_type == "mousemove":
                if len(cmd_args) == 4:                
                    self.send_action("mousemove", int(cmd_args[0]), int(cmd_args[1]), int(cmd_args[2]), int(cmd_args[3]))
                else:
                    self.send_action("mousemove", int(cmd_args[0]), int(cmd_args[1]))
            elif cmd_type == "mousebutton":
                if len(cmd_args) == 2:                
                    self.send_action("mousebutton", cmd_args[0], cmd_args[1])
                else:
                    self.send_action("mousebutton", cmd_args[0])
            elif cmd_type == "delay":
                delay_value = float(cmd_args[0])
                sleep(delay_value/1000.0)
            elif cmd_type == "type":
                #print("got type command: ", cmd_args[0]) #temp
                for char in cmd_args[0]:
                    type_key, type_mods = char_to_keyevent_params(char)
                    
                    self.send_action("keyevent", type_key, type_mods, True)
                    sleep(0.05)
                    self.send_action("keyevent", type_key, type_mods, False)
                    sleep(0.05)
                pass
            else:
                continue

            sleep(0.05)



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
        config.read([
            os.path.expanduser('~/.relaykeys.cfg'),
            os.path.join(dirname, 'relaykeys.cfg'),
        ])
    else:
        config.read([args.config])
    if "client" not in config.sections():
        config["client"] = {}
    app = QApplication(sys.argv)
    try:
        QApplication.setQuitOnLastWindowClosed(True)
        window = Window(args, config)
        window.show()
        window.didShowWindow()
        return app.exec_()
    except:
        raise
        #QMessageBox.critical(None, "RelayKeys Fatal Error", "{}".format(traceback.format_exc()))
        # return 1
if __name__ == '__main__':
    ret = main()
    exit(ret)
