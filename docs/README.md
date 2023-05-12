---
cover: .gitbook/assets/jessimage.jpeg
coverY: 0
---

# Welcome to the RelayKeys Docs!

> These Docs will help get you up-and-running quickly, guide you through advanced features, and explain the concepts that make RelayKeys so unique.

## What is RelayKeys?

**RelayKeys is an open-source suite of software & hardware for communicating with computers, tablets, phones over a bluetooth connection.** It has been designed to work with AAC (Alternative & Augmentative Communication) devices first and foremost but the technology behind this is useful to many people who need to input text/mouse commands on one computer to access another bluetooth-enabled device.

### Why?

Well a range of purposes. For some - its just a convenient way of saving some money on a [KVM switch](https://en.wikipedia.org/wiki/KVM\_switch) - or replacing now hard to find [commercial solutions](https://docs.acecentre.org.uk/products/v/relaykeys/developers/other-projects).

For the [AceCentre](http://acecentre.org.uk/) we want people with disabilities who are forced to use one system (e.g. a dedicated Eyegaze system) to be able to access other computers and systems they may need to use for work or leisure. This has only been available on a couple of commercial AAC systems - and often need to be on the same network which is sadly often impossible in schools or government workplaces - Or they do work over bluetooth but for only one system in the field exists like this (see [here for more details on these](https://docs.acecentre.org.uk/products/v/relaykeys/developers/other-projects#aac-projects)). Some people may also want to just control their tablet or phone using this technique rather than rely on computer control functions - for example to control music software or photo editing software which usually demands the full screen. Or others want to make custom full screen custom keyboards using their specialist software.

**Why not just rely on other solutions?** Some commercial solutions are great. We advocate using them over our solution when you can. When you can't (e.g. no alternative or restrictions to what devices you can control) then this may be a solution.

**We are a commercial developer.. I like it but I think I could do it differently**. Thats great! But please consider the end user. If you as a commercial supplier dont want to continue making this hardware/software solution in the future consider a route to how a user could use a open solution. Please consider either replicating our command set at a serial or CLI level. Are we missing something that your solution provides? Please let us know so we can improve it.

**Why not just do this in software alone?** Sure. If you can. On windows - its not possible.. Yet. Maybe in Windows 11. In MacOS it _should_ be - and iOS & Android its definitely possible. But our solution kind of offloads the problem. If you work in one of the mobile environments and want to replicate the functionality go for it - just please consider following some similarity in command structure (take a look at the macros for example)

**By creating an open system we aim for longevity; even if a developer wants to create their own system we ask to make it compatible by using the same standard way of calling devices.**

{% embed url="https://www.youtube.com/watch?v=2wrZMGWgvcE" %}
**Short demonstration of the main aspects of RelayKeys**
{% endembed %}

## Core Principles

* **No-Software/Hardware on Client** — Because so many people have restrictions in the workplace or education settings we have designed this solution to not use any additional software or hardware for the client device. This means as long as your client device _supports Bluetooth LE_ then RelayKeys will work.
* **Agnostic** — RelayKeys is not specific to certain devices or software solutions. It is not designed for anyone piece of software or hardware. We aim to make a solution that is broad in scope and allows a developer to use this how they wish.
* **Open** — RelayKeys is not a closed, obfuscated, or black-boxed system. Alternative systems have existed for AAC but when technology becomes dropped by manufacturers engineers and clients alike struggle to keep their equipment working. By keeping the technology open we hope that others can fix and develop the solution. Equally, the technology used in this is not just useful to people with disabilities but the general population. We aim to share our progress and hope others build on it. By working together we aim to reduce the steps and overheads to get this feature in all AAC software and other technology solutions; commercial or open-source alike.

## The RelayKeys Ecosystem

There are several components of the RelayKeys ecosystem, below is a brief overview. Remember that the software below works on one computer (a _**server computer**_ - often the AAC device) and the computers/tablets/mobile phones it connects to are _**receiving devices**_.

### RelayKeys-Serial API (_aka_ _RK-Serial_)

We have defined a standard for calling a RelayKeys (or RelayKeys compatible) hardware device when available over serial. RelayKeys can be used over a USB bus or Bluetooth serial connection. See [here](developers/relaykeys-serial.md) for more information.

### RelayKeys-Service (_aka_ _RK-Service_ / _Daemon_)

This is a [RPC](https://en.wikipedia.org/wiki/Remote\_procedure\_call) service that listens for incoming connections and parses the commands. These commands are then converted to AT-Commands that are HID Keyboard/Mouse commands. These AT Commands are then sent over a serial connection to a piece of hardware that talks in Bluetooth to a secondary computer. On Windows we have built an installer that runs this continually.

### RelayKeys-QT (_aka_ _RK-Desktop_)

This is a windowed application that captures keypress' (and one day mouse input) and sends this data to the RelayKeys Service

### RelayKeys-CLI (_aka_ _RK-CLI_)

This is a '_command line interface_' which allows programs that do not support native RPC calls to talk to the Service. It allows us to abstract certain features away from the service - and do more complex things like capturing the pasteboard of the computer.
