import rospy
from std_msgs.msg import Float64
from std_msgs.msg import Int8
from geometry_msgs.msg import PoseWithCovarianceStamped
from gazebo_msgs.msg import ModelStates
import simpleguitk as simplegui
from tf.transformations import euler_from_quaternion
import numpy, math

class var:
    def __init__(self):
        self.var = 0
    def set(self, val):
        self.var = val
    def get(self):
        return self.var
    def toggle(self):
        if self.var == 0:
            self.var = 1
        else:
            self.var = 0

def calc_error(car_loc,WP):
    dist = float((WP[0]-car_loc['x'])**2+(WP[1]-car_loc['y'])**2)**0.5
    des = math.atan2(WP[1]-car_loc['y'], WP[0]-car_loc['x'])
    #print "desired: ",des," act: ", car_loc['theta']
    ori_error =  180.0/math.pi*(des-car_loc['theta'])
    if ori_error<-180:
        ori_error += 360
    if ori_error>180:
        ori_error -= 360
    return dist, ori_error

def PID(dist,dt):
    s = dt/45
    g = dist*0.01
    if g<0.05:
        g = 0.05
    if dist<1.0:
        g = 0
    return g,s

class ROS:
    def __init__(self):
        self.speed = var()
        self.steer = var()
        self.brake = var()
        self.hb = var()
        self.hb.set(0)
        self.direction = var()
        self.direction.set(1)
        self.loc = {'x':0.0,'y':0.0,'theta':0.0}
        self.real_loc = {'x':0.0,'y':0.0,'theta':0.0}        
        rospy.init_node('operator')
        #Publishers
        self._gas = rospy.Publisher('/drivingVic/gas_pedal/cmd', Float64)
        self._brake = rospy.Publisher('/drivingVic/brake_pedal/cmd', Float64)
        self._wheel = rospy.Publisher('/drivingVic/hand_wheel/cmd', Float64)
        self._hand_brake = rospy.Publisher('/drivingVic/hand_brake/cmd', Float64)
        self._direction = rospy.Publisher('/drivingVic/direction/cmd', Int8)
        self._key = rospy.Publisher('/drivingVic/key/cmd', Int8)
        #Subscriber
        self._real_loc = rospy.Subscriber('/gazebo/model_states',ModelStates, self.real_location)  
      
    def stop(self):
        self.speed.set(0)
        self.steer.set(0)

    def real_location(self,obj):
        i = 0
        for objecti in obj.name:
            if objecti == 'drivingVic':
                val = i
                break
            i += 1
        theta = euler_from_quaternion( numpy.array((obj.pose[val].orientation.x, obj.pose[val].orientation.y, obj.pose[val].orientation.z, obj.pose[val].orientation.w), dtype=numpy.float64))
        self.real_loc['x'] = int(obj.pose[val].position.x*100)/100.0
        self.real_loc['y'] = int(obj.pose[val].position.y*100)/100.0
        self.real_loc['theta'] = int(theta[2]*100)/100.0
        
    def publisher(self):
        self.publish_int8()
        self.publish_float64()

    def publish_int8(self):
        msg = Int8()
        #publish direction
        msg.data = self.direction.get()
        self._direction.publish(msg)

    def publish_float64(self):
        msg = Float64()
        #publish HB
        msg.data = self.hb.get()
        self._hand_brake.publish(msg)
        #publish Gas
        msg.data = self.speed.get()
        self._gas.publish(msg)
        msg.data = self.brake.get()
        self._brake.publish(msg)
        #publish Steering
        msg.data = self.steer.get()
        self._wheel.publish(msg)

ros_handler = ROS()
auto_flag = 0
wp = []
def keydown_handler(key):
    global auto_flag,label,ros_handler
    if key == simplegui.KEY_MAP['a']:
        ros_handler.direction.toggle()
    if key == simplegui.KEY_MAP['up']:
        ros_handler.speed.set(1)
    if key == 37:
		ros_handler.steer.set(1)
    if key == 39:
		ros_handler.steer.set(-1)
    if key == 40:	
		ros_handler.brake.set(1)
    if key == simplegui.KEY_MAP['space']:
        auto_flag = abs(auto_flag-1)
        if not auto_flag:
            label.set_text('Manual')
        else:
            label.set_text('Auto')

def draw(canvas):
    global wp
    i = 1
    for w in wp:
        wstr = '(%d,%d)'%(w[0],w[1])
        canvas.draw_text(wstr, (30,i*30),12,'Blue')
        i += 1

def keyup_handler(key):
    global gas, auto_flag,ros_handler
    if (key == simplegui.KEY_MAP['up']):
        ros_handler.speed.set(0)
    if key == 40:
		ros_handler.brake.set(0)
    if key == 37:
        ros_handler.steer.set(0)
    if key == 39:
        ros_handler.steer.set(0)
    if key == simplegui.KEY_MAP['space']:
        pass
        

def input_handler1(text_input):
    global wp,inp1
    num = 0
    flag = 0
    ok = False
    for c in text_input:
        
        if c.isdigit():
            ok = True
            num = num*10 + int(c)
        else:
            if ok == True:            
                flag += 1
        if flag == 1:
            num1 = num
            num = 0
            flag = 0
            ok = False
    num2 = num
    wp.append([num1,num2])
    inp1.set_text('')

def mouse_handler(position):
    global wp
    try:
        wp.pop(position[1]/30)
    except:
        pass

def publisher_handler():
    global ros_handler, auto_flag,wp
    if auto_flag:
        ok = True
        while(ok):
            if len(wp)==0:
                ros_handler.stop()
                ok = False
            else:
                d,t = calc_error(ros_handler.real_loc,wp[0])
                if d < 3:
                    WP = wp.pop(0)
                    wp.append(WP)
                else:
                    g,s = PID(d,t)
                    ros_handler.speed.set(g*3)
                    ros_handler.steer.set(s)
                    ok = False
    ros_handler.publisher()

frame = simplegui.create_frame('driver_gui',100,100)
frame.set_canvas_background('White')
label = frame.add_label('Manual')
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown_handler)
frame.set_keyup_handler(keyup_handler)
frame.set_mouseclick_handler(mouse_handler)
inp1 = frame.add_input('add WP', input_handler1, 50)
pub_timer = simplegui.create_timer(100, publisher_handler)
pub_timer.start()
frame.start()
pub_timer.stop()
#print inp.get_text()
for i in range(3):
	
	ros_handler.stop()
	rospy.sleep(0.1)
	ros_handler.publisher()
