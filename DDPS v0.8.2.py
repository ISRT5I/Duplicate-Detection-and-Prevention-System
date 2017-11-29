import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter import *
import os, sys, time
import hashlib

class Scroll(object):

#    def __init__(self):
#        self.root = tk.Tk()
#    # create a Text widget with a Scrollbar attached
#        self.txt = ScrolledText(self.root, undo=True)
#        self.txt['font'] = ('consolas', '12')
#        self.txt.pack(expand=True, fill='both')

#class GUI:
#
#    def __init__(self, master):
#       frame = Frame(master)
#       frame.pack()
#       self.menuButton = Button(frame, text="Menu", height=5, width=10)
#       self.menuButton.grid(row=0, sticky=W)
#       self.fileButton = Button(frame, text="Files", height=5, width=10)
#       self.fileButton.grid(row=1, sticky=W)
#       self.dupButton = Button(frame, text="Duplicates", height=5, width=10)
#       self.dupButton.grid(row=2, sticky=W)
#       self.setButton = Button(frame, text="Settings", height=5, width=10)
#       self.setButton.grid(row=3, sticky=W)
#       self.scanButton = Button(frame, text="Scan", bg="blue", fg="white", height=3,width=15)
#       self.scanButton.grid(row=3, column=5, sticky=E)
#       self.dupLabel = Label(frame, text="Duplicates: ")
#       self.dupLabel.grid(row=2, column=3, sticky=W)
       
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
    
    def memScan():
        folder = filedialog.askdirectory()
        #progress = tk.Tk()
        #pb = ttk.Progressbar(progress, orient="horizontal", length=200, mode="indeterminate")
        #pb.pack()
        #pb.start()
        dups = {}
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
        folder = filedialog.askdirectory()
        #progress = tk.Tk()
        #pb = ttk.Progressbar(progress, orient="horizontal", length=200, mode="indeterminate")
        #pb.pack()
        #pb.start()
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

#class Realtime:
#    
#    def watchPath():
#       insert = "here"
#
#    def realTimeWatch():
#        insert = "here"

#class Options:
#    def check():
#        nothing = 1
        
            
class Main:       
    def main():
        result = messagebox.askyesno("DDPS","Would you like to perform another scan?")
        if result == True:
            Hash.memScan()
        else:
            sys.exit()
        Main.main()
            
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    result = messagebox.askyesno("DDPS","Would you like to perform a scan?")
    if result == True:
        Hash.memScan()
    else:
        sys.exit()
    Main.main()

