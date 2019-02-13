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
  ("MENU", 0x76), # Keyboard Menu
  ("APP", 0x65), # Keyboard Application
  ("LGUI", 0xE3), # Keyboard Left GUI
  ("RGUI", 0xE7), # Keyboard Right GUI
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
