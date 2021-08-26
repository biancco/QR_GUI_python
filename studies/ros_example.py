#!/usr/bin/env python
# license removed for brevity
# edit example

import rospy
import time
import serial
import math
import os
from std_msgs.msg import String
from std_msgs.msg import Int32MultiArray
from core_msgs.msg import VehicleState
from core_msgs.msg import Control

alive = 0
enc = []
global s

sudoPassword = 'snuzero123'
command = 'chmod 777 /dev/ttyUSB2'
p= os.system('echo %s|sudo -S %s' % (sudoPassword, command))


def init():

    pub = rospy.Publisher('/vehicle_state', VehicleState, queue_size=10)
    #pub_s = rospy.Publisher('s_distance_driven', Float32, queue_size=10) #publish s to make (x, y, s, mission state) sets in global coordinate
    
    control_data = getControlData()
    rospy.Subscriber("/input_control", Control, control_data.callback)
    rospy.init_node('serial_com', anonymous=True)
    rate = rospy.Rate(20)
    msg = VehicleState() #define msg - current platform state

    while not rospy.is_shutdown():
        with serial.Serial(port='/dev/ttyUSB2',
                           baudrate=115200 ,
                           parity=serial.PARITY_NONE,
                           stopbits=serial.STOPBITS_ONE,
                           bytesize=serial.EIGHTBITS,
                           timeout=1) as ser:

            while not rospy.is_shutdown():
                msg=MsgUpdate(msg,ser)
                #rospy.loginfo(msg)
                pub.publish(msg)
                sendSerial(ser,control_data)
                rate.sleep()

#PCU signal: 5=E-STOP 6=GEAR(0=D,1=N,2=R) 7~8=SPEED(0~200) by m/s 9~10=STEER*71 11=BRAKE(1~200)
#           12~15=Encoder[same as speed] 16=ALIVE

def MsgUpdate(msg,ser): #message about current sate (serial data : platform->upper)

    raw_data = ser.read(18)
    pub_serial_data = rospy.Publisher('/serial_data', String, queue_size=10)
    pub_serial_data.publish(raw_data)
    data = []
    #file.write("raw_data[i]\traw_data[i].encode('hex')\tint(raw_data[i].encode('hex'),16\thex(int(raw_data[i].encode('hex'),16))\n")
    for i in range(0,18):
	#file.write(raw_data[i])
	#file.write("\t")
	#file.write(raw_data[i].encode('hex'))
	#file.write("\t")
	#file.write("%d" % int(raw_data[i].encode('hex'),16))
	#file.write("\t")
	#file.write(hex(int(raw_data[i].encode('hex'),16)))
	#file.write("\n")
        data.append(hex(int(raw_data[i].encode('hex'),16)))
    is_auto = int(data[3],16)
    estop = int(data[4],16)
    if(estop == 16):
        estop = 1
    gear = int(data[5],16)


   #Steer calculation # degree
    if(len(data[9])>=4):
        steer = int(data[9], 16) * 256 + int(data[8], 16) + 1 - pow(2,15)
        steer = float(steer)/71 -462
    else:
        steer = int(data[9], 16) * 256 + int(data[8], 16)
        steer = float(steer)/71

    brake = int(data[10], 16)

    global alive
    alive = int(data[15], 16)

   #encoder caculation

    encoder = int(data[14], 16) * pow(256,3) + int(data[13], 16) * pow(256,2) + int(data[12], 16) * pow(256,1) + int(data[11], 16)
    if encoder > pow(256,4) * 0.75: # in case encoder < 0
        encoder = encoder - pow(256,4)

    #s sould be caculated!
    
    #Speed caculation : m/s
    global enc
    radius = 0.266 # meter scale
    distance = 2 * math.pi * radius # distance per rotation
    enc.append(encoder)
    # 10 data time-interval is 0.510sec
    # encoder pulse per rotation = 100
    if(len(enc)>=11):
        speed = ((enc[10] - enc[0]) /0.51/100.0) * float(distance) # m/s
        enc.pop(0)
    else:
        speed = 0 #initial speed : 0 m/s

    if not isValidValue(speed, steer): return msg #in case of invalid speed or steer -> no update of msg

    #setting message variables
    msg.is_auto = is_auto
    msg.estop = estop
    msg.gear = gear
    msg.brake = brake
    msg.speed = round(speed,3)
    rospy.loginfo("car speed :" + str(msg.speed))
    msg.steer = round(steer,3) #left is positive
    msg.encoder = encoder
    msg.alive = alive
    ##msg.header.stamp = rospy.Time.now()
    return msg

def sendSerial(ser,data): #upper->platform
    is_auto=data.is_auto
    estop=data.estop
    gear=data.gear    
    speed=data.speed*36 # km/h *10
    steer1=data.steer1
    steer2=data.steer2
    brake=data.brake
    global alive
    #rospy.loginfo("is_auto " + str(is_auto))
    #rospy.loginfo("estop " + str(estop))
    #rospy.loginfo("gear " + str(gear))
    #rospy.loginfo("speed " + str(speed))
    #rospy.loginfo("steer1 " + str(steer1))
    #rospy.loginfo("steer2 " + str(steer2))
    #rospy.loginfo("brake " + str(brake))
    #rospy.loginfo("alive " + str(alive))
    data_array = bytearray([83, 84, 88, is_auto, estop, gear, 0, speed, steer1, steer2, brake, alive, 13, 10])
    ser.write(data_array)

def isValidValue(speed, steer): #speed : m/s, steer : degree
    if abs(speed) <= 6 and speed>=0 and abs(steer) <= 28:
        return True
    else:
        return False

class getControlData(): #input:speed(m/s), steer(degree) -> output: speed(km/h * 10), steer(degree*71, steer1:first byte, steer2:second byte)
    def __init__(self):
        self.is_auto = 1
        self.estop = 0
        self.gear = 0
        self.speed = 0
        self.steer1 = 0
        self.steer2 = 0
        self.brake=200
        pass

    def callback(self,data_): #serial data update (upper->platform)

        print("callback")
        self.is_auto = data_.is_auto
        
        self.estop = data_.estop
        self.gear = data_.gear
        self.speed = int(float(data_.speed))

        # rad to degree
    	steer_degree = data_.steer
        if steer_degree >=0:
            steer = int(float(steer_degree)*71)
            steer_low = steer%256
            steer_high = (steer-steer_low)/256
        else:
            steer = pow(2,15) + int(steer_degree*71)
            steer_low = steer%256
            steer_high = (steer-steer_low)/256 + pow(2,7)
	    if (steer_high >= 256):
	        steer_high = 255
	    if (steer_low >= 256):
	        steer_low = 255        

	    self.steer1 = steer_high
        self.steer2 = steer_low

        self.brake = data_.brake



if __name__ == '__main__':
    try:
        #file = open("/home/snuzero/catkin_ws/src/serial_communicator/data.txt", 'w')
        init()
	#file.close()
    except rospy.ROSInterruptException:
        pass