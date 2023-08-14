# Architektur von RelayKeys

![RelayKeys-Skizze](../.gitbook/assets/untitled\_page.png)

RelayKeys ist eine Mischung aus einem Open-Hardware-Board, das über Bluetooth LE kommuniziert und als BLE-HID-Gerät (d. h. eine Tastatur/Maus) fungiert, das emulieren kann**alle** Tastaturtasten und deren Modifikatoren sowie Mausbewegungen. (4). Dies wird durch eine serielle Verbindung von einem Gerät gesteuert – entweder kabelgebunden (z. B. als USB-Dongle) oder drahtlos (z. B. als serielles BLE-Gerät).\ \ Wir haben einen RPC-Server (2) für einen Desktop-Computer entwickelt, der die Softwareverbindung vereinfacht den seriellen Bus und ermöglicht es uns, eine einfachere Möglichkeit zum Senden von Befehlen an das Gerät zu schaffen als AT-Befehle. Dies geschieht entweder direkt über den RPC-Server (_Daemon_) oder über einen**Befehlszeilenschnittstelle** (_CLI_). \*\* \*\* Zur Demonstration haben wir auch eine kleine grafische Schnittstellenanwendung (_RK-Desktop_, auch als Relaykeys-_QT-Anwendung_ bezeichnet) (1).

Wenn Sie Software erstellen und von den Funktionen von RelayKeys profitieren möchten, können Sie Befehle entweder an den RPC-Server (2) oder über unsere CLI (1) oder, wenn Sie möchten, direkt an die serielle Schnittstelle (6) schreiben. Dies kann seriell verkabelt oder drahtlos sein, wenn Sie das Gerät in den drahtlosen Modus versetzen (5). Auch wenn Sie unsere Hardware ignorieren möchten, bitten wir die Entwickler von Hilfstechnologien, das Kopieren der Befehlsstruktur auf einer dieser Ebenen in Betracht zu ziehen, um eine offene Entwicklung zu ermöglichen.

Das Arduino-basierte Board ist derzeit ein**Adafruit nrf52840 Express oder Adafruit nrf52840 itsybitsy** .

## Anatomie der Dateien

*  `arduino/` - Firmware für das Arduino-Board
*  `docs/` - VuePress-Dokumente fürhttp://acecentre.github.io/relayKeys/.  Build-Skript ist**docs-deploy.sh**
*  `resources/` - Hilfsdateien für die Entwicklung (z. B `demoSerial.py` das vorgibt, ein angeschlossenes Arduino-Board zu sein, viewComPorts, das die verbundenen COM-Ports ausgibt), AAC-Software-Seitensätze und all-keys.txt, das eine Ausgabe aller von RelayKeys unterstützten Schlüssel ist. Beachten Sie auch die Entwicklungsdateien - `relaykeys-pygame` Und `relaykeys.py` - das sind abgespeckte Versionen des gesamten Projekts. Nützlich zum Debuggen und Testen von Dingen ohne den Daemon-Server. Beweg dich einfach `relaykeys.py` in das Stammverzeichnis, damit es funktioniert.
*  `blehid.py` - Bibliothek/Importdatei, die von Relaykeysd verwendet wird. Enthält die Funktion, die den AT-Befehl an den seriellen Port schreibt, den seriellen Port initialisiert und Tastatur-/Mauscodes sendet.
*  `build.py`, `buildinstaller.nsi` - Erstellen Sie Dateien, um dieses Projekt in ein Installationsprogramm umzuwandeln. Laufen `python build.py` um den Build auszulösen.
*  `docs-deploy.sh` – Stellt die Dokumentation auf der Github-Seiten-Site bereit.
*  `relaykeys-cli.py` – Dies ist die Befehlszeilenschnittstellenversion von Relaykeys. Stellt eine Verbindung zum Daemon-Server her.
*  `relaykeys-example.cfg` – Die Standardkonfigurationsdatei. Beachten Sie, dass dies bei der Installation an den richtigen Speicherort kopiert und als Standardkonfiguration verwendet wird. Beachten Sie die auskommentierten Baud- und Entwicklungszeilen. Dev behebt das Problem `COM` Port, wenn der COM-Port-Suchcode nicht funktioniert
*  `relaykeys-qt.py` - Die GUI-Version unserer Relakeys-Test-App.
*  `relaykeys.spec.ini` – Wird für den NSIS-Build verwendet (d. h `buildinstaller.nsi`)
*  `relaykeysclient.py` – Die Hauptbibliotheksdatei, die von den Versionen -cli und -qt verwendet wird. Verbindet sich mit dem Server.
*  `relaykeysd-service-restart.bat`, `relaykeysd-service.py` – Die Windows-Dienstanwendung
*  `relaykeysd.py` - Der Dämon. Dies wird im Hintergrund ausgeführt – und vom Dienst gesteuert. Wenn Sie RelayKeys testen möchten, führen Sie zuerst diese Datei aus und lassen Sie sie laufen. z.B `python relakyeysd.py &&`. Beachten Sie die Befehlszeilenflags im Header.

## Schritte zum Ausführen von RelayKeys (Methode ohne Installationsprogramm)

_Voraussetzungen_

* [Python 3 installieren](https://www.python.org/downloads/windows/)
* Haben Sie Zugriff auf ein Arduino-Board Nrf52840. zB der Adafruit nrf52840 Express

1. Besorgen Sie sich ein nrf52840-Board und laden Sie den Arduino-Code darauf. Stecken Sie es in einen USB-Steckplatz Ihres Computers
2. Überprüfen Sie, ob Ihr Arduino wie erwartet funktioniert. Suchen und notieren Sie den COM-Port, um den es sich handelt ([im Gerätemanager gefunden](https://www.sevenforums.com/attachments/hardware-devices/263068d1486601972t-com-port-missing-device-manager-com-port-pic.jpg) )
3. Laden Sie den Code an einen sinnvollen Ort herunter – z `git clone https://github.com/AceCentre/RelayKeys.git`
4. Kopiere das `relaykeys-example.cfg` Datei z.B `copy relaykeys-example.cfg relaykeys.cfg`
5. Installationsanforderungen, z. B `pip install -r requirements.txt`
6. Führen Sie den Daemon-Code aus. `python relaykeysd.py`
7. Koppeln Sie Ihr Relaykeys Arduino mit einem PC/Mac/iOS/Android-Gerät und öffnen Sie eine Textdatei
8. Testen Sie es mit der CLI-Datei, z. B `python relaykeys-cli.py type:Hello`

Wenn alles wie erwartet funktioniert, sollten Sie die Eingabe auf dem zweiten Gerät sehen. Wenn nicht, schauen Sie sich die Protokolldateien an.

Ein Problem könnte sein, dass der Daemon den COM-Port nicht finden kann. Sie können dies beheben, indem Sie den in Schritt 2 gefundenen COM-Port reparieren und in die Konfigurationsdatei einfügen. zB hinzufügen `dev=COM6` wenn der COM-Port 6 ist. Weitere Informationen finden Sie hier[here](../../developers/relaykeys-cfg.html#dev-defining-your-port-of-the-relaykeys-hardware)
