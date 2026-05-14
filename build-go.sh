#!/bin/bash
set -e

VERSION=${VERSION:-"2.0.0"}
LDFLAGS="-s -w -X main.version=$VERSION"
OUTDIR="./build-go"

rm -rf $OUTDIR
mkdir -p $OUTDIR

echo "Building RelayKeys v$VERSION..."

# macOS: CGO_ENABLED=1 required for go.bug.st/serial (IOKit/CoreFoundation)
echo "  macOS arm64..."
CGO_ENABLED=1 GOOS=darwin GOARCH=arm64 go build -ldflags "$LDFLAGS" -o $OUTDIR/relaykeys-daemon-darwin-arm64 ./cmd/relaykeys-daemon
CGO_ENABLED=1 GOOS=darwin GOARCH=arm64 go build -ldflags "$LDFLAGS" -o $OUTDIR/relaykeys-cli-darwin-arm64 ./cmd/relaykeys-cli

echo "  macOS amd64..."
CGO_ENABLED=1 GOOS=darwin GOARCH=amd64 go build -ldflags "$LDFLAGS" -o $OUTDIR/relaykeys-daemon-darwin-amd64 ./cmd/relaykeys-daemon
CGO_ENABLED=1 GOOS=darwin GOARCH=amd64 go build -ldflags "$LDFLAGS" -o $OUTDIR/relaykeys-cli-darwin-amd64 ./cmd/relaykeys-cli

# Windows: CGO_ENABLED=0 is fine — serial enumerator has a pure-Go Windows impl
# Capture module (capture_windows.go) needs CGO, build separately with MinGW if available
echo "  Windows amd64..."
CGO_ENABLED=0 GOOS=windows GOARCH=amd64 go build -ldflags "$LDFLAGS" -o $OUTDIR/relaykeys-daemon-windows-amd64.exe ./cmd/relaykeys-daemon
CGO_ENABLED=0 GOOS=windows GOARCH=amd64 go build -ldflags "$LDFLAGS" -o $OUTDIR/relaykeys-cli-windows-amd64.exe ./cmd/relaykeys-cli

# Linux: pure Go, no CGO needed
echo "  Linux amd64..."
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags "$LDFLAGS" -o $OUTDIR/relaykeys-daemon-linux-amd64 ./cmd/relaykeys-daemon
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags "$LDFLAGS" -o $OUTDIR/relaykeys-cli-linux-amd64 ./cmd/relaykeys-cli

echo ""
echo "Running tests..."
CGO_ENABLED=1 go test ./... -count=1

echo ""
echo "Copying keymaps and macros..."
cp -r keymaps $OUTDIR/
mkdir -p $OUTDIR/macros

echo ""
echo "Build complete. Binaries in $OUTDIR/:"
ls -lh $OUTDIR/
