# Serielle API

### Serielle Befehle

Wenn Sie also direkt mit dem seriellen Gerät kommunizieren wollen - statt über den Server - können Sie das tun. Dazu müssten Sie Ihre Software so schreiben, dass sie die serielle Verbindung öffnet und die richtigen Befehle verwendet, um mit der Hardware zu _sprechen_;

### Verbindung - Baudrate, nr/vid Einstellungen

* Die Baudrate sollte 115200 betragen.
* Hardware-Flusskontrolle CTS/RTS eingeschaltet
* nrfVID = '239A'
* nrfPID = '8029'

Dann senden und empfangen Sie Befehle über die serielle Schnittstelle. Im Folgenden finden Sie eine Liste der Befehle und der zu erwartenden Rückmeldungen

### Maus- und Tastaturbefehle

#### AT+BLEKEYBOARDCODE=TastaturCode

Das Gute an RelayKeys ist, dass wir nicht versuchen, echte Zeichen zu senden - wir senden echte Schlüssel. Das ist gut - denn es bedeutet, dass wir uns nicht mit mehrsprachigen Problemen und unterschiedlichen Tastaturbelegungen herumschlagen müssen. Es bedeutet aber auch, dass der Befehl zum Senden und Drücken einer Taste auf der Tastatur ein wenig entmutigend aussehen kann. So sieht es aus.

`AT+BLEKEYBOARDCODE=02-00-00-00-00-00-00-00`

Dies ist ein ziemlicher Standard, wenn es um einen Tastatur-HID-Code geht. Z.B. [schauen Sie sich das an](https://www.usb.org/sites/default/files/documents/hut1_12v2.pdf), um zu sehen, worum es geht. Kurz und gut:

```
Byte 0: Keyboard modifier bits (SHIFT, ALT, CTRL etc)
    Byte 1: reserved
    Byte 2-7: Up to six keyboard usage indexes representing the keys that are 
              currently "pressed". 
              Order is not important, a key is either pressed (present in the 
              buffer) or not pressed.
```

Der Buchstabe "a" hat zum Beispiel den Verwendungscode 0x04. Wenn Sie ein "A" in Großbuchstaben wünschen, müssen Sie auch die Modifikatorbits von Byte 0 auf "Linksverschiebung" (oder "Rechtsverschiebung") einstellen.

Hinweis: [Schauen Sie sich diese Datei an, um einen Weg zu finden, dies schön zu formatieren](https://github.com/AceCentre/RelayKeys/blob/69fffd89cf5ace9ee74ed6bc4fe958bff4fb3db2/blehid.py#L222)

#### AT+BLEHIDMOUSEMOVE=MouseMoveX,MouseMoveY,0,0

AT+BLEHIDMOUSEMOVE=X,Y,WY,WX`

* X = Rechte Bildpunkte
* Y = Pixel nach unten
* WY = Nach unten blättern
* WX = Nach rechts blättern

MouseMoveX = Pixel RIGHT und MouseMoveY = Pixel DOWN. Also, um nach RECHTS/oben zu gehen = negative Zahlen verwenden.

z.B. Dies verschiebt sie um 10 nach rechts und um 10 nach unten

AT+BLEHIDMOUSEMOVE=10,10,0,0`

#### AT+BLEHIDMOUSEBUTTON=MouseButton

AT+BLEHIDMOUSEBUTTON=Button[,Action]`

Button ist einer der

* l = Links
* r= Rechts
* m=Mitte
* b=Maus rückwärts
* f=Maus vorwärts

NB: Die Funktionen "Maus zurück" und "Maus vor" sind nicht auf allen Betriebssystemen verfügbar.

Aktion ist

* Klicken
* Doppelklick
* O (fungiert als Umschalttaste für Drücken/Loslassen)

z.B..

_Einfacher Klick:_

```
AT+BLEHIDMOUSEBUTTON=l,click
```

_Doppelklick:_

```
AT+BLEHIDMOUSEBUTTON=l,doubleclick
```

### Verbindungsbefehle

#### AT+BLEADDNEWDEVICE

Fügt ein neues Gerät zur zwischengespeicherten Liste der Geräte hinzu. Nach der Eingabe dieses AT-Befehls sollte sich der Benutzer über BLE mit dem Board verbinden. Wenn die Verbindung erfolgreich ist, wird der Name des Geräts in die Liste aufgenommen und das Board verbindet sich mit dem Gerät.

Hinweis: Ein Benutzer kann nur dann ein neues Gerät hinzufügen, wenn die Liste im Cache nicht voll ist. Wenn die Liste voll ist, meldet das Board einen "Fehler". Wenn sich bis zum Timeout (auf 30 Sekunden eingestellt) kein neues Gerät mit dem Board verbindet, wird ein `Timeout Error` zurückgegeben.

#### AT+BLEREMOVEDEVICE="DEVICE_NAME"

Mit diesem AT-Befehl wird der Name des Geräts aus der Cache-Liste entfernt. Der Name des Geräts sollte in Anführungszeichen geschrieben werden. Sie müssen hier sehr genau sein! Wenn `device_name` nicht in der Liste gefunden wird, dann gibt die Karte einen `Error` zurück.

Wenn `Gerätename` aktuell mit einem BLE-Gerät verbunden ist, trennt das Board die Verbindung zu diesem Gerät und entfernt den Gerätenamen aus der Liste.

#### AT+BLECURRENTDEVICENAME

Dieser AT-Befehl gibt den Namen des aktuell verbundenen BLE-Geräts zurück. Wenn das Board nicht mit einem BLE-Gerät verbunden ist, wird `NONE` zurückgegeben.

#### AT+SWITCHCONN

Mit diesem AT-Befehl wird die BLE-Verbindung zum nächsten Gerät in der Cache-Liste umgeschaltet. Das Board wird versuchen, sich mit dem nächsten aufgelisteten Gerät zu verbinden, bis die Zeitüberschreitung eintritt, dann wird "Timeout Error" zurückgegeben und das Board wird versuchen, sich mit dem nächsten im Cache aufgelisteten Gerät zu verbinden... und so weiter.

#### AT+PRINTDEVLIST

Dieser AT-Befehl liefert eine Liste von Gerätenamen.

#### AT+BLEMAXDEVLISTSIZE=NUMBER

Mit diesem AT-Befehl wird die maximal mögliche Anzahl von BLE-Geräten in der Cache-Liste geändert. Die Zahl sollte größer als 0 und kleiner als 15 sein

#### AT+GETMODE

Ruft den aktuellen Modus ab - entweder kabelgebunden oder drahtlos. &#x20;

#### AT+SWITCHMODE

Schaltet den aktuellen Modus von kabelgebunden auf drahtlos um. Oder Drahtlos zu verdrahtet.&#x20;

{% hint style="info" %}
Beachten Sie, wenn das Gerät **NICHT** drahtlos mit RelayKeys verbunden ist, reagiert es nicht mehr. Sie müssen dann die Verbindung auf eine andere Technik umstellen. Siehe [hier](../installation/#wireless-mode) für weitere Details
{% endhint %}