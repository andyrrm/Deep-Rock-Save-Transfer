from functools import wraps
from tkinter import *
from tkinter import messagebox, filedialog
import shutil
import os
import ntpath
from datetime import date
import webbrowser
import sys

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#UI window.
window = Tk()

window.title("DRST")

window.geometry('220x300')
window.resizable(width=False,height=False)

logo = PhotoImage(file=resource_path('./savetransferlogo_mini.png'))

logolabel = Label(window, image=logo).pack()

def callback():
    webbrowser.open_new("https://github.com/andyrrm/Deep-Rock-Save-Transfer#readme")

#Function that makes new backups and does the actual transfer.
def TransferTool(saveX, saveY, destY, backups):
    #Makes a new backup folder
    backupnum = 0
    backupchecker = backups + "/New Backup " + str(date.today())
    while os.path.exists(backupchecker):
        backupnum += 1
        backupchecker = backups + "/New Backup " + str(date.today()) + " " + str(backupnum)
    os.mkdir(backupchecker)
    basenameX = ntpath.basename(saveX)
    basenameY = ntpath.basename(saveY)
    renamepath = destY + "/" + basenameX
    #Copies/moves original files to backup folder
    shutil.copy(saveX, backupchecker)
    shutil.move(saveY, backupchecker)
    #Moves the save to the other save folder
    shutil.copy(saveX, destY)
    os.rename(renamepath, saveY)

#Function for setting up initial folder directories. 
def SetupClick():
    xboxsetuppath = filedialog.askdirectory(title="Select the folder containing your Xbox save")
    steamsetuppath = filedialog.askdirectory(title="Select the folder containing your Steam save")
    backupsetuppath = filedialog.askdirectory(title="Create or select a backup folder")
    settings = open(resource_path("settings.txt"), "w")
    settings.write(xboxsetuppath + "\n" + steamsetuppath + "\n" + backupsetuppath)

#Function for the Xbox to Steam button.
def XboxClick():
    pathfinder = open(resource_path("settings.txt"), "r")
    xboxsavepath = pathfinder.readline().strip()
    steamsavepath = pathfinder.readline().strip()
    backuppath = pathfinder.readline().strip()
    pathfinder.close()
    xboxsavefile = filedialog.askopenfilename(title="Select the Xbox save", initialdir=xboxsavepath)
    steamsavefile = filedialog.askopenfilename(title="Select the Steam save", initialdir=steamsavepath)
    TransferTool(xboxsavefile, steamsavefile, steamsavepath, backuppath)
    messagebox.showinfo("Transfer complete", "Rock and stone!")
    
#Function for the Steam to Xbox button.
def SteamClick():
    pathfinder = open(resource_path("settings.txt"), "r")
    xboxsavepath = pathfinder.readline().strip()
    steamsavepath = pathfinder.readline().strip()
    backuppath = pathfinder.readline().strip()
    pathfinder.close()
    steamsavefile = filedialog.askopenfilename(title="Select the Steam save", initialdir=steamsavepath)
    xboxsavefile = filedialog.askopenfilename(title="Select the Xbox save", initialdir=xboxsavepath)
    TransferTool(steamsavefile, xboxsavefile, xboxsavepath, backuppath)
    extenremover = os.path.splitext(xboxsavefile)[0]
    os.rename(xboxsavefile, extenremover)
    messagebox.showinfo("Transfer complete", "Rock and stone!")

#UI buttons.
setup = Button(window, text="First Time Setup", command=SetupClick).pack(pady=10)
xboxtransfer = Button(window, text="Transfer Xbox Save to Steam", command=XboxClick).pack(pady=10)
steamtransfer = Button(window, text="Transfer Steam Save to Xbox", command=SteamClick).pack(pady=10)
howto = Button(window, text="How To Use", command=callback).pack(pady=10)

window.mainloop()