# Developing without a board

If you don't have an nRF52840 dongle connected, you can still develop and test RelayKeys.

## Built-in simulator

RelayKeys includes a full firmware simulator (`internal/simulator`) that responds to AT commands just like the real hardware. The test suite uses this simulator to verify RPC commands end-to-end.

Run the tests:

```bash
go test ./... -count=1
```

## Running without serial

Use the `--noserial` flag to start the daemon without attempting a serial connection:

```bash
relaykeys-daemon.exe --noserial --debug
```

The web UI (`http://127.0.0.1:5383/ui/`) and JSON-RPC server will still work — they just won't be able to send commands to a BLE device.

You can also point the daemon at a non-existent COM port:

```bash
relaykeys-daemon.exe --dev=COM99 --debug
```

## Testing with the CLI

The CLI client works against the daemon's RPC server regardless of whether hardware is connected:

```bash
relaykeys-cli.exe daemon
relaykeys-cli.exe devlist
```

Commands that require the dongle (type, keypress, mouse) will return errors when no hardware is connected, but the RPC communication path is still exercised.
