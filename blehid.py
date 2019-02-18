import operator
import logging
from time import sleep
from functools import reduce

# keys source http://www.freebsddiary.org/APC/usb_hid_usages.php
keymap = dict([
  ("BACKSPACE", 0x2a),
  ("ENTER", 0x28),
  ("TAB", 0x2b),
  ("PAUSE", 0x48),
  ("ESCAPE", 0x29),
  ("SPACE", 0x2c),
  ("QUOTE", 0x34),
  ("COMMA", 0x36),
  ("MINUS", 0x2d),
  ("PERIOD", 0x37),
  ("SLASH", 0x38),
  ("0", 0x27),
  ("1", 0x1e),
  ("2", 0x1f),
  ("3", 0x20),
  ("4", 0x21),
  ("5", 0x22),
  ("6", 0x23),
  ("7", 0x24),
  ("8", 0x25),
  ("9", 0x26),
  ("SEMICOLON", 0x33),
  ("EQUALS", 0x2e),
  ("LEFTBRACKET", 0x2f),
  ("BACKSLASH", 0x31),
  ("RIGHTBRACKET", 0x30),
  ("BACKQUOTE", 0x35),
  ("A", 0x04),
  ("B", 0x05),
  ("C", 0x06),
  ("D", 0x07),
  ("E", 0x08),
  ("F", 0x09),
  ("G", 0x0a),
  ("H", 0x0b),
  ("I", 0x0c),
  ("J", 0x0d),
  ("K", 0x0e),
  ("L", 0x0f),
  ("M", 0x10),
  ("N", 0x11),
  ("O", 0x12),
  ("P", 0x13),
  ("Q", 0x14),
  ("R", 0x15),
  ("S", 0x16),
  ("T", 0x17),
  ("U", 0x18),
  ("V", 0x19),
  ("W", 0x1a),
  ("X", 0x1b),
  ("Y", 0x1c),
  ("Z", 0x1d),
  ("DELETE", 0x4c),
  ("KP0", 0x62),
  ("KP1", 0x59),
  ("KP2", 0x5a),
  ("KP3", 0x5b),
  ("KP4", 0x5c),
  ("KP5", 0x5d),
  ("KP6", 0x5e),
  ("KP7", 0x5f),
  ("KP8", 0x60),
  ("KP9", 0x61),
  ("KP_PERIOD", 0x63),
  ("KP_DIVIDE", 0x54),
  ("KP_MULTIPLY", 0x55),
  ("KP_MINUS", 0x56),
  ("KP_PLUS", 0x57),
  ("KP_ENTER", 0x58),
  ("KP_EQUAL", 0x67), # Keypad =
  ("KP_COMMA", 0x85), # Keypad Comma
  ("KP_EQSIGN", 0x86), # Keypad Equal Sign
  ("UP", 0x52),
  ("DOWN", 0x51),
  ("RIGHT", 0x4f),
  ("LEFT", 0x50),
  ("INSERT", 0x49),
  ("HOME", 0x4a),
  ("END", 0x4d),
  ("PAGEUP", 0x4b),
  ("PAGEDOWN", 0x4e),
  ("F1", 0x3a),
  ("F2", 0x3b),
  ("F3", 0x3c),
  ("F4", 0x3d),
  ("F5", 0x3e),
  ("F6", 0x3f),
  ("F7", 0x40),
  ("F8", 0x41),
  ("F9", 0x42),
  ("F10", 0x43),
  ("F11", 0x44),
  ("F12", 0x45),
  ("NUMLOCK", 0x53),
  ("CAPSLOCK", 0x39),
  ("SCROLLOCK", 0x47),
  ("RIGHTARROW", 0x4F),
  ("LEFTARROW", 0x50),
  ("DOWNARROW", 0x51),
  ("UPARROW", 0x52),
  ("APP", 0x65), # Keyboard Application
  ("LGUI", 0xE3), # Keyboard Left GUI
  ("RGUI", 0xE7), # Keyboard Right GUI
  ("CUSTOM~", 0x32), # Keyboard Non-US # and ~
  ("PRINTSCREEN", 0x46), # Keyboard PrintScreen
  ("POWER", 0x66), # Keyboard Power
  ("EXECUTE", 0x74), # Keyboard Execute
  ("HELP", 0x75), # Keyboard Help
  ("MENU", 0x76), # Keyboard Menu
  ("SELECT", 0x77), # Keyboard Select
  ("STOP", 0x78), # Keyboard Stop
  ("AGAIN", 0x79), # Keyboard Again
  ("UNDO", 0x7A), # Keyboard Undo
  ("CUT", 0x7B), # Keyboard Cut
  ("COPY", 0x7C), # Keyboard Copy
  ("PASTE", 0x7D), # Keyboard Paste
  ("FIND", 0x7E), # Keyboard Find
  ("MUTE", 0x7F), # Keyboard Mute
  ("VOLUP", 0x80), # Keyboard Volume Up
  ("VOLDOWN", 0x81), # Keyboard Volume Down
  ("LOCKING_CAPSLOCK", 0x82), # Keyboard Locking Caps Lock
  ("LOCKING_NUMLOCK", 0x83), # Keyboard Locking Num Lock
  ("LOCKING_SCROLLOCK", 0x84), # Keyboard Locking Scroll Lock
  ("ALTERASE", 0x99), # Keyboard Alternate Erase
  ("ATTENTION", 0x9A), # Keyboard SysReq/Attention
  ("CANCEL", 0x9B), # Keyboard Cancel
  ("CLEAR", 0x9C), # Keyboard Clear
  ("PRIOR", 0x9D), # Keyboard Prior
  ("RETURN", 0x9E), # Keyboard Return
  ("SEPARATOR", 0x9F), # Keyboard Separator
  ("OUT", 0xA0), # Keyboard Out
  ("OPER", 0xA1), # Keyboard Oper
])

def blehid_init_serial (ser):
  # TODO check for OK or ERROR
  ser.write("AT\r".encode())
  sleep(1)
  ser.flushInput()
  # ser.write("ATI\r".encode())
  # time.sleep(1)
  ser.write("ATE=0\r".encode())
  sleep(1)
  ser.flushInput()
  ser.write("AT+BLEHIDEN=1\r".encode())
  sleep(1)
  ser.flushInput()
  ser.write("ATZ\r".encode())


def blehid_send_movemouse (ser, right, down):
  atcmd = "AT+BLEHIDMOUSEMOVE={},{}\r".format(right, down)
  logging.debug('atcmd:'+ atcmd)
  ser.write(atcmd.encode())

def blehid_send_mousebutton (ser, btn, behavior=None):
  atcmd = "AT+BLEHIDMOUSEBUTTON={}{}\r".format(btn, "" if behavior is None else "," + behavior)
  logging.debug('atcmd:' + atcmd)
  ser.write(atcmd.encode())

def blehid_send_keyboardcode (ser, key, modifiers, down, keys):
    logging.debug('key:'+str(key)+'  modifiers:'+str(modifiers))
    hidmod = reduce(operator.or_, map(
      lambda a: a[1],
      filter(lambda a: a[0] in modifiers,
             [ ("LCTRL", 0x01), ("LSHIFT", 0x02), ("LALT", 0x04),
               ("LMETA", 0x08), ("RCTRL", 0x10), ("RSHIFT", 0x20),
               ("RALT", 0x40), ("RMETA", 0x80) ])), 0)
    keycode = keymap.get(key, 0)
    # if OS == 'ios' and keycode == 13:
    #    hidcode = 0x58
    logging.debug("keycode: {:02x}, mod: {:02x}".format(keycode, hidmod))
    if key != 0:
      for i in range(0, 6):
          if keys[i] == 0:
              if down == True:
                  keys[i] = keycode
                  break
          elif keys[i] == keycode:
              if down == False:
                  keys[i] = 0
              else:
                  break
    atcmd = "AT+BLEKEYBOARDCODE={:02x}-00".format(hidmod)
    zerocmd = ""
    for i in range(0, 6):
        if keys[i] != 0:
            atcmd += "-{:02x}".format(keys[i])
        else:
            zerocmd += "-00"
    atcmd += zerocmd + "\r"
    logging.debug('atcmd:'+ atcmd)
    ser.write(atcmd.encode());

def blehid_send_devicecommand(ser, devicecommand):
    logging.debug('device command:'+str(devicecommand))
    if devicecommand == 'drop-bonded-device':
        ser.write("AT+GAPDISCONNECT\r".encode())
        ser.write("AT+GAPDELBONDS\r".encode())
        logging.debug('Reset BT device')
