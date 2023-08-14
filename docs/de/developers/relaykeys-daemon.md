# Referenz zum Server (Daemon).

Der_Server_ (_RPC-Server_ oder_Daemon_ (wie wir es manchmal nennen) ist die Komponente, die eine Verbindung zum COM-Port herstellt und den richtigen AT-Befehl an die Platine sendet. Sie können es mit einigen Argumenten steuern

Wenn Sie unser Installationsprogramm verwenden, wird dies als Dienst installiert. Wenn Sie den Code ohne Installation ausführen (oder den Dienst aus irgendeinem Grund deaktivieren), können Sie ihn als ausführen `relaykeysd.py` oder `relaykeysd.exe`

## --noserial

Führen Sie den Daemon aus und versuchen Sie nicht, eine Verbindung zur Hardware herzustellen. Wenn Sie Linux/MacOS verwenden, können Sie eine serielle Schnittstelle vortäuschen[Befolgen Sie diese Tipps](../installation/supported-boards/#developing-without-a-board). Wenn Sie Windows verwenden, legen Sie einfach einen COM-Port in der Konfigurationsdatei fest oder verwenden Sie den `--dev` Option – wählen Sie einfach einen nicht vorhandenen COM-Port

## --dev

Erzwingen Sie, dass der Daemon einen COM-Port verwendet, anstatt ihn automatisch zu erkennen.

z.B

`python Relaykeysd.py --noserial --dev=COM7`

Weitere Informationen finden Sie unter[here](../../developers/relaykeys-cfg.html#dev-defining-your-port-of-the-relaykeys-hardware)

## --debuggen

Legt eine ausführlichere Debug-Ausgabe auf der Konsole fest.

## --pidfile=Datei

Geben Sie eine PID-Datei an, die der Daemon erstellen soll – oder verlinken Sie darauf.

**Standard: pidfile**

## --logfile=Protokolldatei

Datei, die als Protokolldatei für die Debugging-Meldungen verwendet werden soll.

**Standard: Protokolldatei**

## --config=configfile

Datei, die als Konfigurationsdatei verwendet werden soll. Weitere Informationen finden Sie unter[here](relaykeys-cfg.md)

**Standard: Relaykeys.cfg**

## --**ble\_mode=True|False**

Verwenden Sie den Daemon im drahtlosen (ble\_mode) oder kabelgebundenen Modus.

**Standard: false**
