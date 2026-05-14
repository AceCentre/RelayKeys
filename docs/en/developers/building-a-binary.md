# Building a binary

RelayKeys is written in Go. Builds are tested on Windows and macOS.

## Prerequisites

- **Go 1.21+** — https://go.dev/dl/
- **NSIS 3.x** (Windows installer only) — https://nsis.sourceforge.io/
- **SimpleSC plugin** for NSIS — copy `SimpleSC.dll` into the NSIS `Plugins` directory

## Quick Build (Windows)

The PowerShell script builds everything and produces an installer:

```powershell
powershell -ExecutionPolicy Bypass -File build-go.ps1
```

This compiles the daemon, CLI, and tray app, runs tests, copies assets, and runs NSIS to produce `RelayKeys-VERSION-setup.exe`.

## Manual Build

```bash
# Build the daemon
go build -o relaykeys-daemon.exe ./cmd/relaykeys-daemon

# Build the CLI client
go build -o relaykeys-cli.exe ./cmd/relaykeys-cli

# Build the system tray app (Windows only)
go build -o relaykeys-tray.exe ./cmd/relaykeys-tray
```

On macOS/Linux, replace `.exe` with the appropriate binary name (or omit the extension).

## Tests

```bash
go test ./... -count=1
```

## Vet

```bash
go vet ./...
```

## Building the Installer (Windows)

From the repo root:

```bash
makensis /DVERSION=2.0.0 build-installer.nsi
```

This produces `RelayKeys-2.0.0-setup.exe`. The installer:

- Installs the daemon, CLI, and tray app
- Installs and starts the Windows service
- Creates desktop and Start Menu shortcuts
- Adds the tray app to the Startup folder
- Provides a clean uninstaller that stops and removes the service

## Cross-Compilation

RelayKeys is pure Go (no CGo required). Cross-compile with:

```bash
GOOS=windows GOARCH=amd64 go build -o relaykeys-daemon.exe ./cmd/relaykeys-daemon
GOOS=darwin  GOARCH=amd64 go build -o relaykeys-daemon     ./cmd/relaykeys-daemon
GOOS=linux   GOARCH=amd64 go build -o relaykeys-daemon     ./cmd/relaykeys-daemon
```

Note: The macOS menubar app (`cmd/relaykeys-menubar`) requires CGo and must be built on macOS.

## Firmware

If you wish to create a UF2 file for the firmware, follow [this guide](https://learn.adafruit.com/adafruit-metro-m0-express/uf2-bootloader-details#entering-bootloader-mode-2929745) (see "Making your own UF2") — noting that RelayKeys uses M4-based boards.
