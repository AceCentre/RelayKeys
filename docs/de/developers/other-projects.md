# Stand der Technik/verwandte Projekte

### Andere Projekte / Ähnliche Arbeiten / Inspiration

* [Die originalen RelayKeys von Harold Pimental](https://haroldpimentel.wordpress.com/2016/09/08/bluetooth-keyboard-switch-with-arduino/).
* **bbx10**in den Adafruit-Foren.**bbx10** hat die Ascii-zu-HID-Übersetzungsfunktion entwickelt. Ein großes Dankeschön – der Code gehört derzeit größtenteils ihm. Er hat auch einige der anfänglichen Geschwindigkeitsprobleme gelöst, die wir hatten. Sie können den vollständigen Thread lesen[here](https://forums.adafruit.com/viewtopic.php?f=53\&t=145081\&start=15) .
* [HID-Relay](https://github.com/juancgarcia/HID-Relay)aus[Juancgarcia](https://github.com/juancgarcia) . Ich habe nicht wirklich viel Zeit damit verbracht, mir das anzuschauen – aber es sieht ordentlich aus. Konvertiert Hardware-Tastaturen in Bluetooth.
* [232Key](https://www.232key.com/index.html)- Konvertiert serielle Geräte in Tastaturen. Irgendwie umgekehrt zu dem, was wir wollen.
* [BL\_keyboard\_RPI](https://github.com/quangthanh010290/BL\_keyboard\_RPI). Verwandelt einen Pi in einen Tastaturemulator
* [ESP32\_mouse\_keyboard](https://github.com/RoganDawes/esp32\_mouse\_keyboard). Verwendet einen ESP32 als Maus/Tastatur über die serielle Schnittstelle. Sehr ähnliche Idee. (Sehen[issue 39](https://github.com/AceCentre/RelayKeys/issues/29) Einzelheiten hierzu im Zusammenhang mit der Verwendung von VNC (TY[@RoganDawes](https://github.com/RoganDawes) )

### AAC-Projekte

* [MacroServerMac](http://github.com/willwade/MacroServerMac)war ein Versuch, einen Mac-Port von „MacroServer“ zu erstellen, entwickelt von[JabblaSoft](http://jabblasoft.com) für MindExpress. Dies ist ein Protokoll für die Kommunikation über einen TCP/IP-Stack. Das ist ganz nett – aber wenn Sie sich in einer Schule oder einem Unternehmen befinden, ist es oft eingeschränkt, anderen Computern den Zugriff auf das Netzwerk auf diese Weise zu erlauben. Es kann auch ziemlich flockig sein
* [Liberator](http://liberator.co.uk)/[PRC](http://prentrom.com) - die beste kommerzielle Lösung für AAC haben, die es gibt. Sie können entweder ein USB-Kabel anschließen oder einen Bluetooth-Dongle verwenden, um eine Verbindung mit einem anderen Computer herzustellen. Es ist großartig – steht Ihnen aber leider nur zur Verfügung, wenn Sie eines ihrer Geräte verwenden.
* [Dynavox](http://tobiidynavox.com)verwendet, um das zu machen[AccessIT](http://www.spectronics.com.au/product/accessit) . Eine ähnliche Idee, aber mit Infrarot statt Radio/Bluetooth. Es war ziemlich teuer, aber viele Leute liebten seine Einfachheit. In jüngerer Zeit haben sie dies mit wieder zum Leben erweckt[AccessIT 3](https://www.tobiidynavox.com/products/accessit-3) . Beachten Sie, dass es nur in der Snap-Software funktioniert – und nicht für jedes Gerät. Nur ein weiteres Windows-Gerät. Sie benötigen außerdem einen USB-Anschluss an dem Gerät, an das Sie eine Verbindung herstellen.
* Die AAC-Welt versucht seit Jahren, Standards dafür zu schaffen. Und einige haben es geschafft. Kasse[AACKeys](https://aacinstitute.org/aac-keys/) und das „GIDEI“-Protokoll – das mittlerweile etwas veraltet wirkt, aber ein großartiger Versuch ist, die Kommunikation zwischen AAC-Geräten und anderen Systemen über die serielle Schnittstelle zu standardisieren.

### Nicht-behinderungsbezogene Produkte

* Die[Buffalo BSHSBT04BK](http://buffalo.jp/product/peripheral/wireless-adapter/bshsbt04bk/) war ziemlich ordentlich. Das gibt es immer noch in Japan und es macht einen sehr ähnlichen Job
* Der[IOGEAR KeyShair](https://www.iogear.com/product/GKMB02) (jetzt eingestellt) sah aus wie genau der gleiche Dongle – aber mit anderer Software.

Beide Produkte reagierten jedoch nicht zuverlässig auf Software-Tastaturen (auf dem Bildschirm).
