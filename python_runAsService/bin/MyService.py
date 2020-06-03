#!/usr/bin/env python

import os, sys, time, atexit
import pwd
import grp
import stat

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(os.path.dirname(here), 'lib'))

from runAsService import runAsService

class MyService(runAsService):

    def run(self):
        while True:
            '''
            Do your stuff here.
            Example: Sleep 1 second forever untill service is running
            '''
            time.sleep(1)


if __name__ == "__main__":
    MyService_PID = '/var/run/MyService.pid'
    Service = MyService(MyService_PID)
    if len(sys.argv) == 2:
        if sys.argv[1] == 'start':
            Service.start()
        elif sys.argv[1] == 'stop':
            Service.stop()
        elif sys.argv[1] == 'restart':
            Service.restart()
        elif sys.argv[1] == 'status':
            Service.status()
        else:
            print "Invalid argument"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s status|start|stop|restart" % sys.argv[0]
        sys.exit(2)
