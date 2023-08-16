# Befehlszeilenverwendung

### Kommandozeilen-Flags

Wir haben eine Kommandozeilen-Schnittstelle entwickelt, mit der Sie Maus- und Tastaturbefehle an Ihre RelayKeys-Hardware senden können.

Um es auszuführen, rufen Sie

relaykeys-cli.exe Befehl:Daten".

oder wenn es in reinem Python ausgeführt wird

python relaykeys-cli.py command:data".

und die nicht-verbale, nicht-fensterspezifische Version

python relaykeys-cli-win.py command:data".

Wobei "Befehl" und "Daten" unten angegeben sind.

{% hint style="info" %}
Denken Sie daran, Ihre Anwendung entsprechend zu ändern Wir verwenden in dieser Dokumentation regelmäßig den Begriff für die Kommandozeilenanwendung '_relaykeys-cli_'. Häufig werden Sie jedoch die Anwendung '**relaykeys-cli-win.exe**' verwenden wollen, die etwas schneller läuft und keine Druckausgabe hat. Verwenden Sie diese Anwendung für Ihren Standardaufruf von relaykeys aus anderen Anwendungen. Wenn Sie alle Fehler sehen wollen, verwenden Sie '_relaykeys-cli.exe_'
{% endhint %}

{% hint style="info" %}
Wenn Sie mit dem Code entwickeln, müssen Sie sicherstellen, dass der Server läuft, wenn Sie die Cli-Dateien aufrufen. Der [server (aka Daemon)](../developers/relaykeys-daemon.md) ist der Code, der diese Befehle in die korrekte AT-Syntax umwandelt und auf den Com-Port zugreift
{% endhint %}

### Definieren einer Keymap -c

Keymap-Dateien befinden sich im Ordner [**cli_keymap**](https://github.com/AceCentre/RelayKeys/tree/master/cli_keymaps). Sie können wählen, welche Keymap-Datei die CLI in der cfg verwenden soll, indem Sie den Dateinamen der Variable keymap_file zuweisen (siehe [hier](https://github.com/AceCentre/RelayKeys/blob/12d3eadca2cea53561a5a3979562aae8b4b6cd7c/relaykeys-example.cfg#L17))

Standardmäßig wird die **us_keymap.json** geladen.
Um relaykeys-cli mit einer anderen Tastaturbelegung laufen zu lassen, ändern Sie entweder die cfg-Einstellung [oder verwenden Sie das Flag -c](../developers/relaykeys-cfg.md) in der cli-Anwendung. z.B..

`relaykeys-cli.exe -c .\relaykeys-example.cfg type:@`

Weitere Informationen über das Format finden Sie [hier](../developers/relaykeys-cfg.md#introduction)

### Befehl: einfügen

Dies nimmt die Zwischenablage des Computers (z.B. wenn Sie einen Text kopieren) und fügt die resultierende Zeichenfolge in RelayKeys ein

d.h.

Relais-Schlüssel-cli.exe einfügen".

### Befehl: type:text

Geben Sie die Zeichenfolge nach dem : ein. Beachten Sie, dass Sie Leerzeichen usw. auslassen müssen.

Relais-Schlüssel-cli.exe Typ:Hallo" Welt

#### Ein besonderer Hinweis zum Thema Tippen/Einfügen

Sie können Sonderzeichen senden, die normalerweise verschoben werden, indem Sie die Taste und den Umschaltmodifikator senden (siehe **keyevent** unten). Für die Befehle "Tippen" und "Einfügen" gibt es jedoch einige andere Zeichen, die fest kodiert sind, und die Umwandlung erfolgt im laufenden Betrieb.

Zum Beispiel, um das @-Symbol zu senden:

relaykeys-cli.exe Typ:@`

Alle Codes, die umgewandelt werden, sind unten zu sehen. **NB: \t = Tabulator \r\n sind Zeilenumbrüche~**

### Befehl: keypress:KEY,MODIFIER

Sendet den KEY und einen beliebigen Modifikator, zum Beispiel:

relaykeys-cli.exe Tastendruck:A

Emuliert das Drücken und Loslassen des Buchstabens "A". Was ist mit einer Verschiebung?

relaykeys-cli.exe Tastendruck:A,LSHIFT`

Emuliert das Drücken des A mit der linken Umschalttaste, d.h. das A wird groß geschrieben.

Relais-Tasten-Cliexe Tastendruck:RECHTSPFEIL,LSHIFT,LCTRL`

Drücken Sie die rechte Pfeiltaste, die linke Shit-Taste und die linke Steuertaste (um das nächste Wort in Programmen wie Word auszuwählen).

#### Modifikatoren

* Linke Steuerung/CTRL: `LCTRL`
* Linke Umschalttaste: `LSHIFT`
* Linke Alt/Alt-Taste: "LALT".
* (Linke) Meta/Windows-Taste/Mac-Taste/Befehlstaste: LMETA **Hinweis: Unter Windows gibt es im Allgemeinen nur eine Windows-Taste. Benutze also LMETA, um das Drücken der Windows-Taste zu emulieren**
* Rechte Steuerungstaste/CTRL: `LCTRL`
* Rechte Umschalttaste: `RSHIFT`
* (Rechts) Meta/Windows-Taste/Mac-Taste/Befehlstaste: `RMETA`

{% hint style="info" %}
Wenn Sie zwei Tasten mit einem Modifikator senden wollen, senden Sie die **Taste** - **dann** **Modifikator**. Z.B. `Tastendruck:C,LCTRL` - nicht andersherum!&#x20;
{% endhint %}

{% hint style="warning" %}
Wenn Sie an iOS oder einen Mac senden, denken Sie daran, dass dort die Befehlstaste (LMETA) verwendet wird - oft dort, wo Windows die STRG-Taste verwendet. Lesen Sie [hier] (https://support.apple.com/en-us/HT201236) für weitere Beispiele
{% endhint %}

Wir haben auch eine begrenzte Anzahl von **Verbraucher-Schlüsseln - und zwar volumenbezogen (wenn Sie weitere benötigen, lassen Sie es uns wissen** (https://github.com/AceCentre/RelayKeys/issues/26)**)**

* Lauter: `VOLUP`
* Lautstärke runter: "VOLDOWN".
* Stummschalten: `MUTE`

Alle anderen Schlüssel sind also unten definiert. Wir werden versuchen zu erklären, was diese sind, wenn sie nicht eindeutig sind

<details>

<summary>Keys</summary>

* 0
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]
[...]

</details>

### Befehl: keyevent:KEY,MODIFIER,Up/Down

Emuliert das Halten oder Loslassen einer Taste mit einem Modifier. Zum Beispiel:

Tastenereignis:A,LSHIFT,1`

Emuliert das Drücken von `A` mit `Shift` Down. Zum Loslassen:

Tastenereignis:A,LSHIFT,0`

Ein klassisches Beispiel ist die Emulation des Drückens der Alt-Taste und der Tabulator-Taste. Dies wird häufig verwendet, um zwischen Anwendungen zu wechseln. Hierfür müssten Sie zwei Befehle senden.

```
relaykeys-cli-win.exe" keyevent:TAB,LALT,1
    relaykeys-cli-win.exe" keyevent:TAB,LALT,0
```

### Befehl: mousemove:PixelsRight,PixelsDown

Sendet den Befehl, die Maus x Pixel nach rechts und x Pixel nach unten zu bewegen. Um in die andere Richtung zu gehen, senden Sie negative Zahlen. Z.B. um 10 nach rechts und um 10 nach unten zu gehen

relaykeys-cli.exe mousemove:10,10".

und Links um 10, oben um 10:

relaykeys-cli.exe mousemove:-10,-10`

Geradeaus:

relaykeys-cli.exe mousemove:0,-10`

Gerade nach unten:

relaykeys-cli.exe mousemove:0,10".

Geradeaus rechts:

relaykeys-cli.exe mousemove:10,0".

Gerade links:

relaykeys-cli.exe mousemove:-10,0`

{% hint style="info" %}
Möchten Sie eine Mausbewegung eine Weile lang wiederholen?
Führen Sie die Anwendung **mouserepeat.exe** aus, die Sie im Installationsordner von RelayKeys finden. Führen Sie es mit "mouserepeat.exe -x 10 -y 10" aus, wobei die Richtung, in die Sie die Maus bewegen wollen, anzugeben ist. Dies wird dann so lange wiederholt, bis Sie die Anwendung beenden. Führen Sie dazu ein Powershell-Skript aus:
`Stop-Process -Name "mouserepeat"`
{% endhint %}

### Befehl: mousebutton:Button,Behaviour

Sendet das Drücken der Maustaste. Verfügbare Maustasten:

* L: Links
* R: Rechts
* M: Mitte
* F: Vorwärts blättern
* B: Rückwärts blättern

Verhaltensweisen:

* Klicken
* Doppelklick

Hinweis: Wenn Sie kein Verhalten angeben, wird die Taste für 0 Sekunden gehalten und wieder losgelassen.

Senden Sie einen Doppelklick:

relaykeys-cli.exe Maustaste:L,Doppelklick`

Senden Sie einen Rechtsklick:

relaykeys-cli.exe Maustaste:R,Klick`

**Was ist mit dem Ziehen? **

Aktivieren Sie die Schaltfläche Start ziehen

Relaykeys-cli Maustaste:L,drücken`

Benutzer bewegt die Maus

relaykeys-cli mousemove:x,y`

Benutzer bewegt die Maus weiter

relaykeys-cli mousemove:x,y`

Der Benutzer aktiviert die Schaltfläche Ziehen stoppen

relaykeys-cli mousebutton:0

### Befehl: Verzögerung: nms

Fügt eine Verzögerung hinzu. Besonders nützlich, wenn Sie ein Makro schreiben und warten müssen, bis etwas auf dem Client-Betriebssystem passiert.

relaykeys-cli Verzögerung:1000

Setzt eine Verzögerung von 1 Sekunde ein.

### Geräteverwaltungsbefehle

#### Optionale Zusatzflaggen --notfiy --copy

Bei den folgenden Befehlen können Sie das Flag `--notify` angeben. In diesem Fall wird Ihr Betriebssystem eine Systembenachrichtigung zurückgeben. Nützlich, wenn Sie keinen Zugriff auf die Befehlszeile haben. Wenn Sie möchten, können Sie auch das Flag `--copy` angeben. Damit werden die Ergebnisse an Ihre Zwischenablage zurückgegeben, damit Sie die Daten wieder einfügen können. **Seien Sie vorsichtig damit. Es überschreibt alle Kopieren/Einfügen-Funktionen, die Sie vielleicht schon haben.

relaykeys-cli.exe ble_cmd:devname`

Gibt das aktuell verbundene Gerät zurück

relaykeys-cli.exe ble_cmd:devlist`

Ruft eine Liste der Geräte ab, die sich im Speicher des Geräts befinden

relaykeys-cli.exe ble_cmd:devadd`

Versetzen Sie das Gerät in einen Pairing-Status

relaykeys-cli.exe ble_cmd:devreset`

Zurücksetzen der gesamten gespeicherten Geräte (es ist wie das Löschen des flüchtigen Speichers)

relaykeys-cli.exe ble_cmd:switch`

Schaltet das aktuell angeschlossene Gerät auf das nächste Gerät im RelayKeys-Speicher um

relaykeys-cli.exe ble_cmd:devremove=DEVNAME`

Entfernen Sie nur ein benanntes Gerät aus dem Speicher.

relaykeys-cli.exe ble_cmd:reconnect`

Sagt dem Daemon/Server, dass er versuchen soll, die Verbindung zur seriellen Schnittstelle wieder herzustellen.

relaykeys-cli.exe daemon:switch_mode`

Sagt dem Daemon/Server, dass er versuchen soll, zwischen verkabelten

relaykeys-cli.exe daemon:get_mode`

Gibt den aktuellen Modus zurück

relaykeys-cli.exe daemon:dongle_status`

Gibt zurück, ob er verbunden ist oder nicht

relaykeys-cli.exe ble_cmd:get_mode`&#x20;

Ruft den aktuellen Modus ab - verkabelt oder drahtlos

relaykeys-cli.exe ble_cmd:switch_mode`

Wechselt den Modus von Verkabelt -> Drahtlos und Drahtlos-> Verkabelt.

### Befehl: -f file.txt (Makro)

Erstellen Sie eine Makrodatei, bei der jede Zeile in einer Textdatei ein Cli-Befehl ist. Zum Beispiel **ios_open_notes.txt** im Verzeichnis _macros_ des Installationsordners (d. h. unter _C:\Programme (x86)\Ace Centre\RelayKeys\maccros)\

relaykeys-cli.exe -f ios_open_notes.txt`

oder so

relaykeys-cli.exe -f Dokumente/open_ios_notes.txt`

wo es die Datei aus einem Dateipfad liest... oder...
relaykeys-cli.exe -f ./open_ios_notes.txt`

wo die Datei in dem Ordner gelesen wird, aus dem die aktuelle Exe ausgeführt wird.

wo sich ios_open_notes.txt befindet:

```
keypress:H,LMETA
keypress:SPACE,LMETA
type:notes
delay:500
keypress:ENTER
```

{% hint style="info" %}
Warnung: Es gibt keine Syntaxprüfung für dieses Dokument.
{% endhint %}

{% hint style="info" %}
Sie möchten eine lange Reihe von Mausbefehlen senden und Ihre Bewegungen für ein Skript aufzeichnen? Benutzen Sie die RelayKeys-QT-App und verwenden Sie die Aufzeichnungsmakrofunktion!
{% endhint %}