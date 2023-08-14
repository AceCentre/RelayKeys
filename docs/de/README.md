---
description: Overview of the project and its components
cover: .gitbook/assets/jessimage.jpeg
coverY: 0
---

# 😎 Einleitung

Willkommen bei der RelayKeys-Dokumentation! Dieser umfassende Leitfaden hilft dir, schnell loszulegen, fortgeschrittene Funktionen zu entdecken und die einzigartigen Konzepte von RelayKeys kennenzulernen.

### Einführung in RelayKeys

RelayKeys ist eine Open-Source-Software und -Hardware, die eine nahtlose Kommunikation zwischen Computern, Tablets und Telefonen über Bluetooth-Verbindungen ermöglicht. Die vielseitige Technologie wurde ursprünglich für Geräte der Unterstützten Kommunikation (AAC) entwickelt, eignet sich aber auch für andere Nutzer/innen, die Texteingaben oder Mausbefehle für den Zugriff auf Bluetooth-fähige Geräte benötigen.

#### Zweck und Vorteile

RelayKeys dient verschiedenen Zwecken:

* **Kosteneffiziente Lösung**: Für manche ist es eine kostengünstige Alternative oder ein Ersatz für teure oder veraltete Hardware.
* **Zugänglichkeit für Menschen mit Behinderungen**: Unser Hauptaugenmerk liegt darauf, Menschen mit Behinderungen zu unterstützen. RelayKeys ermöglicht es Nutzern, die auf spezielle Systeme der Unterstützten Kommunikation wie Eyegaze angewiesen sind, auf andere Geräte zuzugreifen, die für Arbeit oder Freizeit wichtig sind. Im Gegensatz zu begrenzten kommerziellen Lösungen funktioniert RelayKeys geräteübergreifend und benötigt kein gemeinsames Netzwerk. Es verhält sich genau wie eine Bluetooth-Tastatur und -Maus - es gibt also nur eine minimale Verzögerung.
* **Benutzerdefinierte Steuerung**: Mit RelayKeys können Nutzer/innen ihre Tablets oder Telefone steuern. Das ist besonders nützlich für Aufgaben wie Musikbearbeitung oder Fotobearbeitung, die in der Regel eine bildschirmfüllende Steuerung erfordern. Jedes Gerät, das auf eine Bluetooth-Tastatur oder -Maus reagiert, funktioniert - z. B. Smart-TVs.
* **Offenes System**: Die offene Architektur von RelayKeys sorgt für Langlebigkeit und fördert die Zusammenarbeit bei Systemverbesserungen, die sowohl Menschen mit Behinderungen als auch der allgemeinen Bevölkerung zugute kommen.

{% embed url=["https://www.youtube.com/watch?v=2wrZMGWgvcE"](https://www.youtube.com/watch?v=2wrZMGWgvcE)%}

### Warum RelayKeys wählen?

Es gibt zwar auch andere kommerzielle Lösungen, aber RelayKeys bietet eine Reihe von einzigartigen Vorteilen:

* **Nutzerzentrierter Ansatz**: Wir ermutigen kommerzielle Entwickler, die Bedürfnisse der Nutzer zu berücksichtigen und offene Lösungen zu erforschen. Wenn unser Ansatz nicht mit deinen Vorstellungen übereinstimmt, kannst du in Erwägung ziehen, unseren Befehlssatz für Kompatibilität und Verbesserungen zu übernehmen.
* **Ergänzend zur Software**: RelayKeys kann auf verschiedene Weise mit deiner eigenen Software zusammenarbeiten. Wir haben Beispiele dafür, wie es mit Software für Unterstützte Kommunikation und einer in Python geschriebenen eigenständigen Anwendung funktioniert. Wir können sogar Beispiele dafür zeigen, wie es verwendet werden kann, um Text auf einem [separaten zweiten Bildschirm](https://github.com/AceCentre/open-ble-screen) anzuzeigen.
* **Standardisierung für Kompatibilität**: Ein offenes System gewährleistet Kompatibilität und vereinfacht die Entwicklung. So können Entwickler/innen leichter eigene Lösungen entwickeln, die mit unserer Befehlsstruktur übereinstimmen.

### Kernprinzipien

RelayKeys basiert auf einer Reihe von Grundprinzipien, die sein Wesen ausmachen:

* **Keine Client-Software/Hardware**: RelayKeys wurde für den Einsatz am Arbeitsplatz und in der Ausbildung entwickelt und funktioniert ohne zusätzliche Software oder Hardware auf dem Client-Gerät. Solange Bluetooth LE Unterstützung vorhanden ist, funktioniert RelayKeys.
* **Geräteunabhängig**: RelayKeys ist nicht an bestimmte Geräte oder Softwarelösungen gebunden. Seine Vielseitigkeit ermöglicht es Entwicklern, es auf verschiedene Weise zu nutzen und so Innovationen zu fördern.
* **Offene Architektur**: RelayKeys ist ein offenes und transparentes System, das sich von geschlossenen, proprietären Alternativen unterscheidet. Diese Offenheit fördert die Zusammenarbeit und stellt sicher, dass die Technologie lebensfähig bleibt, auch wenn die Hersteller ihren Schwerpunkt verlagern.

### Das RelayKeys-Ökosystem

Das RelayKeys-Ökosystem besteht aus mehreren Schlüsselkomponenten, die jeweils eine bestimmte Aufgabe erfüllen:

#### RelayKeys-Serial API (RK-Serial)

Unsere standardisierte API ermöglicht die nahtlose Kommunikation mit RelayKeys-kompatiblen Hardware-Geräten über serielle Verbindungen, z. B. USB-Busse oder serielle Bluetooth-Verbindungen. Weitere Informationen findest du unter folgendem [Link](https://relaykeys.example.com/rk-serial).

#### RelayKeys-Service (RK-Service / Daemon)

Der RK-Service funktioniert wie ein RPC-Dienst, der eingehende Verbindungen empfängt und Befehle verarbeitet. Diese Befehle werden in AT-Befehle übersetzt, die HID-Tastatur/Maus-Aktionen simulieren. Die AT-Befehle werden dann über eine serielle Verbindung an Bluetooth-fähige Zweitgeräte übertragen. Für den Dauerbetrieb unter Windows ist ein Installationsprogramm verfügbar.

#### RelayKeys-QT (RK-Desktop)

RK-Desktop ist eine Fensteranwendung, die für die Erfassung von Tastatureingaben und zukünftigen Mauseingaben zuständig ist. Sie leitet diese Daten zur Verarbeitung an den RelayKeys-Dienst weiter.

#### RelayKeys-CLI (RK-CLI)

Die RK-CLI bietet eine Befehlszeilenschnittstelle für die Interaktion mit RelayKeys und ist eine vielseitige und effiziente Methode für Benutzer, die mit terminalbasierten Interaktionen vertraut sind.

Diese Dokumentation soll dir das Wissen vermitteln, das du brauchst, um die Möglichkeiten von RelayKeys voll auszuschöpfen. Egal, ob du als unterstützt kommunizierender Nutzer einen erweiterten Zugang suchst oder als Entwickler an bahnbrechenden Lösungen arbeitest, RelayKeys bietet eine Plattform, die Barrierefreiheit und Innovation fördert.
