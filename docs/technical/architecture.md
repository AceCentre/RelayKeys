Architecture of RelayKeys
===========================

RelayKeys consists of:
1. A hardware dongle that communicate in Bluetooth lE
2. A daemon (server) that talks directly to the hardware. Currently this over a serial connection. This could be a wired or wireless serial connection
3. A client that talks to the daemon. This could be either a GUI, a command line app or directly from a dedicated piece of software 

