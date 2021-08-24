from tkinter import *

class Myframe(Frame):
    def __init__(self, master):
        img = PhotoImage(file='test.jpg')
        lbl = Label(image=img)
        lbl.grid(row=0,column=0)

def main():
    root = Tk()
    root.title("이미지 보기")
    root.geometry()
