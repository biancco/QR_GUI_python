#!/usr/bin/env python

import rospy
import cv2
import os
import pyzbar.pyzbar as pyzbar

from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image

global cap
data_list = []
used_codes = []


def init():
    def __init__(self, master, cap):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("Spin")
        self.pack(fill=BOTH, expand=True) #사용되지 않은 공간을 모두 활용

        #text
        frame1 = Frame(self)
        frame1.pack(fill=X)
        lblName = Label(frame1, text="Please show QR code",width=100) #Label은 텍스트,이미지칸
        lblName.config(anchor=CENTER)
        lblName.pack(ipady=40)
        img = PhotoImage(file='test.gif')
        lblqr = Label(image=img)
        lblqr.image = img
        lblqr.pack(side=TOP, ipady=50)



def main():
    root = Tk()
    root.geometry("600x550+100+100")
    cap = cv2.VideoCapture(0)
    app = Myframe(root, cap)
    root.mainloop()
    key = cv2.waitKey(1)
    if key == 27:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    try:
        init()
    except rospy.ROSInterruptException:
        pass