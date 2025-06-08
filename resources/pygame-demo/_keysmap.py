import array as arr

import pygame

# some scripting to form keys and mapping of them

keynames = [
    "K_BACKSPACE",  #   \b      backspace
    "K_TAB",  #         \t      tab
    "K_CLEAR",  #               clear
    "K_RETURN",  #      \r      return
    "K_PAUSE",  #               pause
    "K_ESCAPE",  #      ^[      escape
    "K_SPACE",  #               space
    "K_EXCLAIM",  #     !       exclaim
    "K_QUOTEDBL",  #    "       quotedbl
    "K_HASH",  #        #       hash
    "K_DOLLAR",  #      $       dollar
    "K_AMPERSAND",  #   &       ampersand
    "K_QUOTE",  #               quote
    "K_LEFTPAREN",  #   (       left parenthesis
    "K_RIGHTPAREN",  #  )       right parenthesis
    "K_ASTERISK",  #    *       asterisk
    "K_PLUS",  #        +       plus sign
    "K_COMMA",  #       ,       comma
    "K_MINUS",  #       -       minus sign
    "K_PERIOD",  #      .       period
    "K_SLASH",  #       /       forward slash
    "K_0",  #           0       0
    "K_1",  #           1       1
    "K_2",  #           2       2
    "K_3",  #           3       3
    "K_4",  #           4       4
    "K_5",  #           5       5
    "K_6",  #           6       6
    "K_7",  #           7       7
    "K_8",  #           8       8
    "K_9",  #           9       9
    "K_COLON",  #       :       colon
    "K_SEMICOLON",  #   ;       semicolon
    "K_LESS",  #        <       less-than sign
    "K_EQUALS",  #      =       equals sign
    "K_GREATER",  #     >       greater-than sign
    "K_QUESTION",  #    ?       question mark
    "K_AT",  #          @       at
    "K_LEFTBRACKET",  # [       left bracket
    "K_BACKSLASH",  #   \       backslash
    "K_RIGHTBRACKET",  # ]      right bracket
    "K_CARET",  #       ^       caret
    "K_UNDERSCORE",  #  _       underscore
    "K_BACKQUOTE",  #   `       grave
    "K_a",  #           a       a
    "K_b",  #           b       b
    "K_c",  #           c       c
    "K_d",  #           d       d
    "K_e",  #           e       e
    "K_f",  #           f       f
    "K_g",  #           g       g
    "K_h",  #           h       h
    "K_i",  #           i       i
    "K_j",  #           j       j
    "K_k",  #           k       k
    "K_l",  #           l       l
    "K_m",  #           m       m
    "K_n",  #           n       n
    "K_o",  #           o       o
    "K_p",  #           p       p
    "K_q",  #           q       q
    "K_r",  #           r       r
    "K_s",  #           s       s
    "K_t",  #           t       t
    "K_u",  #           u       u
    "K_v",  #           v       v
    "K_w",  #           w       w
    "K_x",  #           x       x
    "K_y",  #           y       y
    "K_z",  #           z       z
    "K_DELETE",  #              delete
    "K_KP0",  #                 keypad 0
    "K_KP1",  #                 keypad 1
    "K_KP2",  #                 keypad 2
    "K_KP3",  #                 keypad 3
    "K_KP4",  #                 keypad 4
    "K_KP5",  #                 keypad 5
    "K_KP6",  #                 keypad 6
    "K_KP7",  #                 keypad 7
    "K_KP8",  #                 keypad 8
    "K_KP9",  #                 keypad 9
    "K_KP_PERIOD",  #   .       keypad period
    "K_KP_DIVIDE",  #   /       keypad divide
    "K_KP_MULTIPLY",  # *       keypad multiply
    "K_KP_MINUS",  #    -       keypad minus
    "K_KP_PLUS",  #     +       keypad plus
    "K_KP_ENTER",  #    \r      keypad enter
    "K_KP_EQUALS",  #   =       keypad equals
    "K_UP",  #                  up arrow
    "K_DOWN",  #                down arrow
    "K_RIGHT",  #               right arrow
    "K_LEFT",  #                left arrow
    "K_INSERT",  #              insert
    "K_HOME",  #                home
    "K_END",  #                 end
    "K_PAGEUP",  #              page up
    "K_PAGEDOWN",  #            page down
    "K_F1",  #                  F1
    "K_F2",  #                  F2
    "K_F3",  #                  F3
    "K_F4",  #                  F4
    "K_F5",  #                  F5
    "K_F6",  #                  F6
    "K_F7",  #                  F7
    "K_F8",  #                  F8
    "K_F9",  #                  F9
    "K_F10",  #                 F10
    "K_F11",  #                 F11
    "K_F12",  #                 F12
    "K_F13",  #                 F13
    "K_F14",  #                 F14
    "K_F15",  #                 F15
    "K_NUMLOCK",  #             numlock
    "K_CAPSLOCK",  #            capslock
    "K_SCROLLOCK",  #           scrollock
    "K_RSHIFT",  #              right shift
    "K_LSHIFT",  #              left shift
    "K_RCTRL",  #               right control
    "K_LCTRL",  #               left control
    "K_RALT",  #                right alt
    "K_LALT",  #                left alt
    "K_RMETA",  #               right meta
    "K_LMETA",  #               left meta
    "K_LSUPER",  #              left Windows key
    "K_RSUPER",  #              right Windows key
    "K_MODE",  #                mode shift
    "K_HELP",  #                help
    "K_PRINT",  #               print screen
    "K_SYSREQ",  #              sysrq
    "K_BREAK",  #               break
    "K_MENU",  #                menu
    "K_POWER",  #               power
    "K_EURO",  #                Euro
]

# Translate keycodes from pygame to USB HID codes
# uint8_t HIDCode[512]
HIDCode = arr.array(
    "B",
    [
        0,  # 0
        0,  # 1
        0,  # 2
        0,  # 3
        0,  # 4
        0,  # 5
        0,  # 6
        0,  # 7
        0x2A,  # 8
        0x2B,  # 9
        0,  # 10
        0,  # 11
        0,  # 12
        0,  # 13
        0,  # 14
        0,  # 15
        0,  # 16
        0,  # 17
        0,  # 18
        0x48,  # 19
        0,  # 20
        0,  # 21
        0,  # 22
        0,  # 23
        0,  # 24
        0,  # 25
        0,  # 26
        0x29,  # 27
        0,  # 28
        0,  # 29
        0,  # 30
        0,  # 31
        0x2C,  # 32
        0,  # 33
        0,  # 34
        0,  # 35
        0,  # 36
        0,  # 37
        0,  # 38
        0x34,  # 39
        0,  # 40
        0,  # 41
        0,  # 42
        0,  # 43
        0x36,  # 44
        0x2D,  # 45
        0x37,  # 46
        0x38,  # 47
        39,  # 48
        30,  # 49
        31,  # 50
        32,  # 51
        33,  # 52
        34,  # 53
        35,  # 54
        36,  # 55
        37,  # 56
        38,  # 57
        0,  # 58
        0x33,  # 59
        0,  # 60
        0x2E,  # 61
        0,  # 62
        0,  # 63
        0,  # 64
        0,  # 65
        0,  # 66
        0,  # 67
        0,  # 68
        0,  # 69
        0,  # 70
        0,  # 71
        0,  # 72
        0,  # 73
        0,  # 74
        0,  # 75
        0,  # 76
        0,  # 77
        0,  # 78
        0,  # 79
        0,  # 80
        0,  # 81
        0,  # 82
        0,  # 83
        0,  # 84
        0,  # 85
        0,  # 86
        0,  # 87
        0,  # 88
        0,  # 89
        0,  # 90
        0x2F,  # 91
        0x31,  # 92
        0x30,  # 93
        0,  # 94
        0,  # 95
        0x35,  # 96
        4,  # 97
        5,  # 98
        6,  # 99
        7,  # 100
        8,  # 101
        9,  # 102
        10,  # 103
        11,  # 104
        12,  # 105
        13,  # 106
        14,  # 107
        15,  # 108
        16,  # 109
        17,  # 110
        18,  # 111
        19,  # 112
        20,  # 113
        21,  # 114
        22,  # 115
        23,  # 116
        24,  # 117
        25,  # 118
        26,  # 119
        27,  # 120
        28,  # 121
        29,  # 122
        0,  # 123
        0,  # 124
        0,  # 125
        0,  # 126
        0x4C,  # 127
        0,  # 128
        0,  # 129
        0,  # 130
        0,  # 131
        0,  # 132
        0,  # 133
        0,  # 134
        0,  # 135
        0,  # 136
        0,  # 137
        0,  # 138
        0,  # 139
        0,  # 140
        0,  # 141
        0,  # 142
        0,  # 143
        0,  # 144
        0,  # 145
        0,  # 146
        0,  # 147
        0,  # 148
        0,  # 149
        0,  # 150
        0,  # 151
        0,  # 152
        0,  # 153
        0,  # 154
        0,  # 155
        0,  # 156
        0,  # 157
        0,  # 158
        0,  # 159
        0,  # 160
        0,  # 161
        0,  # 162
        0,  # 163
        0,  # 164
        0,  # 165
        0,  # 166
        0,  # 167
        0,  # 168
        0,  # 169
        0,  # 170
        0,  # 171
        0,  # 172
        0,  # 173
        0,  # 174
        0,  # 175
        0,  # 176
        0,  # 177
        0,  # 178
        0,  # 179
        0,  # 180
        0,  # 181
        0,  # 182
        0,  # 183
        0,  # 184
        0,  # 185
        0,  # 186
        0,  # 187
        0,  # 188
        0,  # 189
        0,  # 190
        0,  # 191
        0,  # 192
        0,  # 193
        0,  # 194
        0,  # 195
        0,  # 196
        0,  # 197
        0,  # 198
        0,  # 199
        0,  # 200
        0,  # 201
        0,  # 202
        0,  # 203
        0,  # 204
        0,  # 205
        0,  # 206
        0,  # 207
        0,  # 208
        0,  # 209
        0,  # 210
        0,  # 211
        0,  # 212
        0,  # 213
        0,  # 214
        0,  # 215
        0,  # 216
        0,  # 217
        0,  # 218
        0,  # 219
        0,  # 220
        0,  # 221
        0,  # 222
        0,  # 223
        0,  # 224
        0,  # 225
        0,  # 226
        0,  # 227
        0,  # 228
        0,  # 229
        0,  # 230
        0,  # 231
        0,  # 232
        0,  # 233
        0,  # 234
        0,  # 235
        0,  # 236
        0,  # 237
        0,  # 238
        0,  # 239
        0,  # 240
        0,  # 241
        0,  # 242
        0,  # 243
        0,  # 244
        0,  # 245
        0,  # 246
        0,  # 247
        0,  # 248
        0,  # 249
        0,  # 250
        0,  # 251
        0,  # 252
        0,  # 253
        0,  # 254
        0,  # 255
        0x62,  # 256
        0x59,  # 257
        0x5A,  # 258
        0x5B,  # 259
        0x5C,  # 260
        0x5D,  # 261
        0x5E,  # 262
        0x5F,  # 263
        0x60,  # 264
        0x61,  # 265
        0x63,  # 266
        0x54,  # 267
        0x55,  # 268
        0x56,  # 269
        0x57,  # 270
        0x58,  # 271
        0,  # 272
        0x52,  # 273
        0x51,  # 274
        0x4F,  # 275
        0x50,  # 276
        0x49,  # 277
        0x4A,  # 278
        0x4D,  # 279
        0x4B,  # 280
        0x4E,  # 281
        58,  # 282
        59,  # 283
        60,  # 284
        61,  # 285
        62,  # 286
        63,  # 287
        64,  # 288
        65,  # 289
        66,  # 290
        67,  # 291
        68,  # 292
        69,  # 293
        0,  # 294
        0,  # 295
        0,  # 296
        0,  # 297
        0,  # 298
        0,  # 299
        0x53,  # 300
        0x39,  # 301
        0x47,  # 302
        0,  # 303
        0,  # 304
        0,  # 305
        0,  # 306
        0,  # 307
        0,  # 308
        0,  # 309
        0,  # 310
        0,  # 311
        0,  # 312
        0,  # 313
        0,  # 314
        0,  # 315
        0,  # 316
        0,  # 317
        0,  # 318
        0,  # 319
        0,  # 320
        0,  # 321
        0,  # 322
        0,  # 323
        0,  # 324
        0,  # 325
        0,  # 326
        0,  # 327
        0,  # 328
        0,  # 329
        0,  # 330
        0,  # 331
        0,  # 332
        0,  # 333
        0,  # 334
        0,  # 335
        0,  # 336
        0,  # 337
        0,  # 338
        0,  # 339
        0,  # 340
        0,  # 341
        0,  # 342
        0,  # 343
        0,  # 344
        0,  # 345
        0,  # 346
        0,  # 347
        0,  # 348
        0,  # 349
        0,  # 350
        0,  # 351
        0,  # 352
        0,  # 353
        0,  # 354
        0,  # 355
        0,  # 356
        0,  # 357
        0,  # 358
        0,  # 359
        0,  # 360
        0,  # 361
        0,  # 362
        0,  # 363
        0,  # 364
        0,  # 365
        0,  # 366
        0,  # 367
        0,  # 368
        0,  # 369
        0,  # 370
        0,  # 371
        0,  # 372
        0,  # 373
        0,  # 374
        0,  # 375
        0,  # 376
        0,  # 377
        0,  # 378
        0,  # 379
        0,  # 380
        0,  # 381
        0,  # 382
        0,  # 383
        0,  # 384
        0,  # 385
        0,  # 386
        0,  # 387
        0,  # 388
        0,  # 389
        0,  # 390
        0,  # 391
        0,  # 392
        0,  # 393
        0,  # 394
        0,  # 395
        0,  # 396
        0,  # 397
        0,  # 398
        0,  # 399
        0,  # 400
        0,  # 401
        0,  # 402
        0,  # 403
        0,  # 404
        0,  # 405
        0,  # 406
        0,  # 407
        0,  # 408
        0,  # 409
        0,  # 410
        0,  # 411
        0,  # 412
        0,  # 413
        0,  # 414
        0,  # 415
        0,  # 416
        0,  # 417
        0,  # 418
        0,  # 419
        0,  # 420
        0,  # 421
        0,  # 422
        0,  # 423
        0,  # 424
        0,  # 425
        0,  # 426
        0,  # 427
        0,  # 428
        0,  # 429
        0,  # 430
        0,  # 431
        0,  # 432
        0,  # 433
        0,  # 434
        0,  # 435
        0,  # 436
        0,  # 437
        0,  # 438
        0,  # 439
        0,  # 440
        0,  # 441
        0,  # 442
        0,  # 443
        0,  # 444
        0,  # 445
        0,  # 446
        0,  # 447
        0,  # 448
        0,  # 449
        0,  # 450
        0,  # 451
        0,  # 452
        0,  # 453
        0,  # 454
        0,  # 455
        0,  # 456
        0,  # 457
        0,  # 458
        0,  # 459
        0,  # 460
        0,  # 461
        0,  # 462
        0,  # 463
        0,  # 464
        0,  # 465
        0,  # 466
        0,  # 467
        0,  # 468
        0,  # 469
        0,  # 470
        0,  # 471
        0,  # 472
        0,  # 473
        0,  # 474
        0,  # 475
        0,  # 476
        0,  # 477
        0,  # 478
        0,  # 479
        0,  # 480
        0,  # 481
        0,  # 482
        0,  # 483
        0,  # 484
        0,  # 485
        0,  # 486
        0,  # 487
        0,  # 488
        0,  # 489
        0,  # 490
        0,  # 491
        0,  # 492
        0,  # 493
        0,  # 494
        0,  # 495
        0,  # 496
        0,  # 497
        0,  # 498
        0,  # 499
        0,  # 500
        0,  # 501
        0,  # 502
        0,  # 503
        0,  # 504
        0,  # 505
        0,  # 506
        0,  # 507
        0,  # 508
        0,  # 509
        0,  # 510
        0,  # 511
    ],
)

keysmap = list(
    filter(
        lambda a: a[1] != 0,
        map(lambda a: (a[2:].upper(), HIDCode[getattr(pygame, a)]), keynames),
    )
)

keysmap2 = list(
    filter(lambda a: a[1] != 0, map(lambda a: ("pygame." + a, a[2:].upper()), keynames))
)

kmods = list(
    map(
        lambda a: a.strip(),
        """
KMOD_LSHIFT, KMOD_RSHIFT, KMOD_SHIFT, KMOD_CAPS,
KMOD_LCTRL, KMOD_RCTRL, KMOD_CTRL, KMOD_LALT, KMOD_RALT,
KMOD_ALT, KMOD_LMETA, KMOD_RMETA, KMOD_META, KMOD_NUM, KMOD_MODE
""".split(
            ","
        ),
    )
)

keysmap3 = map(
    lambda a: ("pygame.KMOD_" + a[0], a[0]),
    filter(
        lambda a: "KMOD_" + a[0] in kmods,
        [
            ("LCTRL", 0x01),
            ("LSHIFT", 0x02),
            ("LALT", 0x04),
            ("LMETA", 0x08),
            ("RCTRL", 0x10),
            ("RSHIFT", 0x20),
            ("RALT", 0x40),
            ("RMETA", 0x80),
        ],
    ),
)

import win32api
import win32con

keystrokesdata = (
    ("A", "a", win32api.VkKeyScan("a"), "a"),
    ("B", "b", win32api.VkKeyScan("b"), "b"),
    ("C", "c", win32api.VkKeyScan("c"), "c"),
    ("D", "d", win32api.VkKeyScan("d"), "d"),
    ("E", "e", win32api.VkKeyScan("e"), "e"),
    ("F", "f", win32api.VkKeyScan("f"), "f"),
    ("G", "g", win32api.VkKeyScan("g"), "g"),
    ("H", "h", win32api.VkKeyScan("h"), "h"),
    ("I", "i", win32api.VkKeyScan("i"), "i"),
    ("J", "j", win32api.VkKeyScan("j"), "j"),
    ("K", "k", win32api.VkKeyScan("k"), "k"),
    ("L", "l", win32api.VkKeyScan("l"), "l"),
    ("M", "m", win32api.VkKeyScan("m"), "m"),
    ("N", "n", win32api.VkKeyScan("n"), "n"),
    ("O", "o", win32api.VkKeyScan("o"), "o"),
    ("P", "p", win32api.VkKeyScan("p"), "p"),
    ("Q", "q", win32api.VkKeyScan("q"), "q"),
    ("R", "r", win32api.VkKeyScan("r"), "r"),
    ("S", "s", win32api.VkKeyScan("s"), "s"),
    ("T", "t", win32api.VkKeyScan("t"), "t"),
    ("U", "u", win32api.VkKeyScan("u"), "u"),
    ("V", "v", win32api.VkKeyScan("v"), "v"),
    ("W", "w", win32api.VkKeyScan("w"), "w"),
    ("X", "x", win32api.VkKeyScan("x"), "x"),
    ("Y", "y", win32api.VkKeyScan("y"), "y"),
    ("Z", "z", win32api.VkKeyScan("z"), "z"),
    ("ONE", "1", win32api.VkKeyScan("1"), "1"),
    ("TWO", "2", win32api.VkKeyScan("2"), "2"),
    ("THREE", "3", win32api.VkKeyScan("3"), "3"),
    ("FOUR", "4", win32api.VkKeyScan("4"), "4"),
    ("FIVE", "5", win32api.VkKeyScan("5"), "5"),
    ("SIX", "6", win32api.VkKeyScan("6"), "6"),
    ("SEVEN", "7", win32api.VkKeyScan("7"), "7"),
    ("EIGHT", "8", win32api.VkKeyScan("8"), "8"),
    ("NINE", "9", win32api.VkKeyScan("9"), "9"),
    ("ZERO", "0", win32api.VkKeyScan("0"), "0"),
    ("DOT", ".", win32api.VkKeyScan("."), "."),
    ("COMMA", ",", win32api.VkKeyScan(","), ","),
    ("QUESTION", "?", win32api.VkKeyScan("?"), "?"),
    ("EXCLAMATION", "!", win32api.VkKeyScan("!"), "!"),
    ("COLON", ":", win32api.VkKeyScan(":"), ":"),
    ("SEMICOLON", ";", win32api.VkKeyScan(";"), ";"),
    ("AT", "@", win32api.VkKeyScan("@"), "@"),
    ("BASH", "#", win32api.VkKeyScan("#"), "#"),
    ("DOLLAR", "$", win32api.VkKeyScan("$"), "$"),
    ("PERCENT", "%", win32api.VkKeyScan("%"), "%"),
    ("AMPERSAND", "&", win32api.VkKeyScan("&"), "&"),
    ("STAR", "*", win32con.VK_MULTIPLY, "*"),
    ("PLUS", "+", win32con.VK_ADD, "+"),
    ("MINUS", "-", win32con.VK_SUBTRACT, "-"),
    ("EQUALS", "=", win32api.VkKeyScan("="), "="),
    ("FSLASH", "/", win32api.VkKeyScan("/"), "/"),
    ("BSLASH", "\\", win32api.VkKeyScan("\\"), "\\"),
    ("SINGLEQUOTE", "'", win32api.VkKeyScan("'"), "'"),
    ("DOUBLEQUOTE", '"', win32api.VkKeyScan('"'), '"'),
    ("OPENBRACKET", "(", win32api.VkKeyScan("("), "("),
    ("CLOSEBRACKET", ")", win32api.VkKeyScan(")"), ")"),
    ("LESSTHAN", "<", win32api.VkKeyScan("<"), "<"),
    ("MORETHAN", ">", win32api.VkKeyScan(">"), ">"),
    ("CIRCONFLEX", "^", win32api.VkKeyScan("^"), "^"),
    ("ENTER", "ENTER", win32con.VK_RETURN, "\n"),
    ("SPACE", "space", win32con.VK_SPACE, " "),
    ("BACKSPACE", "bckspc", win32con.VK_BACK, chr(8)),
    ("TAB", "tab", win32con.VK_TAB, "\t"),
    ("TABLEFT", "tab", win32con.VK_TAB, "\t"),
    ("UNDERSCORE", "_", win32api.VkKeyScan("_"), "_"),
    ("PAGEUP", "pageup", win32con.VK_PRIOR, None),
    ("PAGEDOWN", "pagedwn", win32con.VK_NEXT, None),
    ("LEFTARROW", "left", win32con.VK_LEFT, None),
    ("RIGHTARROW", "right", win32con.VK_RIGHT, "right"),
    ("UPARROW", "up", win32con.VK_UP, "up"),
    ("DOWNARROW", "down", win32con.VK_DOWN, "down"),
    ("ESCAPE", "esc", win32con.VK_ESCAPE, "esc"),
    ("HOME", "home", win32con.VK_HOME, "home"),
    ("END", "end", win32con.VK_END, None),
    ("INSERT", "insert", win32con.VK_INSERT, None),
    ("DELETE", "del", win32con.VK_DELETE, None),
    ("STARTMENU", "start", win32con.VK_MENU, None),
    ("SHIFT", "shift", win32con.VK_SHIFT, None, True),
    ("ALT", "alt", win32con.VK_MENU, None, True),
    ("CTRL", "ctrl", win32con.VK_CONTROL, None, True),
    ("WINDOWS", "win", win32con.VK_LWIN, None),
    ("APPKEY", "app", win32con.VK_LWIN, None),
    ("LCTRL", "left ctrl", win32con.VK_LCONTROL, None),
    ("RCTRL", "right ctrl", win32con.VK_RCONTROL, None),
    ("LSHIFT", "left shift", win32con.VK_LSHIFT, None),
    ("RSHIFT", "right shift", win32con.VK_RSHIFT, None),
    ("RALT", "right alt", win32con.VK_RMENU, None),
    ("LALT", "alt", win32con.VK_LMENU, None),
    ("CAPSLOCK", "caps", win32con.VK_CAPITAL, None),
    ("F1", "F1", win32con.VK_F1, None),
    ("F2", "F2", win32con.VK_F2, None),
    ("F3", "F3", win32con.VK_F3, None),
    ("F4", "F4", win32con.VK_F4, None),
    ("F5", "F5", win32con.VK_F5, None),
    ("F6", "F6", win32con.VK_F6, None),
    ("F7", "F7", win32con.VK_F7, None),
    ("F8", "F8", win32con.VK_F8, None),
    ("F9", "F9", win32con.VK_F9, None),
    ("F10", "F10", win32con.VK_F10, None),
    ("F11", "F11", win32con.VK_F11, None),
    ("F12", "F12", win32con.VK_F12, None),
)

keynames2 = list(map(lambda a: a[2:].upper(), keynames))

print("[")
for kdata in keystrokesdata:
    val = kdata[0]
    if val not in keynames2:
        val = "#" + val + "#"
    print(f'  ({kdata[2]}, "{val}"),')
"""
for akey in keysmap3:
  print("  ({}, \"{}\"),".format(akey[0], akey[1]))
"""
"""
for akey in keysmap:
  print("  (\"{}\", 0x{:02x}),".format(akey[0], akey[1]))
"""
print("]")
