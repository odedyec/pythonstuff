__author__ = 'lar5'
import serial
ser = serial.Serial('/dev/ttyUSB1', 1200, timeout=0)
ser.open()
print "connected to: " + ser.portstr
count=0
while True:
    line =ser.readline(size=14) # should block, not take anything less than 14 bytes
    if line:
        # Here I want to process 14 bytes worth of data and have
        # the data be consistent.
        print "line(" + str(count) + ")=" + line
        count=count+1
ser.close()