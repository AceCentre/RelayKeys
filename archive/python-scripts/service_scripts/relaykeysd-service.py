# win32 service impl
import socket
from sys import argv

import servicemanager
from win32event import WAIT_OBJECT_0, CreateEvent, SetEvent, WaitForSingleObject
from win32service import SERVICE_STOP_PENDING
from win32serviceutil import HandleCommandLine, ServiceFramework

import relaykeysd


class RelayKeysService(ServiceFramework):
    _svc_name_ = "RelayKeysDaemon"
    _svc_display_name_ = "Relay Keys Daemon"

    def __init__(self, args):
        ServiceFramework.__init__(self, args)
        self.hWaitStop = CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def _interrupt(self):
        rc = WaitForSingleObject(self.hWaitStop, 0)
        if rc == WAIT_OBJECT_0:
            raise SystemExit()

    def SvcStop(self):
        self.ReportServiceStatus(SERVICE_STOP_PENDING)
        SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        relaykeysd.main(interrupt=self._interrupt)


if __name__ == "__main__":
    # PyInstaller needs this
    if len(argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(RelayKeysService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        HandleCommandLine(RelayKeysService)
