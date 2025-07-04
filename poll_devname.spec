# -*- mode: python -*-

block_cipher = None

a = Analysis(['poll_devname.py'],
             pathex=['src'],
             binaries=[
             ],
             datas=[
             ("relaykeys.cfg", "."),
             ("src/relaykeys/cli/keymaps", "relaykeys/cli/keymaps"),
             ],
             hiddenimports=["PyQt5.sip","PyQt6.sip","win32timezone"],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='poll_devname',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          icon="assets/icons/logo.ico")

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='poll_devname')

