# ⚙️ Installation



> Der einfachste Weg, die Software in Betrieb zu nehmen, ist der [Windows Installer] (https://github.com/AceCentre/RelayKeys/releases/latest), der die RelayKeys-CLI und die RelayKeys-Desktop-Software enthält. Lesen Sie weiter, um zu sehen, wie Sie installieren und einrichten.

## Eine kurze Erinnerung an die Funktionsweise

RelayKeys besteht also aus einer Hardwarelösung, die Bluetooth HID mit sekundären Geräten kommuniziert - alles, was sich mit Bluetooth koppeln kann und eine Tastatur versteht, funktioniert, und einer Software auf dem "Server"-Gerät, also dem Gerät, das die Tasten-/Mausbewegungen sendet. Für unsere Installation konzentrieren wir uns also auf den "Server", da das empfangende Gerät keine zusätzliche Hardware oder Software benötigt.

![RelayKeys Übersicht](../img/overview.png)

## Anforderungen

RelayKeys wurde für die Betriebssysteme Windows, Linux und Mac entwickelt. Wir haben ein Windows-Installationsprogramm entwickelt, das den Prozess auf dieser Plattform vereinfacht. Für Mac und Linux müssen Sie die Anwendung aus dem Quellcode erstellen.

* **Windows 7-10**
**Einen USB-Anschluss**
* Die Möglichkeit, die Software als Administrator zu installieren**
* **Ein zweites Gerät zum Verbinden** Kann ein Windows-Computer, ein Mac, ein iPad usw. sein


und das Wichtigste:

**Ein unterstütztes Stück RelayKeys-ready Hardware**
  * Im Moment ist dies so konzipiert, dass es mit dem [Adafruit nrf52840 express](https://www.adafruit.com/product/4062), [Adafruit nrf52840 Itsybitsy](https://www.adafruit.com/product/4481) oder [Raytac nrf52840 dongle](https://www.adafruit.com/product/5199) funktioniert. Andere werden der Liste hinzugefügt, während dies entwickelt wird.
  **Hinweis**: Wenn Sie einen Dongle zum Empfangen verwenden möchten - anstatt sich auf das interne Bluetooth eines Geräts und die Kopplung usw. zu verlassen - benötigen Sie eine zweite Platine.
