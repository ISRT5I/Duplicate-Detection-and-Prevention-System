from tkinter  import *


class GUI:

    def __init__(self, master):
       frame = Frame(master)
       frame.pack()
       self.menuButton = Button(frame, text="Similar Scan", height=5, width=10)
       self.menuButton.grid(row=0, sticky=W)

       self.fileButton = Button(frame, text="Duplicates", height=5, width=10)
       self.fileButton.grid(row=1, sticky=W)

       self.dupButton = Button(frame, text="Whitelist", height=5, width=10)
       self.dupButton.grid(row=2, sticky=W)

       self.setButton = Button(frame, text="Custom Scans", height=5, width=10)
       self.setButton.grid(row=3, sticky=W)

       self.setButton = Button(frame, text="Settings", height=5, width=10)
       self.setButton.grid(row=4, sticky=W)

       self.scanButton = Button(frame, text="Scan", bg="blue", fg="white", height=3,
                                width=15)
       self.scanButton.grid(row=4, column=5, sticky=E)

       self.dupLabel = Label(frame, text="Duplicates: ")
       self.dupLabel.grid(row=2, column=3, sticky=W)


root = Tk()
object = GUI(root)
root.title("Duplicate Detection and Prevention System")
root.geometry("880x580")
root.mainloop()
