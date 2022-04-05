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

from PyQt5.QtCore import pyqtSignal, Qt, pyqtSlot, QObject, QThread, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QApplication, QSystemTrayIcon, \
    QMessageBox, QLabel, QAction, QMenu, QMenuBar, QDialog, QPushButton, QMainWindow
    
from threading import Timer, Thread
from queue import Queue, Empty as EmptyQueue

parser = argparse.ArgumentParser(description='Relay Keys qt client.')
parser.add_argument('--debug', dest='debug', action='store_const',
                    const=True, default=False,
                    help='set logger to debug level')
parser.add_argument('--config', '-c', dest='config',
                    default=None, help='Path to config file')
parser.add_argument('--url', '-u', dest='url', default=None,
                    help='rpc http url, default: http://127.0.0.1:5383/')

devList = []

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
    (0x60, "KP_0"),  # VK_NUMPAD0
    (0x61, "KP_1"),  # VK_NUMPAD1
    (0x62, "KP_2"),  # VK_NUMPAD2
    (0x63, "KP_3"),  # VK_NUMPAD3
    (0x64, "KP_4"),  # VK_NUMPAD4
    (0x65, "KP_5"),  # VK_NUMPAD5
    (0x66, "KP_6"),  # VK_NUMPAD6
    (0x67, "KP_7"),  # VK_NUMPAD7
    (0x68, "KP_8"),  # VK_NUMPAD8
    (0x69, "KP_9"),  # VK_NUMPAD9
    (0x6E, "KP_PERIOD"),  # VK_DECIMAL
    (0x6A, "KP_MULTIPLY"),  # keypad multiply, VK_MULTIPLY
    (0x6F, "KP_DIVIDE"),  # keypad divide, VK_DIVIDE
    (0x6B, "KP_PLUS"),
    (0x6D, "KP_MINUS"),    
])

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

class Window (QMainWindow):
    showErrorMessageSignal = pyqtSignal(str)

    def __init__(self, args, config):
        self.devList = []
        super(Window, self).__init__()
        clientconfig = config["client"]

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
        mainLayout = QVBoxLayout()

        controlBar = QHBoxLayout()

        keyboardControlSect = QVBoxLayout()
        self.keyboardControlLabel = QLabel()
        keyboardControlSect.addWidget(self.keyboardControlLabel)
        self.keyboardToggleButton = QPushButton()
        self.keyboardToggleButton.setText('Toggle: {}'.format(self.getShortcutText(
            self._keyboard_toggle_key, self._keyboard_toggle_modifiers)))
        self.keyboardToggleButton.setToolTip('Keyboard disable toggle')
        self.keyboardToggleButton.clicked.connect(self.didClickKeyboardToggle)
        self.keyboardToggleButton.setFocusPolicy(Qt.NoFocus)
        keyboardControlSect.addWidget(self.keyboardToggleButton)

        mouseControlSect = QVBoxLayout()
        self.mouseControlLabel = QLabel()
        mouseControlSect.addWidget(self.mouseControlLabel)
        self.mouseToggleButton = QPushButton()
        self.mouseToggleButton.setText('Toggle: {}'.format(
            self.getShortcutText(self._mouse_toggle_key, self._mouse_toggle_modifiers)))
        self.mouseToggleButton.setToolTip('Mouse disable toggle')        
        self.mouseToggleButton.clicked.connect(self.didClickMouseToggle)
        self.mouseToggleButton.setFocusPolicy(Qt.NoFocus)
        mouseControlSect.addWidget(self.mouseToggleButton)

        bleControlBar = QHBoxLayout()
        self.bleConnectionSwitch = QPushButton()
        self.bleConnectionSwitch.setText('BLE Switch')
        self.bleConnectionSwitch.setToolTip('swicth ble device connection')
        self.bleConnectionSwitch.clicked.connect(self.sendBleToggleCommand)
        self.bleConnectionSwitch.setFocusPolicy(Qt.NoFocus)
        self.bleDeviceRead = QPushButton()
        self.bleDeviceRead.setText('Cur Device: {}'.format(self._curBleDeviceName))
        self.bleDeviceRead.setToolTip('swicth ble device connection')
        self.bleDeviceRead.clicked.connect(self.readBleDeviceName)
        self.bleDeviceRead.setFocusPolicy(Qt.NoFocus)
        bleControlBar.addWidget(self.bleConnectionSwitch)
        bleControlBar.addWidget(self.bleDeviceRead)

        self.updateTogglesStatus()
        controlBar.addLayout(keyboardControlSect)
        controlBar.addLayout(mouseControlSect)
        mainLayout.addLayout(controlBar)
        mainLayout.addLayout(bleControlBar)

        self.keyboardStatusWidget = KeyboardStatusWidget()
        mainLayout.addWidget(self.keyboardStatusWidget)

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
            mainLayout.addWidget(label)
        
        widget = QWidget(self)
        self.setCentralWidget(widget)
        layout = QVBoxLayout()
        layout.addLayout(mainLayout)

        widget.setLayout(layout)

        self.setContentsMargins(0, 0, 0, 0)

        self.setWindowTitle("Relay Keys Display")
        self.resize(400, 250)

        # New Menu
        self.userMenu = self.menuBar()

        # Device Menu
        self.deviceMenu = QMenu("&Devices", self)
        
        self.actionAddNewDevice = QAction("Add BLE Device", self)
        self.actionAddNewDevice.triggered.connect(self.addDeviceButtonClicked)

        self.deviceMenu.addAction(self.actionAddNewDevice)

        self.removeDeviceMenu = QMenu("&Remove BLE Device", self)

        self.actionResetDevices = QAction("Reset BLE Device List", self)
        self.actionResetDevices.triggered.connect(self.resetDeviceListButtonClicked)
        self.removeDeviceMenu.addAction(self.actionResetDevices)   
        
        self.removeDeviceMenu.addSeparator()

        self.deviceMenu.addMenu(self.removeDeviceMenu)

        self.actionRefreshDevices = QAction("Refresh Device List", self)
        self.actionRefreshDevices.triggered.connect(self.refreshDeviceListButtonClicked)
        self.deviceMenu.addAction(self.actionRefreshDevices)

        self.userMenu.addMenu(self.deviceMenu)

        # Help Menu
        self.helpMenu = self.userMenu.addMenu("&Help") 

        self.helpMenuGitHubDoc = QAction("Git Hub Docs", self)
        self.helpMenuGitHubDoc.triggered.connect(self.openGitHubUrl)
        self.helpMenu.addAction(self.helpMenuGitHubDoc)

        self.helpMenuAceCentre = QAction("Ace Centre", self)
        self.helpMenuAceCentre.triggered.connect(self.openAceCentreUrl)
        self.helpMenu.addAction(self.helpMenuAceCentre)
        
        self.send_action('ble_cmd', 'devname')
        self.send_action('ble_cmd', 'devlist')

    def didShowWindow(self):
        pass

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

    def getShortcutText(self, key, modifiers):
        return " + ".join((key, ) + tuple(modifiers))

    #Menu Functions

    def openGitHubUrl(self):
        url = QUrl('https://acecentre.github.io/RelayKeys/')
        if not QDesktopServices.openUrl(url):
            QMessageBox.warning(self, 'Open Url', 'Could not open url')

    def openAceCentreUrl(self):
        url = QUrl('https://acecentre.org.uk/')
        if not QDesktopServices.openUrl(url):
            QMessageBox.warning(self, 'Open Url', 'Could not open url')
    
    def clearRemoveDeviceMenu(self):
        
        self.removeDeviceMenu.clear()

        self.actionResetDevices = QAction("Reset BLE Device List", self)
        self.actionResetDevices.triggered.connect(self.resetDeviceListButtonClicked)
        self.removeDeviceMenu.addAction(self.actionResetDevices)   
        
        self.removeDeviceMenu.addSeparator()

    def resetDeviceListButtonClicked(self):
        self.send_action('ble_cmd', 'devreset')

    def refreshDeviceListButtonClicked(self):

        self.send_action('ble_cmd', 'devlist')

    def removeDeviceButtonClicked(self):
        action = self.sender()
        self.send_action('ble_cmd', 'devremove|' + action.text()[2:])

    def addDeviceUpdateDialog(self, found):

        self.send_action('ble_cmd', 'devlist')

        if self.oldDevList != self.devList and len(self.devList):
            self.BLEStatusLabel.setText("New Device Added") 
            
            self.addBLEDeviceOK.setEnabled(True)
            self.workerBLE.stop()
            self.BLEthread.quit()
            self.BLEthread.wait()

        if self.addBLEDialog.isVisible() == False:
            self.workerBLE.stop()
            self.BLEthread.quit()
            self.BLEthread.wait()

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

    def createTrayIcon(self):
        self.trayIconMenu = QMenu(self)
        self.trayIconMenu.addAction(
            QAction("Quit", self, triggered=self.onQuit))
        # self.trayIconMenu.addSeparator()
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)

    def onQuit(self):
        self._client_queue.put(("EXIT",))
        self._keyboard_listener.stop()
        self._keyboard_listener.stop()
        app.quit()
        # exit(0)

    def closeEvent(self, event):
        self._client_queue.put(("EXIT",))

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
            ret = self.client.actions(actions)
            if 'result' not in ret:
                logging.error("actions {} response error: {}".format(
                    ", ".join(map(str, actions)), ret.get("error", "undefined")))
                self.showErrorMessageSignal.emit("Failed to send the message!")
            else:
                
                result = 0

                for action in actions:
                
                    if action[0] == 'ble_cmd':
                        if action[1] == 'devname':
                            self._curBleDeviceName = ret['result'][result]
                            self.bleDeviceRead.setText(
                                'Cur Device: {}'.format(self._curBleDeviceName))
                
                        if action[1] == 'devlist':
                            
                            self.clearRemoveDeviceMenu()
                            self.devList = []
                                                            
                            for device in ret['result'][result]:
                                if 'Device found in list - ' not in device \
                                    and 'Disconnected - Device already present in list' not in device \
                                    and 'ERROR:' not in device \
                                    and 'OK' not in device \
                                    and 'SUCCESS' not in device:
        
                                    self.removeDeviceMenu.addAction(device, self.removeDeviceButtonClicked)

                                    self.devList.append(device)
                                    
                        if action[1] == 'devreset':
                            self.clearRemoveDeviceMenu()
                            self.devList = []

                        if 'devremove' in action[1]:
                            self.send_action('ble_cmd', 'devlist')

                    result = result + 1

                logging.info("actions {} response: {}".format(
                    ", ".join(map(str, actions)), ret["result"]))
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
                return True
        except:
            logging.error("{} ({}) raise: {}".format(
                action, ", ".join(map(str, args)), traceback.format_exc()))
            # self.showErrorMessageSignal.emit("Failed to send the message!")
        return False

    def send_action(self, action, *args):
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
            print(key)
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
