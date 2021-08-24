from tkinter import *
from tkinter.ttk import *

class Myframe(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("고객 입력")
        self.pack(fill=BOTH, expand=True) #사용되지 않은 공간을 모두 활용

        #name
        frame1 = Frame(self)
        