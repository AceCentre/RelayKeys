!define NAME "RelayKeys"
!define UNINSTKEY "${NAME}" ; Using a GUID here is not a bad idea
!define DEFAULTNORMALDESTINATON "$ProgramFiles\Ace Centre\${NAME}"
!define DEFAULTPORTABLEDESTINATON "$Desktop\${NAME}"
Name "${NAME}"
Outfile "${NAME} setup.exe"
;RequestExecutionlevel highest
RequestExecutionLevel admin ;Require admin rights on NT6+ (When UAC is turned on)
SetCompressor LZMA
;SetCompress Off

Var NormalDestDir
Var PortableDestDir
Var PortableMode

!include LogicLib.nsh
!include FileFunc.nsh
!include MUI2.nsh

!insertmacro MUI_PAGE_WELCOME
Page Custom PortableModePageCreate PortableModePageLeave
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_LANGUAGE English


Function .onInit
    Call RequireAdmin
    StrCpy $NormalDestDir "${DEFAULTNORMALDESTINATON}"
    StrCpy $PortableDestDir "${DEFAULTPORTABLEDESTINATON}"

    ${GetParameters} $9

    ClearErrors
    ${GetOptions} $9 "/?" $8
    ${IfNot} ${Errors}
        MessageBox MB_ICONINFORMATION|MB_SETFOREGROUND "\
          /PORTABLE : Extract application to USB drive etc$\n\
          /S : Silent install$\n\
          /D=%directory% : Specify destination directory$\n"
        Quit
    ${EndIf}

    ClearErrors
    ${GetOptions} $9 "/PORTABLE" $8
    ${IfNot} ${Errors}
        StrCpy $PortableMode 1
        StrCpy $0 $PortableDestDir
    ${Else}
        StrCpy $PortableMode 0
        StrCpy $0 $NormalDestDir
        ${If} ${Silent}
            Call RequireAdmin
        ${EndIf}
    ${EndIf}

    ${If} $InstDir == ""
        ; User did not use /D to specify a directory, 
        ; we need to set a default based on the install mode
        StrCpy $InstDir $0
    ${EndIf}
    Call SetModeDestinationFromInstdir
FunctionEnd


Function RequireAdmin
    UserInfo::GetAccountType
    Pop $8
    ${If} $8 != "admin"
        MessageBox MB_ICONSTOP "You need administrator rights to install ${NAME}"
        SetErrorLevel 740 ;ERROR_ELEVATION_REQUIRED
        Abort
    ${EndIf}
FunctionEnd


Function SetModeDestinationFromInstdir
    ${If} $PortableMode = 0
        StrCpy $NormalDestDir $InstDir
    ${Else}
        StrCpy $PortableDestDir $InstDir
    ${EndIf}
FunctionEnd


Function PortableModePageCreate
    Call SetModeDestinationFromInstdir ; If the user clicks BACK on the directory page we will remember their mode specific directory
    !insertmacro MUI_HEADER_TEXT "Install Mode" "Choose how you want to install ${NAME}."
    nsDialogs::Create 1018
    Pop $0
    ${NSD_CreateLabel} 0 10u 100% 24u "Select install mode:"
    Pop $0
    ${NSD_CreateRadioButton} 30u 50u -30u 8u "Normal install"
    Pop $1
    ${NSD_CreateRadioButton} 30u 70u -30u 8u "Portable"
    Pop $2
    ${If} $PortableMode = 0
        SendMessage $1 ${BM_SETCHECK} ${BST_CHECKED} 0
    ${Else}
        SendMessage $2 ${BM_SETCHECK} ${BST_CHECKED} 0
    ${EndIf}
    nsDialogs::Show
FunctionEnd

Function PortableModePageLeave
    ${NSD_GetState} $1 $0
    ${If} $0 <> ${BST_UNCHECKED}
        StrCpy $PortableMode 0
        StrCpy $InstDir $NormalDestDir
        Call RequireAdmin
    ${Else}
        StrCpy $PortableMode 1
        StrCpy $InstDir $PortableDestDir
    ${EndIf}
FunctionEnd



Section
    SimpleSC::ExistsService "RelayKeysDaemon"
    Pop $0
    ${If} $0 == 0
        SimpleSC::ServiceIsRunning "RelayKeysDaemon"
        Pop $0
        Pop $1
        ${If} $0 == 0
            ${If} $1 == 1
                ;MessageBox MB_OK "Service exists and running" 
                SimpleSC::StopService "RelayKeysDaemon" 10 30            
            ${EndIf}
        ${EndIf}
    ${EndIf}
    
    SetOutPath "$InstDir"
    File "relaykeysd-service-restart.bat"
    File /r ..\dist\relaykeysd\*
    SetShellVarContext all
    ;create start-menu items
      CreateDirectory "$SMPROGRAMS\Ace Centre\RelayKeys"
      CreateShortCut "$SMPROGRAMS\Ace Centre\RelayKeys\RelayKeys.lnk" "$INSTDIR\relaykeys-qt.exe" "" "$INSTDIR\relaykeys-qt.exe" 0
      CreateShortCut "$SMPROGRAMS\Ace Centre\RelayKeys\RelayKeys-Config.lnk" "$INSTDIR\relaykeys.cfg" "" "$INSTDIR\relaykeys.cfg" 0
      CreateShortCut "$SMPROGRAMS\Ace Centre\RelayKeys\Help.lnk" "$INSTDIR\README.html" "" "$INSTDIR\README.html" 0
      CreateShortCut "$SMPROGRAMS\Ace Centre\RelayKeys\Uninstall.lnk" "$INSTDIR\Uninstall.exe" "" "$INSTDIR\Uninstall.exe" 0
      CreateShortCut "$SMPROGRAMS\Ace Centre\RelayKeys\Restart-RelayKeys.lnk" "$INSTDIR\relaykeysd-service-restart.bat" "" "$INSTDIR\relaykeysd-service-restart.bat" 0
      CreateShortcut "$DESKTOP\RelayKeys-QT.lnk" "$INSTDIR\relaykeys-qt.exe"

    ; SimpleSC Plugin: https://nsis.sourceforge.io/NSIS_Simple_Service_Plugin
    SimpleSC::InstallService "RelayKeysDaemon" "Relay Keys Daemon" 16 2 '"$INSTDIR\relaykeysd-service.exe"'
    Pop $0
    SimpleSC::StartService "RelayKeysDaemon" "" 30
    Pop $0

    ${If} $PortableMode = 0
        WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${UNINSTKEY}" "DisplayName" "${NAME}"
        WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${UNINSTKEY}" "UninstallString" '"$INSTDIR\uninstall.exe"'
        WriteUninstaller "$INSTDIR\uninstall.exe"
    ${Else}
        ; Create the file the application uses to detect portable mode
        FileOpen $0 "$INSTDIR\portable.dat" w
        FileWrite $0 "PORTABLE"
        FileClose $0
    ${EndIf}
SectionEnd


Section Uninstall
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${UNINSTKEY}"
    SimpleSC::StopService "RelayKeysDaemon" 10 30
    SimpleSC::RemoveService "RelayKeysDaemon"
    Delete "$INSTDIR\uninstall.exe"
    SetShellVarContext all
    Delete "$SMPROGRAMS\Ace Centre\RelayKeys\RelayKeys.lnk"
    Delete "$SMPROGRAMS\Ace Centre\RelayKeys\Help.lnk"
    Delete "$SMPROGRAMS\Ace Centre\RelayKeys\Uninstall.lnk"
    Delete "$SMPROGRAMS\Ace Centre\RelayKeys\Restart-RelayKeys.lnk"
    Delete "$SMPROGRAMS\Ace Centre\RelayKeys\Restart-Config.lnk"
    Delete "$DESKTOP\RelayKeys-QT.lnk"
    RMDir /r "$INSTDIR"
SectionEnd