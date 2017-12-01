import tkinter as tk
import PIL.Image, PIL.ImageTk
from tkinter import filedialog, messagebox, ttk
from tkinter import *
import os, sys, time ,hashlib ,threading

#class Scroll(object):
#
#    def __init__(self):
#        self.root = tk.Tk()
#    # create a Text widget with a Scrollbar attached
#        self.txt = ScrolledText(self.root, undo=True)
#        self.txt['font'] = ('consolas', '12')
#        self.txt.pack(expand=True, fill='both')

class GUI(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self.pack(fill=BOTH, expand=1)
        self.configure(background=Theme.backGround())

    def init_window(self):
        simButton = Button(self, text="Similar Scan", bg = Theme.sideButton(), fg=Theme.font(), height=4, width=11)
        simButton.place(x=0, y=80)
        dupButton = Button(self, text="Duplicates", bg = Theme.sideButton(), fg=Theme.font(), height=4, width=11)
        dupButton.place(x=0, y=150)
        realButton = Button(self, text="Real-Time", bg = Theme.sideButton(), fg=Theme.font(), height=4, width=11)
        realButton.place(x=0, y=220)
        listButton = Button(self, text="Whitelist", bg = Theme.sideButton(), fg=Theme.font(), height=4, width=11)
        listButton.place(x=0, y=290)
        cusButton = Button(self, text="Custom Scan(s)", bg =Theme.sideButton(), fg=Theme.font(), height=4, width=11)
        cusButton.place(x=0, y=360)
        setButton = Button(self, text="Themes", bg = Theme.sideButton(), fg=Theme.font(), height=4, width=11, command=Theme.open)
        setButton.place(x=0, y=430)     
        scanButton = Button(self, text="Scan", font=("Calibri"), bg=Theme.scanButton(), fg=Theme.font(), height=4, width=20, command=Hash.scan)
        scanButton.place(x=545, y=375)
        dupLabel = Label(self, text="Duplicates:", font=("Calibri", 40), bg = Theme.backGround())
        dupLabel.place(x=100, y=250)
        load = PIL.Image.open('assets\\DDPS_logo64.png')
        render = PIL.ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.place(x=5, y=5)
        img.configure(background=Theme.backGround())
        s = ttk.Style()
        s.theme_use('classic')
        s.configure("Horizontal.TProgressbar", foreground=Theme.scanButton(), background=Theme.scanButton())
        progressBar = ttk.Progressbar(self, length=600, orient='horizontal', mode='indeterminate', style="Horizontal.TProgressbar", maximum=50)
        progressBar.place(x=150, y=125) 
        #not 100% sure how this works but I am assuming i have to do an initialization of sorts for the label here
        curPathLabel = Label(self, text = " ", font = ("Calibri"), bg = Theme.backGround())
        curPathLabel.place(x = 150, y = 150)

    def progress(state):
        s = ttk.Style()
        s.theme_use('classic')
        s.configure("Horizontal.TProgressbar", foreground=Theme.scanButton(), background=Theme.scanButton())
        gui.progressBar = ttk.Progressbar(gui, length=600, orient='horizontal', mode='indeterminate', style="Horizontal.TProgressbar", maximum=50)
        gui.progressBar.place(x=150, y=125)
        if state == 1:
            gui.progressBar.start()
        else:
            gui.progressBar.stop()
            gui.curPathLabel = Label(gui, text = " ", font = ("Calibri"), bg = Theme.backGround())
            gui.curPathLabel.place(x = 150, y = 150, width = 600, height = 100)
    
    #function to take in a directory and print and update the directory below the progress bar; calling curPath(x) wherever there were print functions with directories
    def curPath(path):
        gui.curPathLabel = Label(gui, text = "Scanning " + path + "...", font = ("Calibri"), bg = Theme.backGround(), wraplength=600, justify = "left")
        gui.curPathLabel.place(x = 150, y = 150, width = 600)
        gui.curPathLabel.update()
        
        
class Hash:

    def findDup(parentFolder):
        dups = {}
        for dirs, subdirs, fileList in os.walk(parentFolder):
            dirName = dirs.replace("\\", "/")
            print('Scanning %s...' % dirName)
            GUI.curPath(dirName)
            for filename in fileList:
                path = dirName + "/" + filename
                file_hash = Hash.hashfile(path)
                if file_hash in dups:
                    dups[file_hash].append(path)
                else:
                    dups[file_hash] = [path]
        return dups
  
    def memDup(parentFolder):
        dups = {}
        dic = open("assets\\lists\\dictionary.txt","a+")
        dic.seek(0)
        dicts = [line.split("|") for line in dic]
        wFiles = open(os.path.join('lists', "whitefile.txt"),"a+")
        wFiles.seek(0)
        whiteFiles = [x.strip() for x in wFiles.readlines()]
        wFolder = open(os.path.join('lists', "whitefolder.txt"),"a+")
        wFolder.seek(0)
        whiteFolder = [x.strip() for x in wFolder.readlines()]
        for dirs, subdirs, fileList in os.walk(parentFolder):
            dirName = dirs.replace("\\", "/")
            if dirName not in whiteFolder:
                print('Scanning %s...' % dirName)
                GUI.curPath(dirName)
                for filename in fileList:
                    path = dirName + "/" + filename
                    if path not in whiteFiles:
                        file_hash = Hash.hashfile(path)
                        if file_hash in dups:
                            dups[file_hash].append(path)
                        elif any(file_hash in sublist for sublist in dicts):
                            dups[file_hash] = [path]
                        else:
                            dic.write(file_hash + "|" + path + "\n")
                            dicts.append([file_hash , path])
                            dups[file_hash] = [path]
        dic.close()
        wFiles.close()
        wFolder.close()
        return dups

    def joinDicts(dict1, dict2):
        for key in dict2.keys():
            if key in dict1:
                dict1[key] = dict1[key] + dict2[key]
            else:
                dict1[key] = dict2[key]
 
 
    def hashfile(path, blocksize = 65536):
        afile = open(path, 'rb')
        hasher = hashlib.md5()
        buf = afile.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(blocksize)
        afile.close()
        return hasher.hexdigest()
 
 
    def printResults(dict1):
        results = list(filter(lambda x: len(x) > 1, dict1.values()))
        if len(results) > 0:
            messagebox.showinfo("DDPS", "Duplicates Found!")
            print('The following files are identical. The name could differ, but the content is identical')
            print('___________________')
            for result in results:
                for subresult in result:
                    print('\t\t%s' % subresult)
                print('___________________')
 
        else:
            messagebox.showerror("DDPS", "No duplicate files found.")
        GUI.progress(0)
    
    def memScan():
        GUI.progress(1)
        folder = filedialog.askdirectory()
        GUI.progress(1)
        wFolder = open("assets\\lists\\whitefolder.txt","a+")
        wFolder.seek(0)
        whiteFolder = [x.strip() for x in wFolder.readlines()]
        wFolder.close()
        folders = [folder]
        for i in folders:
            if i not in whiteFolder:
                if os.path.exists(i):
                    Hash.joinDicts(dups, Hash.memDup(i))
        Hash.printResults(dups)

    def scan():
        GUI.progress(1)
        folder = filedialog.askdirectory()
        dups = {}
        folders = [folder]
        for i in folders:
            if os.path.exists(i):
                Hash.joinDicts(dups, Hash.findDup(i))
        Hash.printResults(dups)

class Whitelist:

    def addFile():
        wFile = open("assets\\lists\\whitefile.txt","a+")
        wFile.seek(0)
        whiteList = [x.strip() for x in wFile.readlines()]
        wFiles = filedialog.askopenfilenames(title='Choose file(s)')
        whiteFiles = list(wFiles)
        if not whiteFiles:
                print ("No files whitelisted.")
        for whiteFile in whiteFiles:
            if whiteFile in whiteList:
                print (whiteFile + " is already whitelisted!")
            else:
                wFile.write(whiteFile + "\n")
                print (whiteFile + " has been whitelisted.")
        wFile.close()        
            
    def addFolder():
        wFolder = open("assets\\lists\\whitefolder.txt","a+")
        wFolder.seek(0)
        whiteList = [x.strip() for x in wFolder.readlines()]
        whiteFolder = filedialog.askdirectory()
        if whiteFolder == "":
            print ("No folders whitelisted.")
        elif whiteFolder in whiteList:
            print (whiteFolder + " is already whitelisted!")
        else:
            wFolder.write(whiteFolder + "\n")
            print (whiteFolder + " has been whitelisted.")
        wFolder.close()

class Realtime:

    def start():
        realFolder = open("assets\\lists\\realfolder.txt","r")
        folder = realFolder.read()
        print (folder)
        if folder != "":
            threading.Thread(target=Realtime.watch, args = (folder,)).start()
        else:
            print("Must set directory first")
        realFolder.close()
        
    def check():
        real = open("assets\\lists\\realtime.txt", "r")
        realtime = real.readlines()
        print (realtime[0])
        if realtime[0] == "1":
            print ("realtime scan is set.")
            Realtime.start()
        else:
            print ("realtime scan not set.")
        real.close()
    
    def set():
        real = open("assets\\lists\\realtime.txt","w")
        real.write("1")
        Realtime.start()
        real.close()

    def watch(folders):
        path_to_watch = folders
        before = dict ([(f, None) for f in os.listdir (path_to_watch)])
        while 1:
          time.sleep (10)
          after = dict ([(f, None) for f in os.listdir (path_to_watch)])
          added = [f for f in after if not f in before]
          removed = [f for f in before if not f in after]
          if added:
              print ("Added: " , ", ".join (added))
              
          if removed:
              print ("Removed: ", ", ".join (removed))
          before = after

    def stop():
        real = open("assets\\lists\\realtime.txt","w")
        real.write("0")
        real.close()
        print ("Program must restart to disable realtime scan.")
        
class Theme():

    def open():
        master = tk.Tk()
        master.geometry("240x142")
        master.resizable(False, False)
        v = IntVar()
        theme = open("assets\\lists\\theme.txt","r")
        themeSet = theme.readlines()
        theme.close
        v.set(themeSet)
        theme1 = Button(master, text="Default", height=4, width=10, command = lambda: Theme.setTheme("1"))
        theme1.grid(row=0, column=0)
        theme2 = Button(master, text="Light", height=4, width=10, command = lambda: Theme.setTheme("2"))
        theme2.grid(row=0, column=1)
        theme3 = Button(master, text="Dark", height=4, width=10,command = lambda: Theme.setTheme("3"))
        theme3.grid(row=1, column=0)
        theme4 = Button(master, text="DarkRed", height=4, width=10, command = lambda: Theme.setTheme("4"))
        theme4.grid(row=1, column=1)
        theme5 = Button(master, text="Contrast", height=4, width=10, command = lambda: Theme.setTheme("5"))
        theme5.grid(row=0, column=2)
        b1 = Button(master, text='ok', bg="gray97", command = master.destroy)
        b1.place(relx=0, x=188, y=95, anchor=NW)

    def setTheme(choice):
        theme = open("assets\\lists\\theme.txt","w")
        theme.write(choice)
        print(choice)
        theme.close()
        
    def sideButton():
        theme = open("assets\\lists\\theme.txt","r")
        themeSet = theme.read()
        print (themeSet)
        if themeSet == "1":
            return "gray80"
        if themeSet == '2':
            return "white"
        if themeSet == "3":
            return "gray40"
        if themeSet == "4":
            return "gray40"
        if themeSet == "5":
            return "black"
        theme.close()

    def scanButton():
        theme = open("assets\\lists\\theme.txt","r")
        themeSet = theme.read()
        if themeSet == "1":
            return "blue"
        if themeSet == '2':
            return "cyan"
        if themeSet == "3":
            return "medium blue"
        if themeSet == "4":
            return "red2"
        if themeSet == "5":
            return "black"
        theme.close()

    def backGround():
        theme = open("assets\\lists\\theme.txt","r")
        themeSet = theme.read()
        if themeSet == "1":
            return "gray90"
        if themeSet == '2':
            return "white"
        if themeSet == "3":
            return "gray45"
        if themeSet == "4":
            return "gray45"
        if themeSet == "5":
            return "white"
        theme.close()

    def font():
        theme = open("assets\\lists\\theme.txt","r")
        themeSet = theme.read()
        if themeSet < "3":
            return "black"
        else:
            return "white"
        theme.close()
            
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    Realtime.check()
    gui = tk.Toplevel()
    object = GUI(gui)
    gui.title("Duplicate Detection and Prevention System")
    gui.geometry("800x500")
    gui.resizable(False, False)
    gui.mainloop()