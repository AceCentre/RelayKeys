# Details zur Konfigurationsdatei

## Einführung

Im selben Verzeichnis wie Relaykeys befindet sich eine Datei `relaykeys.cfg`

Es sieht aus wie das:

```
[server]
host = 127.0.0.1
port = 5383
username = relaykeys
password = QTSEOvmXInmmp1XHVi5Dk9Mj
logfile = logfile.txt

[client]
host = 127.0.0.1
port = 5383
username = relaykeys
password = QTSEOvmXInmmp1XHVi5Dk9Mj
toggle = 1
togglekey = A
togglemods = RALT

[cli]
keymap_file = us_keymap.json
```

Sie können jedoch jederzeit die Einstellungen ändern**Achten Sie darauf, dass Benutzername und Passwort identisch sind** - Andernfalls kann das CLI-Programm nicht mit dem Dienst kommunizieren.

Beachten Sie die Keymap-Datei. Dieses befindet sich im Unterverzeichnis**cli\_keymaps** . Wenn Sie möchten, können Sie hier mehrere Tastaturbelegungen verwenden und mithilfe von zwischen ihnen wechseln[cli mit -c](../using-relaykeys/relaykeys-cli.md#defining-a-keymap-c)

Jede Datei ist eine JSON-Datei (Tipp: Verwenden von[jsonlint](https://jsonlint.com) um zu überprüfen, ob die Formatierung in Ordnung ist) sieht in etwa wie unten aus, wobei die Zeichenfolge abhängig von den gesendeten Zeichen gesendet wird. z.B. auf einer britischen Tastatur**! wird durch Drücken von Shift und 1 gesendet.**

```
{
    "\r": [null, null],
    "\t": ["TAB", []],
    " ":  ["SPACE", []],
    "`":  ["BACKQUOTE", []],
    "~":  ["BACKQUOTE", ["LSHIFT"]],
    "!":  ["1", ["LSHIFT"]]
}
```

## Dev – Definieren Sie Ihren Port der RelayKeys-Hardware

Die RelayKeys-Software versucht, die RelayKeys-Karte automatisch zu finden. Wenn Sie ein Gerät mit mehreren angeschlossenen COM-Anschlüssen oder Geräten mit ähnlicher Funktionalität haben, kann es zu Schwierigkeiten kommen. Wenn ja, versuchen Sie es_Festsetzung_ den COM-Port.

1. Greifen Sie auf den Geräte-Manager zu. Suchen Sie in Windows nach „Geräte-Manager“.

[![Bild von Gyazo](https://i.gyazo.com/0b327be4a6ad9ea569da378e1f1d7a1a.gif) ](https://gyazo.com/0b327be4a6ad9ea569da378e1f1d7a1a)

1. Klicken Sie auf Ports. Wenn Sie nur RelayKeys angeschlossen haben, sollte ein Gerät angezeigt werden. Wenn Sie viele sehen, ziehen Sie den Stecker heraus und schließen Sie ihn wieder an, um herauszufinden, um welchen COM-Anschluss es sich handelt.

[![Bild von Gyazo](https://i.gyazo.com/0b327be4a6ad9ea569da378e1f1d7a1a.gif) ](https://gyazo.com/0b327be4a6ad9ea569da378e1f1d7a1a)

1. Notieren Sie sich die Nummer und bearbeiten Sie Ihre RelayKeys-CFG-Datei. Suchen Sie in Windows nach „RelayKeys config“ – und öffnen Sie es mit Notepad.

[![Bild von Gyazo](https://i.gyazo.com/427603ca7c287942ad92ccd823c0f64d.gif) ](https://gyazo.com/427603ca7c287942ad92ccd823c0f64d)

1. Typ `dev = COM3` Wo**COM3** ist Ihre Portnummer, die Sie in Schritt 2-3 gefunden haben.
