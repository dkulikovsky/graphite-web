#!/usr/bin/python -u
import socket
import sys
import time
import cmath

if len(sys.argv) > 1:
        if sys.argv[1].isdigit():
                offset = int(sys.argv[1])
        else:  
                offset = 0
else:  
        offset = 0

size = [2500,3000]
while 1:
        ts = "%d" % time.time()
        start_t = time.time()
        for i in xrange(int(size[0])):
                out = ""
                for j in xrange(size[1]):
                        sin_ij = cmath.sin(float(ts[0:-1]+"."+ts[-1]))+j
                        out += "test.test%d.test%d %f %s\n" % (i+offset,j,sin_ij.real,ts)
                out += "\n\n"
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(("127.0.0.1", 2024))
                s.send(out)
                s.close()
        delay = time.time() - start_t
        print "Sending %d took %f" % (size[0]*size[1],delay)
        if delay < 60:
                time.sleep(60 - delay)
                print "slept for %f" % (60 - delay)
                speed = size[0]*size[1]/delay
                print "speed %f" % speed
        else:  
                print "overtime for %f " % (delay - 60)
                speed = size[0]*size[1]/delay
                overflow = (delay - 60) * speed
                print "speed %f, overflow %f" % (speed, overflow)

