import sys
import time
from datetime import datetime

import win32api
import win32event
import win32service
import win32serviceutil
import servicemanager
import logging

import BusClock


class MyService(win32serviceutil.ServiceFramework):

    _svc_name_ = "MYBusClock"
    _svc_display_name_ = "MyBusClock"
    _svc_description_ = "提醒公交车到站时间，帮助我节约时间"

    def __init__(self, args):
        logging.basicConfig(filename=r'D:\busclock.log', level=logging.INFO)
        logging.info("init")
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.isAlive = True
        self.loopWaitSeconds = 5
        self.busClock = BusClock.BjBusClock(logging)

    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        try:
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            logging.info('start')
            self.start()
            logging.info('wait')
            win32event.WaitForSingleObject(
                self.stop_event, win32event.INFINITE)
            logging.info('done')
        except BaseException as e:
            logging.info('Exception : %s' % e)
            self.SvcStop()

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        logging.info('stopping')
        self.stop()
        logging.info('stopped')
        win32event.SetEvent(self.stop_event)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def start(self):
        logging.info("svc do run....")
        while self.isAlive:
            self.busClock.run()
            time.sleep(self.loopWaitSeconds)

    def stop(self):
        self.isAlive = False
        pass

if __name__ == "__main__":
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(MyService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(MyService)
