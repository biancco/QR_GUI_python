#!/usr/bin/env python
import sys
import rospy
import cv2
from std_msgs.msg import String, Int32
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from PIL import ImageTk, Image

class imageLoader:

    def __init__(self):
        self.image_pub = rospy.Publisher("/image_topic",Image)
        self.bridge = CvBridge()
        self.start_sub = rospy.Subscriber("/start_sign",Int32,self.start_callback)
        self.recognizer_sub = rospy.Subscriber("/result",Int32,self.recognizer_callback)
        self.show_camera = 1;

    def start_callback(self,msg): 





        
        while not rospy.is_shutdown():
            try:
                self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
            except CvBridgeError as e:
                print(e)

    def recognizer_callback(self,data):
        if(data == 0):
            show_camera = 0;
        else:
            show_camera = 1;


if __name__ == '__main__':
    il = imageLoader()
    rospy.spin()
