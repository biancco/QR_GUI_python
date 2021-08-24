from tkinter import *

class Myframe(Frame):
    def __init__(self, master):
        img = PhotoImage(file='test.gif')
        lbl = Label(image=img)
        lbl.image = img  #img객체를 계속 살려두는 역할
        lbl.grid(row=0,column=0)

def main():
    root = Tk()
    root.title("이미지 보기")
    root.geometry('500x400+100+100')
    myframe = Myframe(root)
    root.mainloop()

if __name__ == '__main__':
    main()
