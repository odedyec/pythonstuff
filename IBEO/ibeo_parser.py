from header import *
import rospy

rospy.init_node('ibeo')
pub = rospy.Publisher('/SENSORS/IBEO/2',MultiLaserScan)
f = open('IBEOReading.txt','r')
st = f.read()#.encode('hex')


def findMagicWord(st,start=0):
    return st.find('affec0c2',start)

def getLittleEndian(st,idx,offset,size,value):
    try:
      if size == 1:
	  return value + int(st[idx+offset*2:idx+offset*2+2],16)
      beg = idx+(offset+size-1)*2
      en = idx+(offset+size-1)*2+2
      h = st[beg:en]
      return getLittleEndian(st,idx,offset,size-1,(value + int(h,16)) * int('0x100',16))
    except:
      return -1
      
def littleEndian(st):
    try:
      LE = ''
      for i in range(1,len(st)/2+1 ):
	  LE += st[len(st)-2*i: len(st)-2*i +2]
      return LE
    except:
      return -1
    
def getBigEndian(st,idx,offset,size,as_hex=1):
  if as_hex:
    return st[idx+offset*2:idx+offset*2+size*2]
  else:
    return int(st[idx+offset*2:idx+offset*2+size*2],16)

def uint2int(num):
  return numpy.int16(numpy.uint16(num))
  
idx = -1 
while(True):
    idx = findMagicWord(st,idx+1)
    if idx == -1:
        break
        print "-------------------------------------------"
        idx = -1
        continue
    size = int(getBigEndian(st,idx,8,4),16)
    dtype = getBigEndian(st,idx,14,2)
    step = getLittleEndian(st,idx,46,2,0)
    s = uint2int(getLittleEndian(st,idx,48,2,0))
    e = uint2int(getLittleEndian(st,idx,50,2,0))
    numOfPoints = getLittleEndian(st,idx,52,2,0)
    points = []
    for i in range((size-44)/10):
      layerEcho = getLittleEndian(st,idx,24+44+i*10,1,0)
      flag = getLittleEndian(st,idx,24+44+i*10 +1,1,0)
      HoAngle = getLittleEndian(st,idx,24+44+i*10 +2,2,0)
      #RD = int(littleEndian(st[idx+(24+44+i*10 +4)*2:idx+(24+44+i*10 +4)*2 +4]),16)
      RadDist = getLittleEndian(st,idx,24+44+i*10 +4,2,0)
      #print 'radDist: 'RD
      EchoPulseWidth = getLittleEndian(st,idx,24+44+i*10 +6,2,0)
      if layerEcho == -1 or flag == -1 or HoAngle == -1 or RadDist == -1 or EchoPulseWidth == -1:
	print 'message stopped. Should have been ',(size-44)/10
	break
      p = Point(layerEcho,flag,HoAngle,RadDist,EchoPulseWidth)
      points.append(p)
    rosPoints = MeasureData()
    rosPoints.set_point_array_as_ROS(points,s,e,step)
    pub.publish(rosPoints._rosPointArray)
    rospy.sleep(0.1)

    print str(idx).zfill(7), ": ",size, dtype, idx+2*size +24*2, " Measurement number: ", getLittleEndian(st,idx,24,2,0), "start: ",360.0*s/step," end: ",360.0*e/step," step: ",360.0/step, "#Points: ", numOfPoints,'should be: ',abs(360.0*e/step-360.0*s/step)/(360.0/step)/4
    
