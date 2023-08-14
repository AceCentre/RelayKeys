# 👩‍💻 Mitwirken

> Unser kleines Team schätzt wirklich jeden Beitrag unserer Community: User Stories, Feature Requests, Bug Reports und insbesondere Pull Requests! Wenn Sie haben_beliebig_ Bei Fragen wenden Sie sich bitte an unser Kernteam unter[AceCentre](https://acecentre.org.uk) .

## Benutzergeschichten

Sie verwenden also RelayKeys? Gefällt Ihnen, was wir tun? Sie haben ein echtes Problem, das behoben werden muss, aber Sie verstehen diesen ganzen Code nicht? Bitte[in Kontakt kommen](https://acecentre.org.uk/contact/) . Wir werden versuchen zu helfen – aber bitte beachten Sie;**Hierbei handelt es sich weitgehend um ein Open-Source- und finanziertes Projekt** . Wenn Sie können, denken Sie bitte darüber nach, das Projekt zu spenden

## RelayKeys-Repository

### [acecentre/relaykeys](https://github.com/acecentre/relaykeys)

Dies ist die Heimat des Projekts. Bitte forken Sie und nehmen Sie in Zukunft Änderungen an diesem Projekt vor. Ein kurzer Überblick über die Inhalte:

* **Arduino/**enthält Skizzen, damit das Board funktioniert. Ein großes Dankeschön an Adafruit, da es sich um nrf52840 handelt_ihre_ Brett mit_ihre_ Firmware und dieser Code ist groß_ihre_ Beispielcode. Wir haben die Mausfunktionalität hinzugefügt
* **Dokumente/**Der Ordner, der die Dokumente enthält (diese Dokumente, die Sie gerade lesen!). Es ist alles mit Gitbook erstellt
* **Ressourcen/**eine Mülldeponie für Ressourcen/Werkzeuge, die für die Entwicklung nützlich sein können. Bemerkenswert ist[demoSerial.py](../../resources/demoSerial.py) - eine Möglichkeit, dies zu programmieren, ohne dass das Board unter Linux/Mac zur Hand ist. Siehe auch[viewComPorts.py](../../resources/viewComPorts.py) um Ihre COM-Ports zu debuggen
* blehid.py – das ist das Modul, das in Relaykeysclient und Relaykeysd verwendet wird. Wenn Sie sich Dinge wie die Konvertierung von Schlüsselcodes und Ähnliches ansehen möchten, klicken Sie hier.
* buildinstaller.py – das ist ein Skript, das die Pyinstaller-Binärdateien „erstellt“ – und die NSIS-Setup.exe.
* Relaykeys-cli.py – das CLI-Programm
* Relaykeys.py – der Originalcode, den wir zum Testen verwendet haben. Im Moment weitgehend überflüssig – aber wenn Sie sich einen Überblick darüber verschaffen möchten, wie das alles funktioniert, schauen Sie zuerst hier nach

## Einfache Pull-Anfragen

Bevor wir uns mit der vollständigen „richtigen“ Methode zum Ausführen einer Pull-Anfrage befassen, wollen wir uns kurz mit einer einfacheren Methode befassen, die Sie verwenden können_klein_ behebt. Diese Methode ist besonders nützlich, um schnelle Tippfehler in den Dokumenten zu beheben, ist jedoch bei Codeänderungen nicht so sicher, da Validierung und Linting umgangen werden.

1. Melden Sie sich bei GitHub an
2. Gehen Sie zu der Datei, die Sie bearbeiten möchten (z. B.:[this page](https://github.com/acecentre/relaykeys/docs/blob/master/feature-requests.md) )
3. Klicken Sie auf das Stiftsymbol, um „Diese Datei bearbeiten“ auszuwählen.
4. Nehmen Sie etwaige Änderungen vor
5. Beschreiben und übermitteln Sie Ihre Änderungen unter „Dateiänderung vorschlagen“.

Das ist es! GitHub erstellt für Sie einen Fork des Projekts und übermittelt die Änderung an einen neuen Branch in diesem Fork. Denken Sie daran, beim Lösen verschiedener Probleme separate Pull-Anfragen einzureichen.

## Richtige Pull-Anfragen

_Lose basierend auf_ [_dieser großartige Kern_](https://gist.github.com/Chaser324/ce0505fbed06b947d962) _von_ [_Chaser324_](https://gist.github.com/Chaser324)

Wir möchten bei der Arbeit mit GitHub einen engen Ablauf einhalten, um sicherzustellen, dass wir einen klaren Verlauf und eine klare Verantwortlichkeit darüber haben, welche Änderungen wann vorgenommen wurden. Die Arbeit mit Git und insbesondere den GitHub-spezifischen Funktionen wie Forken und Erstellen von Pull-Requests kann für neue Benutzer ziemlich entmutigend sein.

Um Sie bei Ihren Git(Hub)-Abenteuern zu unterstützen, haben wir den (ziemlich standardmäßigen) Ablauf für die Mitarbeit an einem Open-Source-Repo zusammengestellt.

### Das Repo forken

Unabhängig davon, ob Sie an der API oder der App arbeiten, benötigen Sie eine eigene Kopie der Codebasis, an der Sie arbeiten können. Gehen Sie zum Repo des Projekts, bei dem Sie helfen möchten, und klicken Sie auf die Schaltfläche „Fork“. Dadurch wird eine vollständige Kopie des gesamten Projekts für Sie auf Ihrem eigenen Konto erstellt.

Um an dieser Kopie zu arbeiten, können Sie das Projekt gemäß der normalen Installationsanleitung lokal installieren und dabei den Namen ersetzen `acecentre` mit dem Namen Ihres Github-Kontos.

### Halten Sie Ihren Fork auf dem neuesten Stand

Wenn Sie mehr Arbeit als nur eine kleine Korrektur durchführen, ist es eine gute Idee, Ihren Fork mit dem „Live“ oder auf dem neuesten Stand zu halten_stromaufwärts_ Repo. Dies ist das Haupt-Acecentre-Repo, das den neuesten Code enthält. Wenn Sie Ihren Fork nicht mit dem Upstream-Fork auf dem neuesten Stand halten, kommt es ziemlich schnell zu Konflikten. Diese Konflikte entstehen, wenn Sie eine Änderung an einer Datei vorgenommen haben, die sich in der Zwischenzeit im Upstream-Repository geändert hat.

#### Auf Git-Fernbedienungen

Wenn Sie Git in der Befehlszeile verwenden, kommt es oft zu einem Pull-and-Push-Vorgang `origin`. Möglicherweise haben Sie diesen Begriff in bestimmten Befehlen gesehen, z

```bash
git push origin master
```

oder

```bash
git pull origin new-feature
```

In diesem Fall das Wort `origin` wird als a bezeichnet_Fernbedienung_. Es ist im Grunde nichts weiter als ein Name für die vollständige Git-URL, von der Sie das Projekt geklont haben:

```bash
git push origin master
```

ist gleich

```bash
git push git@github.com:username/repo.git master
```

Ein lokales Git-Repo kann mehrere Remotes haben. Obwohl es nicht sehr üblich ist, Ihren Code auf mehrere Repos zu übertragen, ist es sehr nützlich, wenn Sie an Open-Source-Projekten arbeiten. Sie können damit das Upstream-Repo als weiteres Remote-Repository hinzufügen und so die neuesten Änderungen direkt in Ihr lokales Projekt abrufen.

```bash
# Add 'upstream' to remotes
git remote add upstream git@github.com:acecentre/relaykeys.git
```

Wenn Sie Ihren Fork mit den neuesten Änderungen aus dem Upstream-Projekt aktualisieren möchten, müssen Sie zunächst alle (neuen) Branches und Commits durch Ausführen abrufen

```bash
git fetch upstream
```

Wenn alle Änderungen abgerufen wurden, können Sie den Zweig, den Sie aktualisieren möchten, auschecken und die Änderungen einbinden.

```
git checkout master
git rebase upstream/master
```

Wenn Sie für den Zweig, den Sie aktualisieren, keine Verpflichtungen eingegangen sind, aktualisiert Git Ihren Zweig ohne Beanstandungen. Wenn du_haben_ Wenn Sie in der Zwischenzeit Commits erstellt haben, wendet Git Schritt für Schritt alle Commits an_stromaufwärts_ und versuchen Sie, den Commit hinzuzufügen, den Sie in der Zwischenzeit vorgenommen haben. Es ist sehr plausibel, dass es in dieser Phase zu Konflikten kommt. Wenn Sie etwas geändert haben, das sich auch im Upstream geändert hat, verlangt Git, dass Sie den Konflikt selbst lösen, bevor Sie fortfahren können.

::: Gefahr Konflikte Sie sollten Änderungen im Upstream immer den Vorzug vor Ihren lokalen geben. :::

### Arbeiten

Wenn Sie mit der Arbeit an einem Bugfix oder einer neuen Funktion beginnen, stellen Sie sicher, dass Sie einen neuen Zweig erstellen. Dadurch wird sichergestellt, dass Ihre Änderungen organisiert und vom Master-Branch getrennt sind, sodass Sie Ihre Pull-Anfragen für separate Fixes/Features einfacher einreichen und verwalten können.

```bash
# Checkout the master branch - you want your new branch to come from master
git checkout master

# Create a new branch named newfeature (give your branch its own simple informative name)
git branch newfeature

# Switch to your new branch
git checkout newfeature
```

::: Warnung Aktualität Stellen Sie sicher, dass Sie Ihren Master-Zweig mit dem vom Upstream aktualisieren, damit Sie sicher sein können, dass Sie mit der neuesten Version des Projekts beginnen! :::

### Senden einer Pull-Anfrage

Bevor Sie Ihren Pull-Request öffnen, möchten Sie möglicherweise Ihren Branch ein letztes Mal aktualisieren, damit er sofort in den Master-Branch des Upstreams eingebunden werden kann.

```bash
# Fetch upstream master and merge with your repo's master branch
git fetch upstream
git checkout master
git merge upstream/master

# If there were any new commits, rebase your master branch
git checkout newfeature
git rebase master
```

::: Warnung Stellen Sie sicher, dass Sie überprüfen, ob Ihre Filiale auf dem neuesten Stand ist `master` Zweig von Upstream. Ein veralteter Zweig macht es für die Betreuer von acecentre nahezu unmöglich, die Pull-Anfrage zu überprüfen und zu überprüfen, und wird höchstwahrscheinlich zu einer verzögerten Zusammenführung führen.:::

Sobald Sie alle Änderungen an Ihrem Branch festgeschrieben und in Ihren Fork auf GitHub übertragen haben, gehen Sie zu GitHub, wählen Sie Ihren Branch aus und klicken Sie auf die Schaltfläche „Pull Request“.

Sie können weiterhin neue Commits an einen bereits geöffneten Pull-Request übertragen. Auf diese Weise können Sie bestimmte Kommentare korrigieren, die Rezensenten möglicherweise hinterlassen haben.

::: Tipp Bitte gestatten Sie den Betreuern des Upstreams, Commits an Ihren Fork zu pushen, indem Sie die Option „Änderungen durch Betreuer zulassen“ aktiviert lassen. Dadurch kann unser Kernteam Sie bei Ihrer PR unterstützen! :::

## Funktionsanfragen

### 80/20-Regel

Das Wichtigste, worauf Sie beim Einreichen einer neuen Acecenter-Feature-Anfrage achten sollten, ist unsere Regel zu Randfällen. Um die Kerncodebasis von acecentre so sauber und einfach wie möglich zu halten, werden wir nur das Hinzufügen von Funktionen in Betracht ziehen, die mindestens 80 % unserer Benutzerbasis nutzen werden. Wenn wir der Meinung sind, dass weniger als 80 % unserer Benutzer die Funktion wertvoll finden, werden wir sie nicht implementieren. Stattdessen sollten diese Edge-Case-Funktionen als Erweiterungen hinzugefügt werden.

### Vorhandene Anfragen durchsuchen

Bevor Sie eine neue Anfrage hinzufügen, sollten Sie dies auch zuerst tun[search](https://github.com/acecentre/relaykeys/issues?q=is%3Aissue+is%3Aopen+sort%3Areactions-%2B1-desc) um zu sehen, ob es bereits übermittelt wurde. Alle Funktionsanfragen sollten das enthalten `enhancement` Label, damit Sie danach filtern können. Und denken Sie daran, auch zu überprüfen_geschlossen_ Probleme, da Ihr Feature möglicherweise bereits in der Vergangenheit eingereicht wurde, und beides[rejected](contributing.md#Our-80/20-Rule) oder bereits umgesetzt.

Wenn Sie außerdem die am häufigsten nachgefragten Funktionen sehen möchten, können Sie diese nach sortieren `:+1:` (das Daumen-hoch-Emoji).

### Senden einer Anfrage

Wenn Ihre Idee den 80/20-Test besteht und noch nicht eingereicht wurde, würden wir uns freuen, davon zu hören! Reichen Sie ein neues Problem mit der Feature-Request-Vorlage ein und stellen Sie sicher, dass Sie Folgendes angeben `enhancement` Etikett. Es ist wichtig, die Vorlage vollständig mit möglichst vielen nützlichen Informationen auszufüllen, damit wir Ihre Anfrage ordnungsgemäß prüfen können. Wenn Sie Screenshots, Designs, Codebeispiele oder andere hilfreiche Assets haben, fügen Sie diese unbedingt auch bei!

### Abstimmung über Anfragen

Sie können auch über bestehende Funktionswünsche abstimmen. Wie oben erwähnt, die `:+1:` Und `:-1:` werden zum Sortieren verwendet. Das Hinzufügen einer dieser Reaktionen zum GitHub-Problem führt also zu einer Abstimmung, die uns hilft, die am meisten gewünschten (oder unerwünschten) Funktionen besser zu identifizieren. Und denken Sie daran, einen Kommentar hinzuzufügen, wenn Sie weitere Gedanken zur Klärung oder Verbesserung der Anfrage haben.

### Eine Anfrage erfüllen

Unser Kernteam arbeitet stets hart daran, die am häufigsten nachgefragten Community-Funktionen zu implementieren, aber wir sind ein kleines Team. Wenn Sie die Funktion schneller benötigen, als wir sie bereitstellen können, oder einfach zur Verbesserung der acecentre-Plattform beitragen möchten, würden wir uns über eine Pull-Anfrage von Ihnen freuen!
