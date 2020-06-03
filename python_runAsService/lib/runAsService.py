#!/usr/bin/env python
 
import sys, os, time, atexit
from signal import SIGTERM
 
class runAsService:
    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
       
    def run_in_bg(self):
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)
       
        os.chdir("/")
        os.setsid()
        os.umask(0)
       
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)
       
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
    
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile,'w+').write("%s\n" % pid)
  
    def delpid(self):
        os.remove(self.pidfile)
 
    def start(self):
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
   
        if pid:
            if self.pidIsAlive(pid):
                sys.stderr.write("Service is already running with PID: %s.\n" % (pid))
                sys.exit(1)
         
        sys.stdout.write("Starting service.\n")
        self.run_in_bg()
        self.run()
 
    def stop(self):
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
       
        if not pid:
            sys.stderr.write("Service is not running.\n")
            return 
        elif not self.pidIsAlive(pid):
            sys.stderr.write("Service is not running.\n")
            return 

        sys.stdout.write("Stopping Service.\n")
 
        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print str(err)
                sys.exit(1)

    def status(self):
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            sys.stderr.write("Service is not running.\n")
            return 
        elif not self.pidIsAlive(pid):
            sys.stderr.write("Service is not running.\n")
            return 
        else:
            sys.stderr.write("Service is running with PID: %s.\n" % (pid))

    def restart(self):
        self.stop()
        self.start()

    def pidIsAlive(self, pid):
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        else:
            return True

    def run(self):
        '''
        override this method in subclass
        This is called after service is started in the background
        '''
