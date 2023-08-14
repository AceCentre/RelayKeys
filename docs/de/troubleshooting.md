# ❓ Fehlersuche

> Im Folgenden findest du Lösungen für einige häufige Probleme, die bei der Arbeit mit RelayKeys auftreten können.

{% hint style="info" %}AceCentre**ist eine Wohltätigkeitsorganisation und wir stellen dieses Angebot so zur Verfügung, wie es ist. Wenn du etwas dringend brauchst und bezahlen kannst, bitten wir dich, uns zu spenden - oder einen anderen Entwickler, der dir bei der Lösung deines Problems hilft{%** endhint %}

## Probleme bei der Installation

### Ich kann es installieren - aber wenn ich Tastenanschläge sende, erscheint nichts auf dem zweiten Gerät?

Versuche es und führe diese Schritte durch:

1. **Ist dein RelayKeys-Stick richtig angebracht?** Vergewissere dich, dass das blaue Licht leuchtet. Wenn nicht, kann es sein, dass du irgendwo einen Wackelkontakt hast.
2. **Ist er gepaart und verbunden?** - Das erkennst du daran, dass das blaue Licht auf dem Relaykeys-Stick konstant leuchtet_(nicht_ blinkt).
3. Überprüfe**deinen COM-Port**. Es kann auch sein, dass die Software den RelayKeys-Stick nicht in ihrer Liste der COM-Ports findet. [Lies diese Anleitung](developers/relaykeys-cfg.md#dev-defining-your-port-of-the-relaykeys-hardware), um deinen COM-Port manuell zu konfigurieren und zu reparieren.
4. Überprüfe**dein Gehäuse und die Abstände**. Wenn du die Kommandozeilenanwendungen verwendest, sei vorsichtig - die Anwendung unterscheidet zwischen Groß- und Kleinschreibung. Es sollte z. B. _type:_ und nicht _Type:_ lauten

### Es hat alles gut funktioniert, aber jetzt nicht mehr!

Ist der Stick gekoppelt und wird er als mit dem empfangenden Gerät verbunden angezeigt? Wenn ja - und er immer noch keinen Text sendet, musst du das Bluetooth AceRK-Gerät entfernen und das AceRK erneut koppeln. Öffne dazu die App RelayKeys-QT auf dem sendenden Gerät, klicke auf "Gerät hinzufügen" und kopple es dann mit dem empfangenden Gerät.

### Ich sende also LSHIFT,2 und habe " erwartet, aber ich bekomme ein @ - Was ist los?

Wirf einen Blick auf die [Tastaturbelegung.](https://docs.acecentre.org.uk/products/v/relaykeys/developers/reference-2#defining-a-keymap-c) Du musst eine Tastaturbelegung für die Tastatur, die du erwartest, definieren/bearbeiten.
