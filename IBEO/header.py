from math import pi
import numpy
class Point:
    
    def __init__(self, layerEcho, flags, horizAngle, RadialDist,echoPulseWidth):
	self._flags = flags
	self._layerEcho = layerEcho
	self._horizAngle = horizAngle
	self._RadialDist = RadialDist
	self._EchoPulseWidth = echoPulseWidth
	
	self._layer = 0
	self._echo = 0
	self.processData()
	
    def processData(self):
	self._layer = self._layerEcho%4
	self._echo = (self._layerEcho - self._layer)/16


from robil_msgs.msg import MultiLaserScan
import rospy
class MeasureData:
  
    def __init__(self):
      self._rosPointArray = MultiLaserScan()
    
    def set_point_array_as_ROS(self,pointArray,startAngle,endAngle,increment):
      self._rosPointArray.header.frame_id = 'ibeo'
      self._rosPointArray.header.stamp = rospy.Time.now()
      
      self._rosPointArray.angle_increment = 2*pi / increment
      self._rosPointArray.angle_t1 = 0.014
      self._rosPointArray.angle_t2 = 0.028
      self._rosPointArray.angle_b1 = -0.014
      self._rosPointArray.angle_b2 = -0.028
      tmin = bmin = rmin = 10000
      rmax = tmax =  bmax = -10000
      for point in pointArray:
	ang = 2 * pi * numpy.int16(numpy.uint16(point._horizAngle)) / increment
	if rmin > point._RadialDist/100.0:
	  rmin = point._RadialDist/100.0
	if rmax < point._RadialDist/100.0:
	  rmax = point._RadialDist/100.0
	
	if point._layer == 0:
	  self._rosPointArray.ranges_b2.append(point._RadialDist/100.0)
	  if ang > bmax:
	    bmax = ang
	  elif ang < bmin:
	    bmin = ang	  
	elif point._layer == 1:
	  self._rosPointArray.ranges_b1.append(point._RadialDist/100.0)
	  if ang > bmax:
	    bmax = ang
	  elif ang < bmin:
	    bmin = ang	 
	elif point._layer == 3:
	  self._rosPointArray.ranges_t2.append(point._RadialDist/100.0)
	  if ang > tmax:
	    tmax = ang
	  elif ang < tmin:
	    tmin = ang	 
	elif point._layer == 2:
	  self._rosPointArray.ranges_t1.append(point._RadialDist/100.0)
	  if ang > tmax:
	    tmax = ang
	  elif ang < tmin:
	    tmin = ang	 
      self._rosPointArray.angle_min_t = tmin
      self._rosPointArray.angle_max_t = tmax
      self._rosPointArray.angle_min_b = bmin
      self._rosPointArray.angle_max_b = bmax
      self._rosPointArray.range_min = rmin
      self._rosPointArray.range_max = rmax+1
	
	
      
	  
	  
class IbeoData:
    
    SizeOfHeader = 24
    header_sizes = [4,4,1,1,2,8]
    
    def __init__(self):
	self.variables = ['prevSize','size','reserved','devID','dataType','NTPtime','messages']
	self.dict = {'prevSize':0,'size':0,'reserved':0,'devID':0,'dataType':0,'NTPtime':0,'messages':[]}
	
    def set_item_by_index(self, idx, value):
	self.set_item_by_name(self.variables[idx],value)

    def set_item_by_name(self, name, value):
	self.dict[name] = value
	
    def print_items_values(self,enters=0):
	for item in self.dict:
	    print item,': ',self.dict[item]
	for ent in range(enters):
	    print ''

class RobilIBEOMsg:
    
    def __init__(self):
	self.variables = ['header','angleMinT','angleMaxT','AngleMinB','angleMaxB','angleInc',
			  'angleLayer1','angleLayer2','angleLayer3','angleLayer4','timeInc',
			  'scanTime','rangeMin','rangeMax','rangesL1','rangesL2','rangesL3','rangesL4']
			  
	self.dict = ['header','angleMinT','angleMaxT','AngleMinB','angleMaxB','angleInc',
		    'angleLayer1','angleLayer2','angleLayer3','angleLayer4','timeInc',
		    'scanTime','rangeMin','rangeMax','rangesL1','rangesL2','rangesL3','rangesL4']
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    