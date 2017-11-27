from tkinter import *
from tkinter import filedialog, messagebox


def get_directories():
    if len(dirs) < 5:
        folder = filedialog.askdirectory()
        if folder != "":       
            dirs.append(folder)
            label = Label(addFolders, text= folder)
            #this creates a new label to the GUI
            size = len(dirs)
            label.place(relx=0, x=35, y=27+((size-1)*18), anchor=NW)
    else:
        messagebox.showwarning("DDPS", "Too many directories! Cannot add any more.")
    return dirs

def done():
    addFolders.destroy()

addFolders = Tk()
addFolders.geometry('340x180')
addFolders.resizable(False, False)
addFolders.title("DDPS")
addFolders.grid_rowconfigure(0, weight = 1)
addFolders.grid_columnconfigure(0, weight = 1)
dirs = []
selected = Label(addFolders, text = "Selected Directories")
selected.place(relx=0, x=0, y=0, anchor=NW)
b1 = Button(addFolders, text='Add Directories...', command = get_directories)
b1.place(relx=0, x=190, y=150, anchor=NW)
b2 = Button(addFolders, text='Done', command = done)
b2.place(relx=0, x=295, y=150, anchor=NW)
addFolders.mainloop()
print (dirs)
