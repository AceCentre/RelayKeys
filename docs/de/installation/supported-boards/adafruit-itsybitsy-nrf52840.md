# Adafruit itsybitsy nRF52840

![](<../../.gitbook/assets/image (3).png>)

Verwenden Sie entweder die UF2-Methode (Ziehen und Ablegen) oder die mehr Schritte umfassende Arduino-Upload-Methode.
Für die UF2-Methode

* Laden Sie die UF2-Datei für das itsybitsy _Board in der aktuellen Version_ herunter
* Doppelklicken Sie auf die Reset-Taste. Sie erhalten dann ein USB-Laufwerk auf Ihrem Computer. Ziehen Sie die UF2-Datei per Drag and Drop in das Stammverzeichnis dieses Laufwerks.
* Es SOLLTE die Verbindung zu Ihrem PC trennen, wenn es erfolgreich war - aber wie gesagt, die Loghts sollten die Farbe auf Grün ändern.
* Weitere Einzelheiten finden Sie in den Schritten [hier] (https://learn.adafruit.com/adafruit-metro-m0-express/uf2-bootloader-details#entering-bootloader-mode-2929745)

Oder die Arduino-Upload-Methode.

* Überprüfen Sie die Einstellungen Ihrer [Arduino IDE](https://learn.adafruit.com/bluefruit-nrf52-feather-learning-guide/arduino-bsp-setup) (denken Sie daran, dass wir das nRF52840-Board verwenden!)
* Laden Sie den [sketch](../../../arduino/arduino_nRF52840/arduino_nRF52840.ino) auf Ihre Feder hoch.
* Führen Sie den serverseitigen Code aus.
* Geschafft!