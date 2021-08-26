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
        frame1.pack(fill=X)
        lblName = Label(frame1, text="성명",width=10) #Label은 텍스트,이미지칸
        lblName.pack(side=LEFT, padx=10, pady=10)
        entryName = Entry(frame1) #Entry는 쓰는칸
        entryName.pack(fill=X, padx=10, expand=True)

        #company
        frame2 = Frame(self)
        frame2.pack(fill=X)
        lblName = Label(frame2, text="회사",width=10)
        lblName.pack(side=LEFT, padx=10, pady=10)
        entryName = Entry(frame2)
        entryName.pack(fill=X, padx=10, expand=True)

        #figure

        

def main():
    root = Tk()
    root.geometry("600x550+100+100")
    app = Myframe(root)
    root.mainloop()

if __name__ == '__main__':
    main()