# Drahtloser Modus

{% hint style="warning" %}
Warnung: Dieser Modus ist definitiv etwas verzögert und kann kompliziert einzurichten sein&#x20;
{% endhint %}

Beachten Sie, dass dieser Modus bei Geräten nützlich ist, an die Sie nichts anschließen können. Die Einrichtung kann sich _fremd anfühlen -_ wir müssen der Relaykeys-Hardware mitteilen, mit welchem Gerät sie sich verbinden soll.

1. Schließen Sie das Gerät an und folgen Sie den Anweisungen [wie oben] (wireless-mode.md#plug-in-your-relaykeys-stick-and-pair-with-a-computer-wired-mode)
2. Koppeln Sie das AAC/Host-Hauptgerät mit ihm. Koppeln Sie also den Computer, an den Sie es angeschlossen haben, mit der RelayKeys-Hardware. Dies kann sich etwas seltsam anfühlen - Sie verbinden die Hardware mit demselben Computer, auf dem Sie sich befinden. Siehe [hier](wireless-mode.md#undefined-1), wie man das Gerät in den Pairing-Modus bringt.
3. Trennen Sie die Relaykeys-Hardware. In den Bluetooth-Einstellungen müssen Sie auf das Element klicken und "Gerät entfernen" wählen. (NB: Wenn Sie dies nicht tun können, kann es daran liegen, dass Sie ein Administrator sein müssen. Öffnen Sie dazu die Systemsteuerung -> Geräte & Drucker -> Relaykeys -> Rechtsklick, Entfernen und Sie werden nach einem Admin-Passwort gefragt)
4. Schließen Sie die RelayKeys an eine Stromquelle an - nicht an den Computer. Ihre RelayKeys sind möglicherweise mit einer Batterie ausgestattet oder Sie müssen sie an eine USB-Stromquelle anschließen.
5. Drücken Sie zweimal auf den User-Schalter. Er sollte jetzt in einem schönen <mark="color:blue;">blau</mark> leuchten!
6. Starte RelayKeysd mit `--ble_mode` Siehe [hier](../../developers/relaykeys-daemon.md) für weitere Details