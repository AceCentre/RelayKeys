#!/usr/bin/python
# Spawn pseudo-tty for input testing.
# Copyright 2010, Canonical, Ltd.
# Author: Kees Cook <kees@ubuntu.com>
# License: GPLv3
import os
import select
import sys

parent, child = os.openpty()
tty = os.ttyname(child)
os.system(f"stty cs8 -icanon -echo < {tty}")
file = open(".serialDemo", "w")
file.write(tty)
file.close()

try:
    os.system("stty cs8 -icanon -echo < /dev/stdin")

    poller = select.poll()
    poller.register(parent, select.POLLIN)
    poller.register(sys.stdin, select.POLLIN)

    running = True
    while running:
        events = poller.poll(1000)
        for fd, event in events:
            if (select.POLLIN & event) > 0:
                chars = os.read(fd, 512)
                if fd == parent:
                    sys.stdout.write(str(chars))
                    sys.stdout.flush()
                else:
                    os.write(parent, str(chars))
finally:
    os.system("stty sane < /dev/stdin")
    os.remove(".serialDemo")
