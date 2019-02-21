import os, glob, subprocess

# Build the spec files
for script, exename, console in [ \
    ('relaykeysd.py', 'relaykeysd', True),
    ('relaykeysd-service.py', 'relaykeysd-service', True),
    ('relaykeys-cli.py', 'relaykeys-cli', True),
    ('relaykeys-cli.py', 'relaykeys-cli-win', False),
    ('relaykeys-qt.py', 'relaykeys-qt', False) ]:
  with open("relaykeys.spec.ini", "rb") as inf:
    data = str(inf.read(), "utf8").format(COL_NAME=exename,
                                   CONSOLE="True" if console else "False",
                                   SCRIPT=script,
                                   EXE_NAME=exename)
    with open("{}.spec".format(exename), "w") as wf:
      wf.write(data)

# first clear out the dist folder..
#os.system("rd /s /q dist")
#os.system("md ./dist")
       
# Do a pyinstaller on these files
for spec in ['relaykeysd.spec','relaykeysd-service.spec','relaykeys-cli.spec','relaykeys-cli-win.spec','relaykeys-qt.spec']:
    subprocess.run(["pyinstaller",spec])

# Create a PDF of the readme - and in future any other docs..
# NB: I realise the next lines are insane. I'm in a hurry
for doc in ['README.md']:
    os.system("python -m markdown "+doc+ "> README.html")

# Copy all the exe's into one dir - we will use the relaykeysd directory for this
for item in ["blehid.pyd",r".\dist\relaykeysd-service\relaykeysd-service.exe",r".\dist\relaykeys-cli\relaykeys-cli.exe",r".\dist\relaykeys-cli-win\relaykeys-cli-win.exe",r".\dist\relaykeys-qt\relaykeys-qt.exe"]:
    os.system("copy " + item + r' dist\relaykeysd ')


# Copy some other stuff to Dist
for item in ['relaykeys.cfg','logfile.txt','LICENSE','README.html']:
    os.system("copy "+item+" dist\relaykeysd")

# Run the nsis 
subprocess.run([r"C:\Program Files (x86)\NSIS\makensis.exe","build-installer.nsi"])    