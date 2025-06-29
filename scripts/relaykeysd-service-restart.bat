:: Comment, Run this command as administrator
@echo off
echo Checking RelayKeys service...
echo Current directory: %~dp0
echo Looking for: "%~dp0relaykeysd-service.exe"

if exist "%~dp0relaykeysd-service.exe" (
    echo Service executable found!
    echo Attempting to restart service...
    "%~dp0relaykeysd-service.exe" restart
) else (
    echo ERROR: Service executable not found!
    echo Please check installation.
    pause
)