# ⌨️ Welcome to the RelayKeys Docs!

> These Docs will help get you up-and-running quickly, guide you through advanced features, and explain the concepts that make RelayKeys so unique.

## What is RelayKeys?

**RelayKeys is an open-source suite of software & hardware for communicating with computers,tablets,phones over a bluetooth connection.** It has been designed to work with AAC (Alternative & Augmenative Communication) devices first and foremost but the technology behind this is useful to many people who need to input text/mouse commands on one computer to access another bluetooth-enabled device. 


### Why? 
Solutions exist to do the same thing - either over a network connection (which can be laggy, slow and hard to configure reliably), or over wired serial connections but these are not easy to implement. Some commercial solutions exist but these are not easy to access for all software. 

## Core Principles

* **No-Software/Hardware on Client** — Because so many people have restrictions in the workplace or education settings we have designed this solution to not use any additional software or hardware for the client device. This means as long as your client device _supports Bluetooth LE_ then RelayKeys will work. 
* **Agnostic** — RelayKeys is not specific to certain devices or software solutions. It is not designed for anyone piece of software or hardware. We aim to make a solution that is broad in scope and allows a developer to use this how they wish. 
* **Open** — RelayKeys is not a closed, obfuscated, or black-boxed system. Alternative systems have existed for AAC but when technology becomes dropped by manufacturers engineers and clients alike struggle to keep their equipment working. By keeping the technology open we hope that others can fix and develop the solution.  Equally, the technology used in this is not just useful to people with disabilities but the general population. We aim to share our progress and hope others build on it. By working together we aim to reduce the steps and overheads to get this feature in all AAC software and other technology solutions; commercial or open-source alike. 


## The RelayKeys Ecosystem

There are several components of the RelayKeys ecosystem, below is a brief overview.

### RelayKeys-Service

This is a [RPC](https://en.wikipedia.org/wiki/Remote_procedure_call) service that listens for incoming connections and parses the commands. These commands are then converted to AT-Commands that are HID Keyboard/Mouse commands. These AT Commands are then sent over a serial connection to a piece of hardware that talks in Bluetooth to a secondary computer. On Windows we have built an installer that runs this continually. 

### RelayKeys-QT

This is a windowed application that captures keypress' (and one day mouse input) and sends this data to the RelayKeys Service

### RelayKeys-CLI

This is a 'command line interface' which allows programs that do not support native RPC calls to talk to the Service. It allows us to abstract certain features away from the service - and do more complex things like capturing the pasteboard of the computer. 