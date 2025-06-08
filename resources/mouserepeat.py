# This is a little dangerous! Running it with -x 10 -y 10 will continually move the mouse
# You'll need to kill it to stop movmeent
# Build it with pyinstaller --onefile --windowed
import argparse
import subprocess
import time

parser = argparse.ArgumentParser(
    description="Relaykeys calling script. Repeats a mousemovement in x,y direction till hotkey"
)
parser.add_argument(
    "--movex", "-x", dest="movex", default=0, help="move in x pixels right"
)
parser.add_argument(
    "--movey", "-y", dest="movey", default=0, help="move in x pixels down"
)
args = parser.parse_args()


def moveMouse(movex, movey, keepRunning=True):
    while keepRunning:
        # call mousemove:movex,movey
        fileargs = "mousemove:" + str(movex) + "," + str(movey)
        print(fileargs)
        subprocess.call(
            [
                "C:\\Program Files (x86)\\Ace Centre\\RelayKeys\\relaykeys-cli.exe",
                fileargs,
            ],
            shell=True,
        )
        # Prolly wise to put a little delay in..
        time.sleep(0.025)


moveMouse(args.movex, args.movey, True)
