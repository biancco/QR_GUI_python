#!/usr/bin/env python
import rospy
import cv2
import sys
from std_msgs.msg import String, Int32
from sensor_msgs.msg import Image
from PIL import ImageTk, Image


class Recognizer:

    def __init__(self):
        self.recognizer_pub = rospy.Publisher("/result",Image)
        self.get_image_data = getImageData()
        self.image_sub = rospy.Subscriber("/image_topic",Image,self.get_image_data.callback)

    def image_callback(self,msg):
        imageValiation(get_image_data)


def imageValidation(data):


class getImageData():
    def __init__(self):
        self.height = 720
        self.width = 1080
        self.encoding = 'bgr8'
        pass

    def callback(self,data_):


def main():
    rc = Recongnizer()
    rospy.init_node('recognizer_node', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")

    if __name__ == '__main__':
        main()
