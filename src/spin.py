from tkinter import *
from tkinter.ttk import *
import cv2
import os
from PIL import ImageTk, Image
import pyzbar.pyzbar as pyzbar

global data_list
global used_codes
global cap
data_list = []
used_codes = []

class Myframe(Frame):
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

        
        frame2 = Frame(self)
        frame2.pack(fill=X)
        frame = cap.read()
        scene = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(video=scene)
        lblv = Label()
        lblv.imgtk = imgtk
        lblv.configure(image=imgtk)
        lblv.pack()

        

    



'''
   #qr feedback (optional)
        frame2 = Frame(self)
        frame2.pack(fill=X)
        img = PhotoImage(file='test.gif')
        lblqr = Label(image=img)
        lblqr.image = img
        #lblqr.config(anchor=)
        lblqr.pack()


class Reader():
    cap = cv2.VideoCapture(0)

    for i in data_list:
        used_codes.append(i.rsplit('/n'))

    while True:
        success, frame = cap.read()

        if success:
            for code in pyzbar.decode(frame):
                cv2.imwrite('grbarcode_image.png',frame)
                my_code = code.data.decode('utf-8')
                if my_code not in used_codes:
                    print("인식 성공 : ",my_code)
                    used_codes.append(my_code)

                    f2 = open("grbarcode_data.txt", "a", encoding="utf8")
                    f2.write(my_code+'\n')
                    f2.close()

                else:
                    print("이미 인식된 코드입니다.")


            #cv2.imshow('cam',frame)

            key = cv2.waitKey(1)
            if key == 27:
                break

    cap.release()
    cv2.destroyAllWindows()
'''
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
    main()