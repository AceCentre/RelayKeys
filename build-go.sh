#!/bin/bash
set -e

VERSION=${VERSION:-"2.0.0"}
LDFLAGS="-s -w -X main.version=$VERSION"
OUTDIR="./build-go"

rm -rf $OUTDIR
mkdir -p $OUTDIR

echo "Building RelayKeys v$VERSION..."

echo "  macOS arm64 (native CGo)..."
CGO_ENABLED=1 GOOS=darwin GOARCH=arm64 go build -ldflags "$LDFLAGS" -o $OUTDIR/relaykeys-daemon-darwin-arm64 ./cmd/relaykeys-daemon
CGO_ENABLED=0 GOOS=darwin GOARCH=arm64 go build -ldflags "$LDFLAGS" -o $OUTDIR/relaykeys-cli-darwin-arm64 ./cmd/relaykeys-cli

echo "  macOS amd64 (native CGo)..."
CGO_ENABLED=1 GOOS=darwin GOARCH=amd64 go build -ldflags "$LDFLAGS" -o $OUTDIR/relaykeys-daemon-darwin-amd64 ./cmd/relaykeys-daemon
CGO_ENABLED=0 GOOS=darwin GOARCH=amd64 go build -ldflags "$LDFLAGS" -o $OUTDIR/relaykeys-cli-darwin-amd64 ./cmd/relaykeys-cli

echo "  Windows amd64..."
if command -v x86_64-w64-mingw32-gcc &>/dev/null; then
    CGO_ENABLED=1 GOOS=windows GOARCH=amd64 CC=x86_64-w64-mingw32-gcc go build -ldflags "$LDFLAGS" -o $OUTDIR/relaykeys-daemon-windows-amd64.exe ./cmd/relaykeys-daemon
else
    echo "    (no MinGW cross-compiler — building without capture support)"
    CGO_ENABLED=0 GOOS=windows GOARCH=amd64 go build -ldflags "$LDFLAGS" -o $OUTDIR/relaykeys-daemon-windows-amd64.exe ./cmd/relaykeys-daemon
fi
CGO_ENABLED=0 GOOS=windows GOARCH=amd64 go build -ldflags "$LDFLAGS" -o $OUTDIR/relaykeys-cli-windows-amd64.exe ./cmd/relaykeys-cli

echo "  Linux amd64..."
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags "$LDFLAGS" -o $OUTDIR/relaykeys-daemon-linux-amd64 ./cmd/relaykeys-daemon
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags "$LDFLAGS" -o $OUTDIR/relaykeys-cli-linux-amd64 ./cmd/relaykeys-cli

echo ""
echo "Copying keymaps..."
cp -r keymaps $OUTDIR/

echo ""
echo "Build complete. Binaries in $OUTDIR/:"
ls -lh $OUTDIR/
