# Erstellen einer Binärdatei

Der Schwerpunkt der Builds liegt auf Windows – wir haben jedoch mit der Arbeit an einem MacOS-Build begonnen.

**Für Windows**

Du brauchst[nsis](http://nsis.sourceforge.io/) installiert und installiert das SimpleSC-Plugin:[https://nsis.sourceforge.io/NSIS\_Simple\_Service\_Plugin](https://nsis.sourceforge.io/NSIS\_Simple\_Service\_Plugin) . \ \ Dann

```
pip install -r requirements.txt
pip install -r equirements-build.txt 
python build.py 
```

Sie erhalten dann eine setup.exe

Wenn Sie eine UF2-Datei für die Firmware erstellen möchten, folgen wir den Anweisungen[diesen Leitfaden](https://learn.adafruit.com/adafruit-metro-m0-express/uf2-bootloader-details#entering-bootloader-mode-2929745) (siehe „Erstellen Sie Ihr eigenes UF2“) – beachten Sie, dass wir auf M4-basierten Platinen arbeiten.

