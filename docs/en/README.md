---
description: Overview of the project and its components
cover: .gitbook/assets/jessimage (1).jpeg
coverY: 0
---

# 😎 Introduction

Welcome to the RelayKeys Documentation! This comprehensive guide will help you swiftly get started, explore advanced features, and delve into the unique concepts that define RelayKeys.

### Introduction to RelayKeys

RelayKeys is an open-source software and hardware suite designed to facilitate seamless communication between computers, tablets, and phones via Bluetooth connections. Initially tailored for *AAC*[^1], its versatile technology extends its utility to a broader range of users who require text input or mouse commands to access Bluetooth-enabled devices.

#### Purpose and Benefits

RelayKeys serves various purposes:

* **Cost-Effective Solution**: For some, it offers a cost-effective alternative or replacement for pricey or obsolete hardware.
* **Accessibility for Disabilities**: Our primary focus is on empowering individuals with disabilities. RelayKeys enables users who rely on dedicated AAC systems, such as *Eyegaze*[^2], to access other devices essential for work or leisure. Unlike some commercial solutions, RelayKeys functions across devices without needing a shared network. It acts just like a Bluetooth keyboard and mouse, ensuring minimal lag.
* **Custom Control**: Users can utilize RelayKeys to control their tablets or phones, especially beneficial for tasks like music editing or photo manipulation, which typically require full-screen control. Any device responsive to a Bluetooth keyboard or mouse will work, e.g., smart TVs.
* **Open System**: RelayKeys' open architecture ensures longevity and promotes collaboration for system improvements, benefiting both individuals with disabilities and the general population.

{% embed url="https://www.youtube.com/watch?v=2wrZMGWgvcE" %}

### Why Choose RelayKeys?

While other commercial solutions exist, RelayKeys offers unique advantages:

* **User-Centric Approach**: We urge commercial developers to prioritize user needs and explore open solutions. If our method doesn't resonate with your vision, consider adopting our command set for compatibility and enhancement.
* **Complementary to Software**: RelayKeys has several ways to integrate with your software. We provide examples of its compatibility with AAC Software and a standalone app example written in Python. We also demonstrate how it can be utilized to display text on [a separate second screen](https://github.com/AceCentre/open-ble-screen).
* **Standardization for Compatibility**: An open system ensures compatibility and streamlines development, facilitating developers to craft solutions that resonate with our command structure.

### Core Principles

RelayKeys adheres to core principles that underpin its philosophy:

* **No Client Software/Hardware**: Catering to workplace and educational environments, RelayKeys functions without necessitating extra software or hardware on the client device. Provided *Bluetooth LE*[^3] support is available, RelayKeys operates seamlessly.
* **Device Agnostic**: RelayKeys isn't restricted to specific devices or software solutions. Its adaptability allows developers to apply it diversely, promoting innovation.
* **Open Architecture**: RelayKeys is a transparent and open system, standing apart from closed, proprietary counterparts. This transparency fosters collaboration and ensures technology remains relevant despite shifting manufacturer priorities.

### The RelayKeys Ecosystem

The RelayKeys ecosystem includes key components, each fulfilling a particular function:

#### RelayKeys-Serial API (RK-Serial)

Our standardized API ensures smooth communication with RelayKeys-compatible hardware devices over serial connections, encompassing USB buses and Bluetooth serial connections. More details are available at this [link](https://relaykeys.example.com/rk-serial).

#### RelayKeys-Service (RK-Service / *Daemon*)[^4]

The RK-Service acts as an *RPC*[^5] service, accepting incoming connections and interpreting commands. These commands are converted into *AT Commands*[^6], mimicking *HID*[^7] keyboard/mouse actions. The AT Commands are subsequently relayed through a serial connection to Bluetooth-integrated secondary devices. A Windows installer facilitates continuous operation.

#### RelayKeys-QT (RK-Desktop)

RK-Desktop is a windowed application tasked with capturing keystrokes and future mouse actions. This data is then relayed to the RelayKeys Service for translation.

#### RelayKeys-CLI (RK-CLI)

The RK-CLI offers a command-line interface for RelayKeys interaction, serving as an adaptable and efficient tool for those familiar with terminal operations.

Harness the full potential of RelayKeys with this documentation. Whether you're an AAC user aspiring for extensive accessibility or a developer pioneering innovative solutions, RelayKeys presents a platform championing accessibility and creativity.

[^1]: **AAC (Alternative and Augmentative Communication)**: Methods of communication that supplement or replace speech or writing for those with impairments in the production or comprehension of spoken or written language.
[^2]: **Eyegaze**: A technology that tracks where a user is looking on a screen, typically used as an input method for those with limited physical mobility.
[^3]: **Bluetooth LE (Low Energy)**: A power-conserving variant of the classic Bluetooth wireless communication standard.
[^4]: **Daemon**: A background process that runs on a computer system, often providing or facilitating services.
[^5]: **RPC (Remote Procedure Call)**: A protocol that allows programs to cause a procedure (subroutine) to execute in another address space (commonly on another computer on a shared network).
[^6]: **AT Commands**: A set of commands originally developed for controlling modems. The "AT" stands for "Attention." These commands have since been repurposed and expanded for a variety of other applications, including Bluetooth LE (BLE) devices.
[^7]: **HID (Human Interface Device)**: A type of computer device that interacts directly with, and most often takes input from, humans.
