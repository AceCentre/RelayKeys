import operator
import logging
import time
from functools import reduce
from serial_wrappers import BLESerialWrapper
import asyncio

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
    ("KP_EQUAL", 0x67),  # Keypad =
    ("KP_COMMA", 0x85),  # Keypad Comma
    ("KP_EQSIGN", 0x86),  # Keypad Equal Sign
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
    ("APP", 0x65),  # Keyboard Application
    ("LCTRL", 0xE0),  # Keyboard Left Control
    ("LSHIFT", 0xE1),  # Keyboard Left Shift
    ("LALT", 0xE2),  # Keyboard Left Alt
    ("LGUI", 0xE3),  # Keyboard Left GUI
    ("RCTRL", 0xE4),  # Keyboard Right Control
    ("RSHIFT", 0xE5),  # Keyboard Right Shift
    ("RALT", 0xE6),  # Keyboard Right Alt
    ("RGUI", 0xE7),  # Keyboard Right GUI
    ("CUSTOM~", 0x32),  # Keyboard Non-US # and ~
    ("NONUSHASH", 0x32),  # Alias
    ("NONUSTILDE", 0x32),  # Alias
    ("NON-US-BACKSLASH", 0x64), # Non US backslash
    ("PRINTSCREEN", 0x46),  # Keyboard PrintScreen
    ("POWER", 0x66),  # Keyboard Power
    ("EXECUTE", 0x74),  # Keyboard Execute
    ("HELP", 0x75),  # Keyboard Help
    ("MENU", 0x76),  # Keyboard Menu
    ("SELECT", 0x77),  # Keyboard Select
    ("STOP", 0x78),  # Keyboard Stop
    ("AGAIN", 0x79),  # Keyboard Again
    ("UNDO", 0x7A),  # Keyboard Undo
    ("CUT", 0x7B),  # Keyboard Cut
    ("COPY", 0x7C),  # Keyboard Copy
    ("PASTE", 0x7D),  # Keyboard Paste
    ("FIND", 0x7E),  # Keyboard Find
    ("MUTE", 0x7F),  # Keyboard Mute
    ("VOLUP", 0x80),  # Keyboard Volume Up
    ("VOLDOWN", 0x81),  # Keyboard Volume Down
    ("LOCKING_CAPSLOCK", 0x82),  # Keyboard Locking Caps Lock
    ("LOCKING_NUMLOCK", 0x83),  # Keyboard Locking Num Lock
    ("LOCKING_SCROLLOCK", 0x84),  # Keyboard Locking Scroll Lock
    ("ALTERASE", 0x99),  # Keyboard Alternate Erase
    ("ATTENTION", 0x9A),  # Keyboard SysReq/Attention
    ("CANCEL", 0x9B),  # Keyboard Cancel
    ("CLEAR", 0x9C),  # Keyboard Clear
    ("PRIOR", 0x9D),  # Keyboard Prior
    ("RETURN", 0x9E),  # Keyboard Return
    ("SEPARATOR", 0x9F),  # Keyboard Separator
    ("OUT", 0xA0),  # Keyboard Out
    ("OPER", 0xA1),  # Keyboard Oper
])

async def _write_atcmd(ser, msg):
    if not isinstance(msg, bytes):
        msg = msg.encode()
    logging.debug("request: {}".format(
        msg if isinstance(msg, str) else str(msg, "utf8")))
    
    ser.flushInput()

    if isinstance(ser, BLESerialWrapper):
        await ser.write(msg + b"\r\n")
    else:
        await asyncio.gather(asyncio.to_thread(ser.write, (msg + b"\r\n")))
        

async def _read_response(ser, n=1):
    v = b""
    while n > 0:
        if isinstance(ser, BLESerialWrapper):
            v += await ser.readline()
        else:
            response = await asyncio.gather(asyncio.to_thread(ser.readline))            
            v += response[0]
        n -= 1
    msg = str(v, "utf8").strip()
    logging.debug("response: {}".format(msg))
    return msg


async def blehid_init_serial(ser):
    await _write_atcmd(ser, "AT")
    await _read_response(ser)
    # _write_atcmd(ser, "ATI")
    # _read_response(ser, n=8)
    await _write_atcmd(ser, "ATE=0")
    await _read_response(ser)
    await _write_atcmd(ser, "AT+BLEHIDEN=1")
    response = await _read_response(ser)
    if response.upper() == "ERROR":
        # running older framework < 0.6.6, fallback to enable keyboard
        await _write_atcmd(ser, "AT+BLEKEYBOARDEN=1")
        await _read_response(ser)
    await _write_atcmd(ser, "ATZ")
    await _read_response(ser)


MOUSE_MAX_MOVE = 2500


async def blehid_send_movemouse(ser, right, down, wheely, wheelx):
    right = max(-1 * MOUSE_MAX_MOVE,
                right) if right < 0 else min(MOUSE_MAX_MOVE, right)
    down = max(-1 * MOUSE_MAX_MOVE,
               down) if down < 0 else min(MOUSE_MAX_MOVE, down)
    wheely = max(-1 * MOUSE_MAX_MOVE,
                 wheely) if wheely < 0 else min(MOUSE_MAX_MOVE, wheely)
    wheelx = max(-1 * MOUSE_MAX_MOVE,
                 wheelx) if wheelx < 0 else min(MOUSE_MAX_MOVE, wheelx)
    while right != 0 or down != 0 or wheelx != 0 or wheely != 0:
        rmove = max(-128, min(right, 127))
        dmove = max(-128, min(down, 127))
        wymove = max(-128, min(wheely, 127))
        wxmove = max(-128, min(wheelx, 127))
        atcmd = "AT+BLEHIDMOUSEMOVE={},{},{},{}".format(
            rmove, dmove, wymove, wxmove)
        await _write_atcmd(ser, atcmd)
        await _read_response(ser)
        right -= rmove
        down -= dmove
        wheely -= wymove
        wheelx -= wxmove


async def blehid_send_mousebutton(ser, btn, behavior=None):
    atcmd = "AT+BLEHIDMOUSEBUTTON={}{}".format(
        btn, "" if behavior is None else "," + behavior)
    await _write_atcmd(ser, atcmd)
    await _read_response(ser)


async def blehid_send_keyboardcode(ser, key, modifiers, down, keys):
    logging.debug('key:'+str(key)+'  modifiers:'+str(modifiers))
    existingModifiers =  list(map(
            lambda a: a[0],
            filter(lambda a: a[1] in keys,
               [("LCTRL", 0xe0), ("LSHIFT", 0xe1), ("LALT", 0xe2),
                ("LMETA", 0xe3), ("RCTRL", 0xe4), ("RSHIFT", 0xe5),
                ("RALT", 0xe6), ("RMETA", 0xe7)])))
    modifiers=list(set(modifiers+existingModifiers))
    logging.debug('existing modifiers:'+str(existingModifiers))
    hidmod = reduce(operator.or_, map(
        lambda a: a[1],
        filter(lambda a: a[0] in modifiers,
               [("LCTRL", 0x01), ("LSHIFT", 0x02), ("LALT", 0x04),
                ("LMETA", 0x08), ("RCTRL", 0x10), ("RSHIFT", 0x20),
                ("RALT", 0x40), ("RMETA", 0x80)])), 0)
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
    atcmd += zerocmd
    await _write_atcmd(ser, atcmd)
    await _read_response(ser)


async def blehid_send_devicecommand(ser, devicecommand):
    logging.debug('device command:'+str(devicecommand))
    if devicecommand == 'drop-bonded-device':
        await _write_atcmd(ser, "AT+GAPDISCONNECT")
        await _read_response(ser)
        await _write_atcmd(ser, "AT+GAPDELBONDS")
        await _read_response(ser)
        logging.debug('Reset BT device')


async def blehid_send_switch_command(ser, devicecommand):
    logging.debug('device command:'+str(devicecommand))
    if devicecommand == 'switch':
        await _write_atcmd(ser, "AT+SWITCHCONN")
        await _read_response(ser)


async def blehid_send_get_device_name(ser, devicecommand):
    logging.debug('device command:'+str(devicecommand))
    if devicecommand == 'devname':
        await _write_atcmd(ser, "AT+BLECURRENTDEVICENAME")
        resp = await _read_response(ser, n=2)
        resp = resp.split('\n') #split('\r\n')
        try:
            return resp[1]
        except:
            pass
        return 'NONE'

async def blehid_send_add_device(ser, devicecommand):
    
    logging.debug('device command:'+str(devicecommand))

    await _write_atcmd(ser, "AT+BLEADDNEWDEVICE")

async def blehid_send_clear_device_list(ser, devicecommand):
    
    logging.debug('device command:'+str(devicecommand))

    await _write_atcmd(ser, "AT+RESETDEVLIST")

async def blehid_send_remove_device(ser, devicecommand):
    
    logging.debug('device command:'+"at+bleremovedevice\"" + devicecommand.split("=")[1] + "\"")

    await _write_atcmd(ser, "AT+BLEREMOVEDEVICE=\"" + devicecommand.split("=")[1] + "\"")

async def blehid_get_device_list(ser, devicecommand):

    logging.debug('device command:'+str(devicecommand))
    
    ser.flushInput()
    ser.flushOutput()

    await asyncio.sleep(0.1) #time.sleep(0.1)

    await _write_atcmd(ser, "AT+PRINTDEVLIST")

    """
    timeout = time.time() + 1    
    while True:
        if time.time() > timeout:
            break
    """
    await asyncio.sleep(1)
 
    data = ser.read_all()

    data = str(data, "utf8").strip().split('\n') #split('\r\n')

    logging.debug("response: {}".format(data))

    return data[1:]
