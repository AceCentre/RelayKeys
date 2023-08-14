# Entwickeln ohne Board

Wenn Sie die „Server“-Seite entwickeln und den Code ausprobieren möchten, können Sie ihn ohne Hardware ausführen, indem Sie über ein Null-Seriell-Terminal verfügen. Führen Sie dazu in einem Terminal Folgendes aus:

```
python resources/demoSerial.py
```

dann in einem anderen Terminal ausführen

```
python relayekeysd.py --noserial
```

Hinweis: Nur unter MacOS getestet, sollte aber auf jedem Posix-System funktionieren. Geben Sie für Windows einfach einen COM-Port an, der nicht existiert.
