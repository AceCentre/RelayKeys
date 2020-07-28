import pygame
from pygame.locals import *
from relaykeysclient import RelayKeysClient

url = "http://localhost:5383/"
client = RelayKeysClient(url=url)

keysmap = dict([
  (pygame.K_BACKSPACE, "BACKSPACE"),
  (pygame.K_TAB, "TAB"),
  (pygame.K_CLEAR, "CLEAR"),
  (pygame.K_RETURN, "RETURN"),
  (pygame.K_PAUSE, "PAUSE"),
  (pygame.K_ESCAPE, "ESCAPE"),
  (pygame.K_SPACE, "SPACE"),
  (pygame.K_EXCLAIM, "EXCLAIM"),
  (pygame.K_QUOTEDBL, "QUOTEDBL"),
  (pygame.K_HASH, "HASH"),
  (pygame.K_DOLLAR, "DOLLAR"),
  (pygame.K_AMPERSAND, "AMPERSAND"),
  (pygame.K_QUOTE, "QUOTE"),
  (pygame.K_LEFTPAREN, "LEFTPAREN"),
  (pygame.K_RIGHTPAREN, "RIGHTPAREN"),
  (pygame.K_ASTERISK, "ASTERISK"),
  (pygame.K_PLUS, "PLUS"),
  (pygame.K_COMMA, "COMMA"),
  (pygame.K_MINUS, "MINUS"),
  (pygame.K_PERIOD, "PERIOD"),
  (pygame.K_SLASH, "SLASH"),
  (pygame.K_0, "0"),
  (pygame.K_1, "1"),
  (pygame.K_2, "2"),
  (pygame.K_3, "3"),
  (pygame.K_4, "4"),
  (pygame.K_5, "5"),
  (pygame.K_6, "6"),
  (pygame.K_7, "7"),
  (pygame.K_8, "8"),
  (pygame.K_9, "9"),
  (pygame.K_COLON, "COLON"),
  (pygame.K_SEMICOLON, "SEMICOLON"),
  (pygame.K_LESS, "LESS"),
  (pygame.K_EQUALS, "EQUALS"),
  (pygame.K_GREATER, "GREATER"),
  (pygame.K_QUESTION, "QUESTION"),
  (pygame.K_AT, "AT"),
  (pygame.K_LEFTBRACKET, "LEFTBRACKET"),
  (pygame.K_BACKSLASH, "BACKSLASH"),
  (pygame.K_RIGHTBRACKET, "RIGHTBRACKET"),
  (pygame.K_CARET, "CARET"),
  (pygame.K_UNDERSCORE, "UNDERSCORE"),
  (pygame.K_BACKQUOTE, "BACKQUOTE"),
  (pygame.K_a, "A"),
  (pygame.K_b, "B"),
  (pygame.K_c, "C"),
  (pygame.K_d, "D"),
  (pygame.K_e, "E"),
  (pygame.K_f, "F"),
  (pygame.K_g, "G"),
  (pygame.K_h, "H"),
  (pygame.K_i, "I"),
  (pygame.K_j, "J"),
  (pygame.K_k, "K"),
  (pygame.K_l, "L"),
  (pygame.K_m, "M"),
  (pygame.K_n, "N"),
  (pygame.K_o, "O"),
  (pygame.K_p, "P"),
  (pygame.K_q, "Q"),
  (pygame.K_r, "R"),
  (pygame.K_s, "S"),
  (pygame.K_t, "T"),
  (pygame.K_u, "U"),
  (pygame.K_v, "V"),
  (pygame.K_w, "W"),
  (pygame.K_x, "X"),
  (pygame.K_y, "Y"),
  (pygame.K_z, "Z"),
  (pygame.K_DELETE, "DELETE"),
  (pygame.K_KP0, "KP0"),
  (pygame.K_KP1, "KP1"),
  (pygame.K_KP2, "KP2"),
  (pygame.K_KP3, "KP3"),
  (pygame.K_KP4, "KP4"),
  (pygame.K_KP5, "KP5"),
  (pygame.K_KP6, "KP6"),
  (pygame.K_KP7, "KP7"),
  (pygame.K_KP8, "KP8"),
  (pygame.K_KP9, "KP9"),
  (pygame.K_KP_PERIOD, "KP_PERIOD"),
  (pygame.K_KP_DIVIDE, "KP_DIVIDE"),
  (pygame.K_KP_MULTIPLY, "KP_MULTIPLY"),
  (pygame.K_KP_MINUS, "KP_MINUS"),
  (pygame.K_KP_PLUS, "KP_PLUS"),
  (pygame.K_KP_ENTER, "KP_ENTER"),
  (pygame.K_KP_EQUALS, "KP_EQUALS"),
  (pygame.K_UP, "UP"),
  (pygame.K_DOWN, "DOWN"),
  (pygame.K_RIGHT, "RIGHT"),
  (pygame.K_LEFT, "LEFT"),
  (pygame.K_INSERT, "INSERT"),
  (pygame.K_HOME, "HOME"),
  (pygame.K_END, "END"),
  (pygame.K_PAGEUP, "PAGEUP"),
  (pygame.K_PAGEDOWN, "PAGEDOWN"),
  (pygame.K_F1, "F1"),
  (pygame.K_F2, "F2"),
  (pygame.K_F3, "F3"),
  (pygame.K_F4, "F4"),
  (pygame.K_F5, "F5"),
  (pygame.K_F6, "F6"),
  (pygame.K_F7, "F7"),
  (pygame.K_F8, "F8"),
  (pygame.K_F9, "F9"),
  (pygame.K_F10, "F10"),
  (pygame.K_F11, "F11"),
  (pygame.K_F12, "F12"),
  (pygame.K_F13, "F13"),
  (pygame.K_F14, "F14"),
  (pygame.K_F15, "F15"),
  (pygame.K_NUMLOCK, "NUMLOCK"),
  (pygame.K_CAPSLOCK, "CAPSLOCK"),
  (pygame.K_SCROLLOCK, "SCROLLOCK"),
  (pygame.K_RSHIFT, "RSHIFT"),
  (pygame.K_LSHIFT, "LSHIFT"),
  (pygame.K_RCTRL, "RCTRL"),
  (pygame.K_LCTRL, "LCTRL"),
  (pygame.K_RALT, "RALT"),
  (pygame.K_LALT, "LALT"),
  (pygame.K_RMETA, "RMETA"),
  (pygame.K_LMETA, "LMETA"),
  (pygame.K_LSUPER, "LSUPER"),
  (pygame.K_RSUPER, "RSUPER"),
  (pygame.K_MODE, "MODE"),
  (pygame.K_HELP, "HELP"),
  (pygame.K_PRINT, "PRINT"),
  (pygame.K_SYSREQ, "SYSREQ"),
  (pygame.K_BREAK, "BREAK"),
  (pygame.K_MENU, "MENU"),
  (pygame.K_POWER, "POWER"),
  (pygame.K_EURO, "EURO"),
])

kmods_map = [
  (pygame.KMOD_LCTRL, "LCTRL"),
  (pygame.KMOD_LSHIFT, "LSHIFT"),
  (pygame.KMOD_LALT, "LALT"),
  (pygame.KMOD_LMETA, "LMETA"),
  (pygame.KMOD_RCTRL, "RCTRL"),
  (pygame.KMOD_RSHIFT, "RSHIFT"),
  (pygame.KMOD_RALT, "RALT"),
  (pygame.KMOD_RMETA, "RMETA"),
]

def onkeyevent (e, isdown):
  modifiers = list(
    map(lambda a: a[1],
        filter(lambda a: e.mod & a[0] != 0, kmods_map)))
  key = keysmap.get(e.key, None)
  print(hex(e.key), hex(e.mod), key)
  ret = client.keyevent(key, modifiers, isdown)
  if 'result' not in ret:
    print("keyevent ({}, {}, {}) response error: {}", key, modifiers, isdown, ret.get("error", "undefined"))
  else:
    print("keyevent ({}, {}, {}) response: {}".format(key, modifiers, isdown, ret["result"]))

## Main. This loads the window
pygame.init()
pygame.display.set_icon(pygame.image.load('resources/logo.png'))
pygame.display.set_caption('RelayKeys Capture Window')
size = (200,200)
screen = pygame.display.set_mode (size)
c = pygame.time.Clock ()
going = True
while going:
  for e in pygame.event.get ():
    # print (e)
    if e.type == QUIT:
      # one can exit relaykeysd
      try:
        client.exit()
      except:
        pass
      going = False
      pygame.quit()
      exit()
    elif e.type == KEYDOWN:
      onkeyevent(e, True)
    elif e.type == KEYUP:
      onkeyevent(e, False)
  pygame.display.flip()
  c.tick(40)
