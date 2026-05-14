$ErrorActionPreference = "Stop"

$VERSION = if ($env:VERSION) { $env:VERSION } else { "2.0.0" }
$LDFLAGS = "-s -w -X main.version=$VERSION"
$OUTDIR = ".\build-go"

Remove-Item -Recurse -Force $OUTDIR -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path $OUTDIR | Out-Null

Write-Host "Building RelayKeys v$VERSION..."

$goExe = "go"
if (-not (Get-Command $goExe -ErrorAction SilentlyContinue)) {
    $goExe = "C:\Program Files\Go\bin\go.exe"
}

$gccPath = $null
if (Get-Command gcc -ErrorAction SilentlyContinue) {
    $gccPath = "gcc"
} elseif (Test-Path "C:\mingw64\bin\gcc.exe") {
    $gccPath = "C:\mingw64\bin\gcc.exe"
}

if ($gccPath) {
    Write-Host "  Windows amd64 (CGo capture support)..."
    $env:CGO_ENABLED = "1"
    $env:CC = $gccPath
    & $goExe build -ldflags $LDFLAGS -o "$OUTDIR\relaykeys-daemon-windows-amd64.exe" .\cmd\relaykeys-daemon
    if ($LASTEXITCODE -ne 0) { throw "daemon CGo build failed" }
    $env:CGO_ENABLED = "0"
    Remove-Item Env:\CC -ErrorAction SilentlyContinue
} else {
    Write-Host "  Windows amd64 (no CGo - capture disabled)..."
    $env:CGO_ENABLED = "0"
    & $goExe build -ldflags $LDFLAGS -o "$OUTDIR\relaykeys-daemon-windows-amd64.exe" .\cmd\relaykeys-daemon
    if ($LASTEXITCODE -ne 0) { throw "daemon build failed" }
}

& $goExe build -ldflags $LDFLAGS -o "$OUTDIR\relaykeys-cli-windows-amd64.exe" .\cmd\relaykeys-cli
if ($LASTEXITCODE -ne 0) { throw "cli build failed" }

Write-Host "  Running tests..."
& $goExe test ./... -count=1
if ($LASTEXITCODE -ne 0) { throw "tests failed" }

Write-Host ""
Write-Host "Copying keymaps, macros, and assets..."
if (-not (Test-Path "$OUTDIR\keymaps")) { Copy-Item -Path keymaps -Destination $OUTDIR -Recurse -Container }
if (Test-Path macros) {
    if (-not (Test-Path "$OUTDIR\macros")) { Copy-Item -Path macros -Destination $OUTDIR -Recurse -Container }
} else {
    New-Item -ItemType Directory -Path "$OUTDIR\macros" | Out-Null
}
if (Test-Path assets) {
    Copy-Item -Path assets -Destination $OUTDIR -Recurse -Container
}

Write-Host ""
Write-Host "Build complete:"
Get-ChildItem $OUTDIR | Format-Table Name, Length

$makensis = $null
if (Test-Path "C:\Program Files (x86)\NSIS\makensis.exe") {
    $makensis = "C:\Program Files (x86)\NSIS\makensis.exe"
} elseif (Get-Command makensis -ErrorAction SilentlyContinue) {
    $makensis = "makensis"
}

if ($makensis) {
    Write-Host ""
    Write-Host "Building NSIS installer..."
    & $makensis "/DVERSION=$VERSION" build-installer.nsi
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Installer: RelayKeys-$VERSION-setup.exe"
    }
}
