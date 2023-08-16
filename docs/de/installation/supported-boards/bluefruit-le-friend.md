# Bluefruit LE Freund

![](<../../.gitbook/assets/image (4).png>)

{% hint style="info" %}
Obwohl es funktionieren _sollte_ - und wir versprechen Ihnen, dass es _funktioniert_ hat - ist etwas an der Funktionalität, die mit dem LE-Freund arbeitet, kaputt gegangen. Daher unterstützen wir dies im Moment **offiziell** nicht
{% endhint %}

* [Installieren Sie den CP2104-Treiber](https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers)
* Aktualisieren Sie ihn auf 0.8.1. Der einfachste Weg, dies zu tun, ist die Verbindung mit der Bluefruit-App - sie aktualisiert ihn automatisch, falls erforderlich.
* Einstecken
* Schalten Sie den Schalter am Gerät in den CMD-Modus.
* Öffnen Sie ein serielles Terminal und stellen Sie eine Verbindung zum Gerät her (genaue Einstellungen für Ihr Betriebssystem finden Sie [hier] (https://learn.adafruit.com/introducing-adafruit-ble-bluetooth-low-energy-friend/terminal-settings#terraterm-windows-5-2)).
* Schalten Sie den HID-Modus ein. Mehr Informationen [hier](https://learn.adafruit.com/introducing-adafruit-ble-bluetooth-low-energy-friend/ble-services#at-plus-blehiden-14-31). Um genau zu sein - geben Sie folgendes in Ihr serielles Terminal ein
```
AT+BLEHIDEN=1
ATZ
```

(Nach jedem Eintrag sollte 'OK' erscheinen)

* Als nächstes ändern Sie die Standardgeschwindigkeit, d.h. geben Sie folgendes in Ihr serielles Terminal ein:
```
AT+BAUDRATE=115200
```
* Als nächstes versetzen Sie das Gerät in den [DATA-Modus](https://learn.adafruit.com/introducing-adafruit-ble-bluetooth-low-energy-friend/uart-test#blefriend-configuration-6-3) (schieben Sie den Schalter).
* Schließlich aktualisieren Sie die Datei relaykeys.cfg mit
```
baud = 115200
```

(Oder jede andere Geschwindigkeit, die Sie wünschen)