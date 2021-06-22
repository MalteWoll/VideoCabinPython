# tkinter for GUI
from tkinter import *
#from tkinter import filedialog
#from tkinter import messagebox

# glob for finding files
#import glob

# subprocess and os for operating system operations
#import subprocess
#import os

# shutil for copying files between partitions
#from shutil import copyfile

# datetime and re for creating files and directories with dates and times
#from datetime import datetime

# for window positioning
windowWidth = 640
windowHeight = 1080
windowPositionX = 1920 - windowWidth
windowPositionY = 0

def introWindow():
    windowNew = Tk()
    #windowNew.geometry(str(windowWidth) + "x" + str(windowHeight) + "+" + str(windowPositionX) + "+" + str(windowPositionY))
    windowNew.title = "Instructions"

    windowNew.mainloop

introWindow()

# https://stackoverflow.com/questions/53541138/how-to-add-multiline-text-dynamically-in-tkinter-python