import socket
import sys
import time
import struct
from array import array
from header import *

"""****************************************
	    DEFINITIONS:
****************************************"""

def get_value_of_data(data):
    return int(data.encode('hex'),16)

def getPointsFromMeasures(measures, numOfPoints):
    points = []
    k=0
    #measures = measures.encode('hex')
    while (k < numOfPoints* Point.SizeOfPoint):
	layer = measures[k:k+1].encode('hex')
	flags = measures[k+1:k+2].encode('hex')
	ANGLE = (measures[k+2:k+4])[::-1].encode('hex')
	try:
	    angle = int(ANGLE,16)
	except:
	    angle = 0
	DIST = (measures[k+4:k+6])[::-1].encode('hex')#+(measures[k+4:k+5].encode('hex'))
	try:
	    dist  = int(DIST,16)
	except:
	    dist = 0
	p = Point(layer, angle, dist, flags)
	#print 'point: ', layer,', ', flags,', ', angle,', ', dist
	points.append(p)
	k += Point.SizeOfPoint
    return points
    
def getMeasureData(data):
    md = MeasureData()
    i=0
    for k in range(len(MeasureData.MeasureData_sizes)):
	md.set_item_by_index(k, get_value_of_data(data[i: (i+MeasureData.MeasureData_sizes[k])]) )
	i+=MeasureData.MeasureData_sizes[k]
    return md
    
def getHeaderFromData(data):
    header = IbeoData()
    i=0
    for k in range(len(IbeoData.header_sizes)):
	header.set_item_by_index(k, (data[i: (i+IbeoData.header_sizes[k])]).encode('hex') )
	#print 'data ', k, ': ',  data[i: (i+IbeoData.header_sizes[k])].encode('hex')
	#print '        ', data[i: (i+IbeoData.header_sizes[k])][::-1].encode('hex')
	i+=IbeoData.header_sizes[k]
    return header
    

"""****************************************
	    READER:
****************************************"""    
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('192.168.0.6', 12002)
#print >>sys.stderr, 'connecting to %s port %s' % server_address

sock.connect(server_address)

i=0
try:
    
    
    for j in range(50000):
	magicWord = ['','','','']
	i=0
	while ((magicWord[(i+0)%4] != 'af')
	or (magicWord[(i+1)%4] != 'fe')
	or (magicWord[(i+2)%4] != 'c0')
	or (magicWord[(i+3)%4] != 'c2') ):
	    data = sock.recv(1).encode('hex')
	    magicWord[i%4] = data
	    i+=1
	  
	#found magic word, now put values in the objects
	if not i==4:
	    print "something is wrong. i=",i
	    i=4
	h = sock.recv(IbeoData.SizeOfHeader-4)
	ibeo_message = getHeaderFromData(h)
	i+=20
	"""
	for k in range(len(header_sizes)):
	    ibeo_message.set_item_by_index(k, sock.recv(header_sizes[k]).encode('hex'))
	    i += header_sizes[k]
	"""
	
	restMessageSize = int(ibeo_message.dict['size'],16)
	print 'restMessageSize ', restMessageSize,', hex:' , ibeo_message.dict['size']
	message = ''
	while restMessageSize > 0:
	    inp_message = sock.recv(restMessageSize)
	    message += inp_message
	    restMessageSize -= len(inp_message)
	if len(message) != int(ibeo_message.dict['size'],16):
	    print "Did not collect all of the message"
	if ibeo_message.dict['dataType'] == '2202':
	    # dataType is 2202 so the IBEO is sending measured points:
	    #print (int(ibeo_message.dict['size'],16) + 24)
	    
	    while i < len(message) + IbeoData.SizeOfHeader:
		
		MD = message[i: i+MeasureData.SizeOfMeasureData]
		IBEOmeasure = getMeasureData(MD)
		i+= MeasureData.SizeOfMeasureData
		
		IBEOmeasure.dict['points'] = []
		
		measures = message[i: i+(MeasureData.numOfPoints*Point.SizeOfPoint) ]
		points = getPointsFromMeasures(measures, MeasureData.numOfPoints)
		IBEOmeasure.dict['points'] = points
		i += MeasureData.numOfPoints*Point.SizeOfPoint
		

		ibeo_message.dict['messages'].append(IBEOmeasure)
		#print "magic word",time.ctime(time.time()),':',MeasureData.numOfPoints
	
	else:
	    if ibeo_message.dict['dataType'] == '2030':
		print 'data type is 2030- message: ' ,message[:8].encode('hex')
	    else:
		print 'data type is: ', ibeo_message.dict['dataType']	  
	
	    
finally:
    print >>sys.stderr, 'closing socket'
    sock.close()
