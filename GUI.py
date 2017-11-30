from tkinter  import *
from PIL import Image, ImageTk
import tkinter.ttk as ttk


class GUI(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self.pack(fill=BOTH, expand=1)

    def init_window(self):
        simButton = Button(self, text="Similar Scan", height=5, width=10)
        simButton.place(x=0, y=110)

        dupButton = Button(self, text="Duplicates", height=5, width=10)
        dupButton.place(x=0, y=195)

        listButton = Button(self, text="Whitelist", height=5, width=10)
        listButton.place(x=0, y=280)

        cusButton = Button(self, text="Custom Scans", height=5, width=10)
        cusButton.place(x=0, y=365)

        setButton = Button(self, text="Settings", height=3, width=10)
        setButton.place(x=0, y=450)

        scanButton = Button(self, text="Scan", font=("Sans"), bg="Blue",
                                                     fg="white", height=4, width=20)
        scanButton.place(x=500, y=350)

        dupLabel = Label(self, text="Duplicates:", font=("Sans", 40))
        dupLabel.place(x=100, y=250)

        load = Image.open('DDPS_logo128.png')
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)

        progressBar = ttk.Progressbar(self, length=600, orient='horizontal', mode='determinate')
        progressBar.place(x=150, y=150)



gui = Tk()
object = GUI(gui)
gui.title("Duplicate Detection and Prevention System")
gui.geometry("800x500")
gui.resizable(False, False)
gui.mainloop()
