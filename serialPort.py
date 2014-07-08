__author__ = 'lar5'
import serial
ser = serial.Serial('/dev/fw2', 115200, timeout=0)
ser.open()
print ("connected to: " + ser.portstr)
count=0
try:
    while True:
        line =ser.readline() # should block, not take anything less than 14 bytes
        if line:
            # Here I want to process 14 bytes worth of data and have
            # the data be consistent.
            print ("line(" + str(count) + ")=" + line)
            count=count+1
finally:
    ser.close()
