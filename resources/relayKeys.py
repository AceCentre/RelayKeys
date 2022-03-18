# coding=utf-8

# To debug - without the correct hardware attached:
#   Run demoSerial.py 
#   Call this code with relayKeys.py no-serial 

import os, sys, glob, serial, logging, time, pygame
import serial.tools.list_ports
import array as arr
from pygame.locals import *
from pygame.compat import as_bytes
BytesIO = pygame.compat.get_BytesIO()

#Use AT+BAUDRATE=115200 but make sure hardware flow control CTS/RTS works
BAUD = 115200
#Doesnt do much currently
OS = 'ios'
debug = True			
		

    
# Translate keycodes from pygame to USB HID codes
# uint8_t HIDCode[512]
HIDCode = arr.array('B', [
0,	# 0
0,	# 1
0,	# 2
0,	# 3
0,	# 4
0,	# 5
0,	# 6
0,	# 7
0x2A,	# 8
0x2B,	# 9
0,	# 10
0,	# 11
0,	# 12
0,	# 13
0,	# 14
0,	# 15
0,	# 16
0,	# 17
0,	# 18
0x48,	# 19
0,	# 20
0,	# 21
0,	# 22
0,	# 23
0,	# 24
0,	# 25
0,	# 26
0x29,	# 27
0,	# 28
0,	# 29
0,	# 30
0,	# 31
0x2C,	# 32
0,	# 33
0,	# 34
0,	# 35
0,	# 36
0,	# 37
0,	# 38
0x34,	# 39
0,	# 40
0,	# 41
0,	# 42
0,	# 43
0x36,	# 44
0x2D,	# 45
0x37,	# 46
0x38,	# 47
39,	# 48
30,	# 49
31,	# 50
32,	# 51
33,	# 52
34,	# 53
35,	# 54
36,	# 55
37,	# 56
38,	# 57
0,	# 58
0x33,	# 59
0,	# 60
0x2E,	# 61
0,	# 62
0,	# 63
0,	# 64
0,	# 65
0,	# 66
0,	# 67
0,	# 68
0,	# 69
0,	# 70
0,	# 71
0,	# 72
0,	# 73
0,	# 74
0,	# 75
0,	# 76
0,	# 77
0,	# 78
0,	# 79
0,	# 80
0,	# 81
0,	# 82
0,	# 83
0,	# 84
0,	# 85
0,	# 86
0,	# 87
0,	# 88
0,	# 89
0,	# 90
0x2F,	# 91
0x31,	# 92
0x30,	# 93
0,	# 94
0,	# 95
0x35,	# 96
4,	# 97
5,	# 98
6,	# 99
7,	# 100
8,	# 101
9,	# 102
10,	# 103
11,	# 104
12,	# 105
13,	# 106
14,	# 107
15,	# 108
16,	# 109
17,	# 110
18,	# 111
19,	# 112
20,	# 113
21,	# 114
22,	# 115
23,	# 116
24,	# 117
25,	# 118
26,	# 119
27,	# 120
28,	# 121
29,	# 122
0,	# 123
0,	# 124
0,	# 125
0,	# 126
0x4C,	# 127
0,	# 128
0,	# 129
0,	# 130
0,	# 131
0,	# 132
0,	# 133
0,	# 134
0,	# 135
0,	# 136
0,	# 137
0,	# 138
0,	# 139
0,	# 140
0,	# 141
0,	# 142
0,	# 143
0,	# 144
0,	# 145
0,	# 146
0,	# 147
0,	# 148
0,	# 149
0,	# 150
0,	# 151
0,	# 152
0,	# 153
0,	# 154
0,	# 155
0,	# 156
0,	# 157
0,	# 158
0,	# 159
0,	# 160
0,	# 161
0,	# 162
0,	# 163
0,	# 164
0,	# 165
0,	# 166
0,	# 167
0,	# 168
0,	# 169
0,	# 170
0,	# 171
0,	# 172
0,	# 173
0,	# 174
0,	# 175
0,	# 176
0,	# 177
0,	# 178
0,	# 179
0,	# 180
0,	# 181
0,	# 182
0,	# 183
0,	# 184
0,	# 185
0,	# 186
0,	# 187
0,	# 188
0,	# 189
0,	# 190
0,	# 191
0,	# 192
0,	# 193
0,	# 194
0,	# 195
0,	# 196
0,	# 197
0,	# 198
0,	# 199
0,	# 200
0,	# 201
0,	# 202
0,	# 203
0,	# 204
0,	# 205
0,	# 206
0,	# 207
0,	# 208
0,	# 209
0,	# 210
0,	# 211
0,	# 212
0,	# 213
0,	# 214
0,	# 215
0,	# 216
0,	# 217
0,	# 218
0,	# 219
0,	# 220
0,	# 221
0,	# 222
0,	# 223
0,	# 224
0,	# 225
0,	# 226
0,	# 227
0,	# 228
0,	# 229
0,	# 230
0,	# 231
0,	# 232
0,	# 233
0,	# 234
0,	# 235
0,	# 236
0,	# 237
0,	# 238
0,	# 239
0,	# 240
0,	# 241
0,	# 242
0,	# 243
0,	# 244
0,	# 245
0,	# 246
0,	# 247
0,	# 248
0,	# 249
0,	# 250
0,	# 251
0,	# 252
0,	# 253
0,	# 254
0,	# 255
0x62,	# 256
0x59,	# 257
0x5A,	# 258
0x5B,	# 259
0x5C,	# 260
0x5D,	# 261
0x5E,	# 262
0x5F,	# 263
0x60,	# 264
0x61,	# 265
0x63,	# 266
0x54,	# 267
0x55,	# 268
0x56,	# 269
0x57,	# 270
0x58,	# 271
0,	# 272
0x52,	# 273
0x51,	# 274
0x4F,	# 275
0x50,	# 276
0x49,	# 277
0x4A,	# 278
0x4D,	# 279
0x4B,	# 280
0x4E,	# 281
58,	# 282
59,	# 283
60,	# 284
61,	# 285
62,	# 286
63,	# 287
64,	# 288
65,	# 289
66,	# 290
67,	# 291
68,	# 292
69,	# 293
0,	# 294
0,	# 295
0,	# 296
0,	# 297
0,	# 298
0,	# 299
0x53,	# 300
0x39,	# 301
0x47,	# 302
0,	# 303
0,	# 304
0,	# 305
0,	# 306
0,	# 307
0,	# 308
0,	# 309
0,	# 310
0,	# 311
0,	# 312
0,	# 313
0,	# 314
0,	# 315
0,	# 316
0,	# 317
0,	# 318
0,	# 319
0,	# 320
0,	# 321
0,	# 322
0,	# 323
0,	# 324
0,	# 325
0,	# 326
0,	# 327
0,	# 328
0,	# 329
0,	# 330
0,	# 331
0,	# 332
0,	# 333
0,	# 334
0,	# 335
0,	# 336
0,	# 337
0,	# 338
0,	# 339
0,	# 340
0,	# 341
0,	# 342
0,	# 343
0,	# 344
0,	# 345
0,	# 346
0,	# 347
0,	# 348
0,	# 349
0,	# 350
0,	# 351
0,	# 352
0,	# 353
0,	# 354
0,	# 355
0,	# 356
0,	# 357
0,	# 358
0,	# 359
0,	# 360
0,	# 361
0,	# 362
0,	# 363
0,	# 364
0,	# 365
0,	# 366
0,	# 367
0,	# 368
0,	# 369
0,	# 370
0,	# 371
0,	# 372
0,	# 373
0,	# 374
0,	# 375
0,	# 376
0,	# 377
0,	# 378
0,	# 379
0,	# 380
0,	# 381
0,	# 382
0,	# 383
0,	# 384
0,	# 385
0,	# 386
0,	# 387
0,	# 388
0,	# 389
0,	# 390
0,	# 391
0,	# 392
0,	# 393
0,	# 394
0,	# 395
0,	# 396
0,	# 397
0,	# 398
0,	# 399
0,	# 400
0,	# 401
0,	# 402
0,	# 403
0,	# 404
0,	# 405
0,	# 406
0,	# 407
0,	# 408
0,	# 409
0,	# 410
0,	# 411
0,	# 412
0,	# 413
0,	# 414
0,	# 415
0,	# 416
0,	# 417
0,	# 418
0,	# 419
0,	# 420
0,	# 421
0,	# 422
0,	# 423
0,	# 424
0,	# 425
0,	# 426
0,	# 427
0,	# 428
0,	# 429
0,	# 430
0,	# 431
0,	# 432
0,	# 433
0,	# 434
0,	# 435
0,	# 436
0,	# 437
0,	# 438
0,	# 439
0,	# 440
0,	# 441
0,	# 442
0,	# 443
0,	# 444
0,	# 445
0,	# 446
0,	# 447
0,	# 448
0,	# 449
0,	# 450
0,	# 451
0,	# 452
0,	# 453
0,	# 454
0,	# 455
0,	# 456
0,	# 457
0,	# 458
0,	# 459
0,	# 460
0,	# 461
0,	# 462
0,	# 463
0,	# 464
0,	# 465
0,	# 466
0,	# 467
0,	# 468
0,	# 469
0,	# 470
0,	# 471
0,	# 472
0,	# 473
0,	# 474
0,	# 475
0,	# 476
0,	# 477
0,	# 478
0,	# 479
0,	# 480
0,	# 481
0,	# 482
0,	# 483
0,	# 484
0,	# 485
0,	# 486
0,	# 487
0,	# 488
0,	# 489
0,	# 490
0,	# 491
0,	# 492
0,	# 493
0,	# 494
0,	# 495
0,	# 496
0,	# 497
0,	# 498
0,	# 499
0,	# 500
0,	# 501
0,	# 502
0,	# 503
0,	# 504
0,	# 505
0,	# 506
0,	# 507
0,	# 508
0,	# 509
0,	# 510
0	# 511
])

# Six keys for USB keyboard HID report
# uint8_t keys[6] = {0,0,0,0,0,0}
keys = arr.array('B', [0, 0, 0, 0, 0, 0])

def mkHID(keycode, modifiers, down):
    logging.debug(f'keycode:{str(keycode)}  modifiers:{str(modifiers)}')
    hidmod = 0
    if modifiers & 0x0040:
        hidmod |= 0x01
    if modifiers & 0x0001:
        hidmod |= 0x02
    if modifiers & 0x0100:
        hidmod |= 0x04
    if modifiers & 0x0400:
        hidmod |= 0x08
    if modifiers & 0x0080:
        hidmod |= 0x10
    if modifiers & 0x0002:
        hidmod |= 0x20
    if modifiers & 0x0200:
        hidmod |= 0x40
    if modifiers & 0x0800:
        hidmod |= 0x80
    hidcode = HIDCode[keycode]
    if OS == 'ios' and keycode == 13:
        hidcode = 0x58
    logging.debug(f'hidcode:{str(hidcode)}  hidmod:{hidmod}')
    for i in range(6):
        if keys[i] == 0:
            if down == True:
                keys[i] = hidcode
                break
        elif keys[i] == hidcode:
            if down == False:
                keys[i] = 0
            else:
                break
    atcmd = "AT+BLEKEYBOARDCODE={:02x}-00".format(hidmod)
    zerocmd = ""
    for i in range(6):
        if keys[i] != 0:
            atcmd += "-{:02x}".format(keys[i])
        else:
            zerocmd += "-00"
    atcmd += zerocmd + "\r"
    logging.debug(f'atcmd:{atcmd}')
    ser.write(atcmd.encode());


# MAIN 
logger = logging.getLogger()
logging.getLogger().addHandler(logging.StreamHandler())
if (debug):
	logger.setLevel(logging.DEBUG)

try:
    if (sys.argv[1]=='no-serial'): 
        noSerial = True
        if os.name == 'nt':
            SERIAL_TERMINAL = 'COM7'
        elif os.name == 'posix':
            if (os.path.isfile('.serialDemo')):	
            	with open('.serialDemo') as f: SERIAL_TERMINAL = f.read()
            else:
            	logger.critical('no-serial is set to true.. Please make sure you have already run \'python resources\demoSerial.py\' from a different shell')
            	exit()
except IndexError:
	noSerial = False

if not noSerial:
    SERIAL_TERMINAL = '/dev/ttyUSB0' if (os.name=='posix') else 'COM6'
# Some helper functions for our pygame window



## Main. This loads the window

pygame.init()
pygame.display.set_icon(pygame.image.load('resources/logo.png'))
pygame.display.set_caption('RelayKeys Capture Window')
size = (200,200)
screen = pygame.display.set_mode (size)
c = pygame.time.Clock ()
going = True

# Look for Adafruit CP2104 break out board or Feather nRF52. Use the first 
# one found. Default is /dev/ttyUSB0 Or COM6 (Windows)
# tty for Bluetooth device with baud
# NB: Could be p.device with a suitable name we are looking for. Noticed some variation around this

for p in serial.tools.list_ports.comports():
    if "CP2104" in p.description or "nRF52" in p.description:
        logging.debug(f'serial desc:{str(p)}')
        SERIAL_TERMINAL = p.device
        break
with serial.Serial(SERIAL_TERMINAL, BAUD, rtscts=1) as ser:
    # TODO check for OK or ERROR
    ser.write("AT\r".encode())
    time.sleep(1)
    ser.flushInput()
    # ser.write("ATI\r".encode())
    # time.sleep(1)
    ser.write("ATE=0\r".encode())
    time.sleep(1)
    ser.flushInput()
    ser.write("AT+BLEHIDEN=1\r".encode())
    time.sleep(1)
    ser.flushInput()
    ser.write("ATZ\r".encode())
    while going:
        for e in pygame.event.get ():
            # print (e)
            if e.type == QUIT:
                going = False
                pygame.quit()
                sys.exit()
            elif e.type == KEYDOWN:
                mkHID(e.key, e.mod, True)

            elif e.type == KEYUP:
                mkHID(e.key, e.mod, False)

        ser.flushInput()
        pygame.display.flip()
        c.tick(40)