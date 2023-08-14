---
description: Overview of the project and its components
cover: .gitbook/assets/jessimage (1).jpeg
coverY: 0
---

# 😎 Introduction

Welcome to the RelayKeys Documentation! This comprehensive guide will help you swiftly get started, explore advanced features, and delve into the unique concepts that define RelayKeys.

### Introduction to RelayKeys

RelayKeys is an open-source software and hardware suite designed to facilitate seamless communication between computers, tablets, and phones via Bluetooth connections. While initially tailored for Alternative and Augmentative Communication (AAC) devices, its versatile technology extends its utility to a broader range of users who require text input or mouse commands to access Bluetooth-enabled devices.

#### Purpose and Benefits

RelayKeys serves various purposes:

* **Cost-Effective Solution**: For some, it provides a cost-effective alternative or replacement for pricey or obsolete hardware.
* **Accessibility for Disabilities**: Our primary focus is on empowering individuals with disabilities. RelayKeys enables users who rely on dedicated AAC systems, such as Eyegaze, to access other devices crucial for work or leisure. Unlike limited commercial solutions, RelayKeys functions across devices and doesn't necessitate a shared network. It acts just like a Bluetooth keyboard and mouse - so there is minimal lag.&#x20;
* **Custom Control**: Users can use RelayKeys to control their tablets or phones, particularly useful for tasks like music editing or photo manipulation, which typically demand full-screen control. Any device which responds to a Bluetooth keyboard or mouse will work - e.g. smart TV's.
* **Open System**: RelayKeys' open architecture ensures longevity and fosters collaboration for system improvements, aiding both people with disabilities and the general population.

{% embed url="https://www.youtube.com/watch?v=2wrZMGWgvcE" %}

### Why Choose RelayKeys?

While other commercial solutions exist, RelayKeys offers a unique set of advantages:

* **User-Centric Approach**: We encourage commercial developers to consider user needs and explore open solutions. If our approach doesn't align with your vision, consider adopting our command set for compatibility and improvement.
* **Complementary to Software**: RelayKeys has a number of ways it can work with your own software. We have examples of how it can work with AAC Software and an example standalone app written in Python. We can even show examples of how it can be used to display text on [a separate second screen](https://github.com/AceCentre/open-ble-screen).&#x20;
* **Standardization for Compatibility**: An open system ensures compatibility and simplifies development, making it easier for developers to create their own solutions that align with our command structure.

### Core Principles

RelayKeys is built upon a set of core principles that define its essence:

* **No Client Software/Hardware**: Designed to accommodate workplace and education settings, RelayKeys operates without requiring additional software or hardware on the client device. As long as Bluetooth LE support is present, RelayKeys is functional.
* **Device Agnostic**: RelayKeys isn't tied to specific devices or software solutions. Its versatility empowers developers to leverage it in various ways, fostering innovation.
* **Open Architecture**: RelayKeys is an open and transparent system, distinct from closed, proprietary alternatives. This openness encourages collaboration and ensures that technology remains viable even as manufacturers shift focus.

### The RelayKeys Ecosystem

The RelayKeys ecosystem comprises several key components, each serving a specific role:

#### RelayKeys-Serial API (RK-Serial)

Our standardized API enables seamless communication with RelayKeys-compatible hardware devices over serial connections, including USB buses or Bluetooth serial connections. For more information, refer to the [link](https://relaykeys.example.com/rk-serial).

#### RelayKeys-Service (RK-Service / Daemon)

The RK-Service functions as an RPC service, receiving incoming connections and processing commands. These commands are translated into AT-Commands, simulating HID Keyboard/Mouse actions. The AT Commands are then transmitted via serial connection to Bluetooth-enabled secondary devices. An installer is available for continuous operation on Windows.

#### RelayKeys-QT (RK-Desktop)

RK-Desktop is a windowed application responsible for capturing keystrokes and future mouse inputs. It forwards this data to the RelayKeys Service for processing.

#### RelayKeys-CLI (RK-CLI)

The RK-CLI provides a command-line interface for interacting with RelayKeys, offering a versatile and efficient method for users comfortable with terminal-based interactions.

This documentation aims to empower you with the knowledge needed to harness RelayKeys' capabilities fully. Whether you're an AAC user seeking expanded access or a developer working on groundbreaking solutions, RelayKeys offers a platform that promotes accessibility and innovation.
