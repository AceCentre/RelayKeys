# Developing without a board

If you are developing the 'server' side of things and want to try out the code you can run this without any hardware by having a null serial terminal. To do this, in a terminal run:

```
python resources/demoSerial.py
```

then in another terminal run

```
python relayekeysd.py --noserial
```

NB: Only tested on MacOS but should work on any posix system. For Windows simply give a COM port that doesn't exist.
