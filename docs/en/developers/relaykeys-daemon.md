# Server (Daemon) reference

The _daemon_ (`relaykeys-daemon`) is the background service that manages the serial connection to the nRF52840 dongle and exposes a JSON-RPC server (port 5383) and a web UI for control and testing.

When installed via the NSIS installer, it runs as a Windows service. You can also run it directly:

```bash
relaykeys-daemon.exe --debug
```

## Command-line flags

### --config=path

Path to the configuration file. See [relaykeys-cfg.md](relaykeys-cfg.md) for config file details.

Search order when not specified: `~/.relaykeys.cfg` → `<exe_dir>/relaykeys.cfg` → `./relaykeys.cfg` → `%APPDATA%\RelayKeys\relaykeys.cfg`

### --dev=port

Force a specific serial port instead of auto-detecting.

```bash
relaykeys-daemon.exe --dev=COM5
```

### --baud=rate

Set the serial baud rate. Default: 115200.

### --noserial

Run without connecting to serial hardware. Useful for development or testing the web UI without a dongle.

### --debug

Enable verbose debug logging to the console.

### --list-ports

List all detected serial ports and exit. Useful for debugging which COM port the dongle is on.

### --version

Print the version and exit.

### --service=action

Manage the Windows service:

```bash
relaykeys-daemon.exe --service install
relaykeys-daemon.exe --service start
relaykeys-daemon.exe --service stop
relaykeys-daemon.exe --service uninstall
```

## Architecture

The daemon starts its HTTP server immediately and attempts serial connection in a background goroutine. If the dongle is not connected, the daemon keeps retrying every 3 seconds. The RPC server and web UI are available even without hardware.

Key components:

- **Serial auto-detect**: Scans for Adafruit nRF52840 boards (VID `239A`, PIDs `8029`, `810B`, `8051`)
- **JSON-RPC server**: Port 5383, used by the CLI and AAC software
- **Web UI**: Embedded HTML/JS/CSS served at `http://127.0.0.1:5383/ui/`
- **WebSocket hub**: Real-time status updates to the web UI

## Related

- [Config file reference](relaykeys-cfg.md)
- [Architecture overview](architecture.md)
- [Developing without a board](developing-without-a-board.md)
