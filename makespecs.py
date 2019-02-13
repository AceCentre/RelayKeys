
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
