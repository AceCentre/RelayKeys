---
description: Overview of the project and its components
cover: .gitbook/assets/jessimage (1).jpeg
coverY: 0
---

# 😎 Introduction

Welcome to the RelayKeys Documentation! This  guide will help you swiftly get started, explore advanced features, and understand the concepts that define RelayKeys.

### Introduction to RelayKeys

RelayKeys is an open-source software and hardware suite designed to facilitate seamless communication between computers, tablets, and phones via Bluetooth connections. Initially tailored for _AAC_, its versatile technology extends its utility to a broader range of users who require text input or mouse commands to access Bluetooth-enabled devices.

### How do you get it?

You need a piece of hardware - a USB dongle that provides the bluetooth harware to allow your device to be a Bluetooth Keyboard/Mouse. You plug this into your AAC (Host) Windows based device. You can either use a receiving USB dongle on a second device to act as a Bluetooth receiver for devices that don't support bluetooth (and this is pre-paired) or connect directly to Bluetooth enabled devices (Phones, Computers). \
\
Once you have the hardware you need to [install our software](installation/download-and-setup-software.md) which is designed for Windows.&#x20;

#### Purpose and Benefits

RelayKeys serves various purposes:

* **Cost-Effective Solution**: For some, it offers a cost-effective alternative or replacement for pricey or obsolete hardware.
* **Accessibility for Disabilities**: Our primary focus is on empowering individuals with disabilities. RelayKeys enables users who rely on dedicated AAC systems, such as _Eyegaze_, to access other devices essential for work or leisure. Unlike some commercial solutions, RelayKeys functions across devices without needing a shared network. It acts just like a Bluetooth keyboard and mouse, ensuring minimal lag.
* **Custom Control**: Users can utilize RelayKeys to control their tablets or phones, especially beneficial for tasks like music editing or photo manipulation, which typically require full-screen control. Any device responsive to a Bluetooth keyboard or mouse will work, e.g., smart TVs.
* **Open System**: RelayKeys' open architecture ensures longevity and promotes collaboration for system improvements, benefiting both individuals with disabilities and the general population.

{% embed url="https://www.youtube.com/watch?v=2wrZMGWgvcE" %}
Quick overview of features between devices
{% endembed %}

{% embed url="https://youtu.be/nEMUdILvEuA" %}
Using the raytac dongles prepaired to control a LG Smart TV
{% endembed %}

### Why Choose RelayKeys?

While other commercial solutions exist, RelayKeys offers unique advantages:

* **User-Centric Approach**: We urge commercial developers to prioritize user needs and explore open solutions. If our method doesn't resonate with your vision, consider adopting our command set for compatibility and enhancement.
* **Complementary to Software**: RelayKeys has several ways to integrate with your software. We provide examples of its compatibility with AAC Software and a standalone app example written in Python. We also demonstrate how it can be utilized to display text on [a separate second screen](https://github.com/AceCentre/open-ble-screen).
* **Standardization for Compatibility**: An open system ensures compatibility and streamlines development, facilitating developers to craft solutions that resonate with our command structure.

### Core Principles

RelayKeys adheres to core principles that underpin its philosophy:

* **No Client Software/Hardware**: Catering to workplace and educational environments, RelayKeys functions without necessitating extra software or hardware on the client device. Provided _Bluetooth LE_ support is available, RelayKeys operates seamlessly.
* **Device Agnostic**: RelayKeys isn't restricted to specific devices or software solutions. Its adaptability allows developers to apply it diversely, promoting innovation.
* **Open Architecture**: RelayKeys is a transparent and open system, standing apart from closed, proprietary counterparts. This transparency fosters collaboration and ensures technology remains relevant despite shifting manufacturer priorities.

### The RelayKeys Ecosystem

The RelayKeys ecosystem includes key components, each fulfilling a particular function:

#### RelayKeys-Serial API (RK-Serial)

Our standardized API ensures smooth communication with RelayKeys-compatible hardware devices over serial connections, encompassing USB buses and Bluetooth serial connections. More details are available at this [link](https://relaykeys.example.com/rk-serial).

#### RelayKeys-Service (RK-Service / _Daemon_)

The RK-Service acts as an _RPC_ service, accepting incoming connections and interpreting commands. These commands are converted into _AT Commands_, mimicking _HID_ keyboard/mouse actions. The AT Commands are subsequently relayed through a serial connection to Bluetooth-integrated secondary devices. A Windows installer facilitates continuous operation.

#### RelayKeys-QT (RK-Desktop)

RK-Desktop is a windowed application tasked with capturing keystrokes and future mouse actions. This data is then relayed to the RelayKeys Service for translation.

#### RelayKeys-CLI (RK-CLI)

The RK-CLI offers a command-line interface for RelayKeys interaction, serving as an adaptable and efficient tool for those familiar with terminal operations.

Harness the full potential of RelayKeys with this documentation. Whether you're an AAC user aspiring for extensive accessibility or a developer pioneering innovative solutions, RelayKeys presents a platform championing accessibility and creativity.

1. **Eyegaze**: A technology that tracks where a user is looking on a screen, typically used as an input method for those with limited physical mobility.
2. **Daemon**: A background process that runs on a computer system, often providing or facilitating services.
