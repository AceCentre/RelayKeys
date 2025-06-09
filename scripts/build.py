# To build you need to install NSIS, And the Simple Service plugin: https://nsis.sourceforge.io/NSIS_Simple_Service_Plugin
# You also need pyinstaller installed

import os
import shutil
import subprocess
from pathlib import Path

# Change to the project root directory (parent of scripts)
project_root = Path(__file__).parent.parent
os.chdir(project_root)


def moveTree(sourceRoot, destRoot):
    if not os.path.exists(destRoot):
        return False
    ok = True
    for path, dirs, files in os.walk(sourceRoot):
        relPath = os.path.relpath(path, sourceRoot)
        destPath = os.path.join(destRoot, relPath)
        if not os.path.exists(destPath):
            os.makedirs(destPath)
        for file in files:
            destFile = os.path.join(destPath, file)
            if os.path.isfile(destFile):
                print("Skipping existing file: " + os.path.join(relPath, file))
                ok = False
                continue
            srcFile = os.path.join(path, file)
            # print "rename", srcFile, destFile
            os.rename(srcFile, destFile)
    for path, dirs, files in os.walk(sourceRoot, False):
        if len(files) == 0 and len(dirs) == 0:
            os.rmdir(path)
    return ok


# Copy the example relaykeys example. This is hacky.
with open("examples/relaykeys-example.cfg") as f:
    with open("relaykeys.cfg", "w") as wf:
        wf.write(f.read())

# Build the spec files
for script, exename, console in [
    ("relaykeysd.py", "relaykeysd", True),
    ("relaykeysd-service.py", "relaykeysd-service", True),
    ("relaykeysd-service-stop.py", "relaykeysd-service-stop", True),
    ("poll_devname.py", "poll_devname", True),
    ("relaykeys-cli.py", "relaykeys-cli", True),
    ("relaykeys-cli.py", "relaykeys-cli-win", False),
    ("relaykeys-qt.py", "relaykeys-qt", False),
]:
    with open("relaykeys.spec.ini", "rb") as inf:
        data = str(inf.read(), "utf8").format(
            COL_NAME=exename,
            CONSOLE="True" if console else "False",
            SCRIPT=script,
            EXE_NAME=exename,
        )
        with open(f"{exename}.spec", "w") as wf:
            wf.write(data)

# first clear out the dist folder..
# os.system("rd /s /q dist")
# os.system("md ./dist")

# Do a pyinstaller on these files
for spec in [
    "relaykeysd.spec",
    "relaykeys-cli.spec",
    "poll_devname.spec",
    "relaykeys-cli-win.spec",
    "relaykeys-qt.spec",
]:
    subprocess.run(["pyinstaller", "-y", spec])

# remaining files that dont fit the standard spec
if os.name == "nt":
    subprocess.run(["pyinstaller", "-y", "relaykeysd-service.spec"])
    subprocess.run(["pyinstaller", "-y", "relaykeysd-service-stop.spec"])
    subprocess.call(
        [
            "pyinstaller",
            "-y",
            "--windowed",
            "--onefile",
            "--distpath",
            "dist/relaykeysd/",
            "-i",
            "assets/icons/logo.ico",
            "./assets/mouserepeat.py",
        ]
    )

# Create a PDF of the readme - and in future any other docs..
# NB: I realise the next lines are insane. I'm in a hurry
for doc in ["README.md"]:
    os.system("python -m markdown " + doc + "> README.html")

# Copy all the exe's into one dir - we will use the relaykeysd directory for this
# for item in ["blehid.pyd",r".\dist\relaykeysd-service\relaykeysd-service.exe",r".\dist\relaykeys-cli\relaykeys-cli.exe",r".\dist\relaykeys-cli-win\relaykeys-cli-win.exe",r".\dist\relaykeys-qt\relaykeys-qt.exe"]:
#    os.system("copy " + item + r' dist\relaykeysd ')

# Merge all directories
if os.name == "nt":
    for item in [
        r"dist\relaykeysd-service",
        r"dist\relaykeysd-service-stop",
        r"dist\relaykeys-cli",
        r"dist\poll_devname",
        r"dist\relaykeys-cli-win",
        r"dist\relaykeys-qt",
    ]:
        moveTree(item, r"dist\relaykeysd")
if os.name == "posix":
    for item in [
        r"dist/relaykeys-cli",
        r"dist/relaykeys-cli-win",
        r"dist/relaykeys-qt",
    ]:
        moveTree(item, r"dist/relaykeysd")

# Logfile may not exist if its not been run
logfile = Path("logfile.txt")
logfile.touch(exist_ok=True)

# Copy some other stuff to Dist
for item in [
    "relaykeys.cfg",
    "logfile.txt",
    "LICENSE",
    "README.html",
    "macros",
]:
    if os.path.isdir(item):
        shutil.copytree(item, r"dist/relaykeysd/" + item, dirs_exist_ok=True)
    else:
        shutil.copy(item, r"dist/relaykeysd")

# Copy keymaps from the new location
if os.path.isdir("src/relaykeys/cli/keymaps"):
    shutil.copytree("src/relaykeys/cli/keymaps", r"dist/relaykeysd/cli_keymaps", dirs_exist_ok=True)

# Bit messy this.. but cant figure out a neater way. Logo needs to go to resources dir for notifications
os.makedirs(r"dist/relaykeysd/resources", exist_ok=True)
shutil.copy(r"assets/icons/logo.png", r"dist/relaykeysd/resources")

# Run the nsis
if os.name == "nt":
    subprocess.run([r"C:\Program Files (x86)\NSIS\makensis.exe", "scripts/build-installer.nsi"])
if os.name == "posix":
    plist = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>KeepAlive</key>
	<true/>
	<key>Label</key>
	<string>RelayKeysD</string>
	<key>ProgramArguments</key>
	<array>
		<string>/Applications/RelayKeys/RelayKeysd.app</string>
	</array>
	<key>RunAtLoad</key>
	<true/>
</dict>
</plist>
    """
    # Write dir
    # Write the Plist to the dmg
    file = open("dist/relaykeysd/RelayKeys.plist", "w")
    file.write(plist)
    file.close
    # Lets just rename the dir - A user can just dump this in their Applications dirs
    os.system("mv dist/relaykeysd dist/RelayKeys")
