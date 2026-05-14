#!/bin/bash
set -e

VERSION=${VERSION:-"2.0.0"}
OUTDIR="./build-go"
APPDIR="$OUTDIR/RelayKeys.app"

echo "Building macOS app bundle..."

# Build the menu bar binary
echo "  Building relaykeys-menubar..."
CGO_ENABLED=1 go build -ldflags "-s -w -X main.version=$VERSION" -o "$OUTDIR/relaykeys-menubar" ./cmd/relaykeys-menubar

# Build the daemon
echo "  Building relaykeys-daemon..."
CGO_ENABLED=1 go build -ldflags "-s -w -X main.version=$VERSION" -o "$OUTDIR/relaykeys-daemon" ./cmd/relaykeys-daemon

# Build the CLI
echo "  Building relaykeys-cli..."
CGO_ENABLED=1 go build -ldflags "-s -w -X main.version=$VERSION" -o "$OUTDIR/relaykeys-cli" ./cmd/relaykeys-cli

# Create .app bundle
echo "  Creating .app bundle..."
rm -rf "$APPDIR"
mkdir -p "$APPDIR/Contents/MacOS"
mkdir -p "$APPDIR/Contents/Resources"

cp "$OUTDIR/relaykeys-menubar" "$APPDIR/Contents/MacOS/RelayKeys"

cat > "$APPDIR/Contents/Info.plist" << PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>RelayKeys</string>
    <key>CFBundleIdentifier</key>
    <string>com.acecentre.relaykeys</string>
    <key>CFBundleName</key>
    <string>RelayKeys</string>
    <key>CFBundleDisplayName</key>
    <string>RelayKeys</string>
    <key>CFBundleVersion</key>
    <string>$VERSION</string>
    <key>CFBundleShortVersionString</key>
    <string>$VERSION</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleIconFile</key>
    <string>AppIcon</string>
    <key>LSUIElement</key>
    <true/>
    <key>LSMinimumSystemVersion</key>
    <string>11.0</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>NSHumanReadableCopyright</key>
    <string>Copyright Ace Centre. MIT License.</string>
</dict>
</plist>
PLIST

# Copy icon if available
if [ -f "assets/icons/logo.png" ]; then
    cp assets/icons/logo.png "$APPDIR/Contents/Resources/AppIcon.png"
fi

echo "  App bundle: $APPDIR"
echo "  Done."
