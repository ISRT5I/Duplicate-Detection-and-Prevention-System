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
        self.configure(background='gray45')

    def init_window(self):
        simButton = Button(self, text="Similar Scan", bg = "gray60", height=4, width=11)
        simButton.place(x=0, y=80)

        dupButton = Button(self, text="Duplicates", bg = "gray60", height=4, width=11)
        dupButton.place(x=0, y=150)

        realButton = Button(self, text="Real-Time", bg = "gray60", height=4, width=11)
        realButton.place(x=0, y=220)

        listButton = Button(self, text="Whitelist", bg = "gray60", height=4, width=11)
        listButton.place(x=0, y=290)

        cusButton = Button(self, text="Custom Scan(s)", bg = "gray60", height=4, width=11)
        cusButton.place(x=0, y=360)

        setButton = Button(self, text="Settings", bg = "gray45", height=4, width=11)
        setButton.place(x=0, y=430)

        scanButton = Button(self, text="Scan", font=("Calibri"), bg="Red2",
                                                     fg="white", height=4, width=20, command=Hash.scan)
        scanButton.place(x=545, y=375)

        dupLabel = Label(self, text="Duplicates:", font=("Calibri", 40), bg = "gray45")
        dupLabel.place(x=100, y=250)

        load = PIL.Image.open('DDPS_logo64.png')
        render = PIL.ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.place(x=5, y=5)
        img.configure(background='gray45')

        s = ttk.Style()
        s.theme_use('classic')
        s.configure("red.Horizontal.TProgressbar", foreground='red2', background='red2')
        progressBar = ttk.Progressbar(self, length=600, orient='horizontal', mode='indeterminate', style="red.Horizontal.TProgressbar", maximum=50)
        progressBar.place(x=150, y=125)

    def progress(state):
        s = ttk.Style()
        s.theme_use('classic')
        s.configure("red.Horizontal.TProgressbar", foreground='red2', background='red2')
        gui.progressBar = ttk.Progressbar(gui, length=600, orient='horizontal', mode='indeterminate', style="red.Horizontal.TProgressbar", maximum=50)
        gui.progressBar.place(x=150, y=125)
        if state == 1:
            gui.progressBar.start()
        else:
            gui.progressBar.stop()
        
class Hash:

    def findDup(parentFolder):
        dups = {}
        for dirs, subdirs, fileList in os.walk(parentFolder):
            dirName = dirs.replace("\\", "/")
            print('Scanning %s...' % dirName)
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
        dic = open(os.path.join('lists', "dictionary.txt"),"a+")
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
        wFolder = open(os.path.join('lists', "whitefolder.txt"),"a+")
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
        wFile = open(os.path.join('lists', "whitefile.txt"),"a+")
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
        wFolder = open(os.path.join('lists', "whitefolder.txt"),"a+")
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
        realFolder = open(os.path.join('lists', "realfolder.txt"),"r")
        folder = realFolder.read()
        print (folder)
        if folder != "":
            threading.Thread(target=Realtime.watch, args = (folder,)).start()
        else:
            print("Must set directory first")
        realFolder.close()
        
    def check():
        real = open(os.path.join('lists', "realtime.txt"),"r")
        realtime = real.readlines()
        print (realtime[0])
        if realtime[0] == "1":
            print ("realtime scan is set.")
            Realtime.start()
        else:
            print ("realtime scan not set.")
        real.close()
    
    def set():
        real = open(os.path.join('lists', "realtime.txt"),"w")
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
        real = open(os.path.join('lists', "realtime.txt"),"w")
        real.write("0")
        real.close()
        print ("Program must restart to disable realtime scan.")
        
#class Options:
#    def check():
#        nothing = 1
             


            
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
