#!/usr/bin/env python
import rospy
import cv2
import sys
import pyzbar.pyzbar as pyzbar
from std_msgs.msg import Int32
from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image


class waitingScreen:

    def __init__(self):
        self.service_pub = rospy.Publisher("/start_sign",Int32)
        self.complete_sub = rospy.Subscriber("/end_sign",Int32,self.reboot_callback)

    def reboot_callback(self,msg):


def main(args):
    sc = waitingScreen()
    rospy.init_node('waiting_screen', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()

    if __name__ == '__main__':
        main(sys.argv)
