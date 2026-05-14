!define NAME "RelayKeys"
!ifndef VERSION
  !define VERSION "2.0.0"
!endif
!define UNINSTKEY "${NAME}"
!define DEFAULTNORMALDESTINATON "$ProgramFiles\Ace Centre\${NAME}"
Name "${NAME} ${VERSION}"
Outfile "${NAME}-${VERSION}-setup.exe"
RequestExecutionLevel admin
SetCompressor LZMA

!include LogicLib.nsh
!include FileFunc.nsh
!include MUI2.nsh

!define MUI_ABORTWARNING
!define MUI_ICON "assets\icons\logo.ico"
!define MUI_UNICON "assets\icons\logo.ico"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_LANGUAGE English

Var IsUpgrade

Function .onInit
    StrCpy $InstDir "${DEFAULTNORMALDESTINATON}"
    StrCpy $IsUpgrade 0

    ClearErrors
    ReadRegStr $0 HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${UNINSTKEY}" "UninstallString"
    ${IfNot} ${Errors}
        StrCpy $IsUpgrade 1
    ${EndIf}
FunctionEnd

Section ""
    ${If} $IsUpgrade == 1
        DetailPrint "Stopping existing service..."
        SimpleSC::StopService "RelayKeys" 1 30
        Pop $0
        DetailPrint "Removing existing service..."
        SimpleSC::RemoveService "RelayKeys"
        Pop $0
        Sleep 2000
    ${EndIf}

    SetOutPath "$InstDir"
    File "build-go\relaykeys-daemon-windows-amd64.exe"
    File "build-go\relaykeys-cli-windows-amd64.exe"

    Rename "$InstDir\relaykeys-daemon-windows-amd64.exe" "$InstDir\relaykeys-daemon.exe"
    Rename "$InstDir\relaykeys-cli-windows-amd64.exe" "$InstDir\relaykeys-cli.exe"

    SetOutPath "$InstDir\keymaps"
    File /r "build-go\keymaps\*.*"

    SetOutPath "$InstDir\macros"
    File /r "build-go\macros\*.*"

    SetOutPath "$InstDir\assets\icons"
    File /r "build-go\assets\icons\*.*"

    SetShellVarContext all
    CreateDirectory "$SMPROGRAMS\Ace Centre\RelayKeys"
    CreateShortCut "$SMPROGRAMS\Ace Centre\RelayKeys\RelayKeys Web UI.lnk" "http://127.0.0.1:5383/ui/" "" "" 0
    CreateShortCut "$SMPROGRAMS\Ace Centre\RelayKeys\RelayKeys CLI.lnk" "cmd.exe" '/k "$InstDir\relaykeys-cli.exe"' "" 0
    CreateShortCut "$SMPROGRAMS\Ace Centre\RelayKeys\Uninstall.lnk" "$InstDir\uninstall.exe" "" "$InstDir\uninstall.exe" 0

    DetailPrint "Installing RelayKeys service..."
    SimpleSC::InstallService "RelayKeys" "RelayKeys Daemon" 16 2 '"$InstDir\relaykeys-daemon.exe"'
    Pop $0
    ${If} $0 == 0
        SimpleSC::SetServiceDescription "RelayKeys" "RelayKeys BLE HID daemon - Bluetooth keyboard/mouse relay via nRF52840 dongle"
        Pop $0
        DetailPrint "Starting RelayKeys service..."
        SimpleSC::StartService "RelayKeys" "" 30
        Pop $0
        ${If} $0 != 0
            SimpleSC::GetErrorMessage $0
            Pop $1
            MessageBox MB_ICONEXCLAMATION "Service installed but could not be started.$\n$\nError: $1$\n$\nTry starting it from services.msc."
        ${EndIf}
    ${Else}
        SimpleSC::GetErrorMessage $0
        Pop $1
        MessageBox MB_ICONEXCLAMATION "Could not install Windows service.$\n$\nError: $1$\n$\nYou can run relaykeys-daemon.exe directly instead."
    ${EndIf}

    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${UNINSTKEY}" "DisplayName" "${NAME} ${VERSION}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${UNINSTKEY}" "UninstallString" '"$InstDir\uninstall.exe"'
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${UNINSTKEY}" "DisplayVersion" "${VERSION}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${UNINSTKEY}" "Publisher" "Ace Centre"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${UNINSTKEY}" "InstallLocation" "$InstDir"
    WriteUninstaller "$InstDir\uninstall.exe"
SectionEnd

Section "Uninstall"
    DetailPrint "Stopping RelayKeys service..."
    SimpleSC::StopService "RelayKeys" 1 30
    Pop $0

    DetailPrint "Removing RelayKeys service..."
    SimpleSC::RemoveService "RelayKeys"
    Pop $0
    Sleep 2000

    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${UNINSTKEY}"

    SetShellVarContext all
    Delete "$SMPROGRAMS\Ace Centre\RelayKeys\RelayKeys Web UI.lnk"
    Delete "$SMPROGRAMS\Ace Centre\RelayKeys\RelayKeys CLI.lnk"
    Delete "$SMPROGRAMS\Ace Centre\RelayKeys\Uninstall.lnk"
    RMDir "$SMPROGRAMS\Ace Centre\RelayKeys"
    RMDir "$SMPROGRAMS\Ace Centre"

    Delete "$InstDir\uninstall.exe"
    RMDir /r "$InstDIR"
SectionEnd
