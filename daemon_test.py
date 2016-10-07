#!/usr/bin/env python
#coding: utf-8
import sys,os
import signal

lock = '/tmp/daemon.lock'

def daemonize(stdin="/dev/null", stdout="/dev/null", stderr="/dev/null"):
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, e:
        sys.stderr.write("fork #1 failed: (%d) %s\n" % (e.errno, e.stderror))
        sys.exit(1)

    os.chdir("/")
    os.umask(0)
    os.setsid()

    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, e:
        sys.stderr.write("fork #1 failed: (%d) %s\n" % (e.errno, e.stderror))
        sys.exit(1)

    for f in sys.stdout, sys.stderr: f.flush
    si = open(stdin, 'r')
    so = open(stdout, 'a+')
    se = open(stderr, 'a+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

def on_signal(signum, frame):
    if os.path.exists(lock):
        os.remove(lock)
        sys.stdout.write('Bye from process %d\n'%os.getpid())
    sys.exit(0)

def check_lock():
    signal.signal(signal.SIGTERM, on_signal)
    signal.signal(signal.SIGINT, on_signal)
    signal.signal(signal.SIGQUIT, on_signal)

    try:
        lock_file = file(lock, 'r')
        pid = int(lock_file.read().strip())
    except Exception as e:
        sys.stdout.write('No Instance, creating ... \n')
        pid = None

    if pid:
        sys.stdout.write('instance is already in running \n')
        sys.exit(0)

    file(lock, 'w+').write('%s\n' % os.getpid())

def main():
    import time
    f = open('/tmp/my-log', 'w')
    pid = os.getpid()
    sys.stdout.write('%s: Daemon started with pid %d\n' % (time.ctime(time.time()),pid))

    while True:
        f.write('Process %d \t Time %s\n' % (pid, time.ctime(time.time())))
        f.flush()
        time.sleep(10)

if __name__ == "__main__":
    print "DAEMON-TEST"

    daemonize('/dev/null','/tmp/daemon_stdout.log','/tmp/daemon_error.log')
    check_lock()
    main()
