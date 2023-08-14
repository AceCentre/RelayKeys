# Building a binary

Builds are focused on Windows - but we have started to work on a MacOS build.&#x20;

**For Windows**

You need [nsis](http://nsis.sourceforge.io/) installed and install SimpleSC Plugin: [https://nsis.sourceforge.io/NSIS\_Simple\_Service\_Plugin](https://nsis.sourceforge.io/NSIS\_Simple\_Service\_Plugin). \
\
Then

```
pip install -r requirements.txt
pip install -r equirements-build.txt 
python build.py 
```

You will then get a setup.exe

If you wish to create a UF2 file for the firmware we follow [this guide ](https://learn.adafruit.com/adafruit-metro-m0-express/uf2-bootloader-details#entering-bootloader-mode-2929745)(see "Making your own UF2") - making note that we are on M4 based boards.&#x20;

