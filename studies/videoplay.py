from tkinter import *
from tkinter.ttk import *
import cv2 as cv
import os
from PIL import ImageTk, Image
import pyzbar.pyzbar as pyzbar

cap = cv.VideoCapture(0)

def video_play():
    ret, frame = cap.read() # 프레임이 올바르게 읽히면 ret은 True
    if not ret:
        cap.release() # 작업 완료 후 해제
        return
    frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    img = Image.fromarray(frame) # Image 객체로 변환
    imgtk = ImageTk.PhotoImage(image=img) # ImageTk 객체로 변환
    # OpenCV 동영상
    lbl1 = Label()
    lbl1.imgtk = imgtk
    lbl1.configure(image=imgtk)
    lbl1.after(10, video_play)

video_play()
win.mainloop() #GUI 시작