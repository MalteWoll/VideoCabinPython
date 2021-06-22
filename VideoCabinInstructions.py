# tkinter for GUI
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

# glob for finding files
import glob

# subprocess and os for operating system operations
import subprocess
import os

# shutil for copying files between partitions
from shutil import copyfile

# datetime and re for creating files and directories with dates and times
from datetime import datetime

# for screen information
import screeninfo

# for window positioning
desktopResolutionX = 1920
desktopResolutionY = 1080

windowWidth = int(desktopResolutionX / 2.5)
windowHeight = desktopResolutionY

windowPositionX = 0 - windowWidth
windowPositionY = 0

def introWindow():
    windowNew = tk.Tk()
    windowNew.geometry(str(windowWidth) + "x" + str(windowHeight) + "+" + str(windowPositionX) + "+" + str(windowPositionY))
    windowNew.title = "Instructions"

    windowNew.mainloop()

print(screeninfo.get_monitors())
introWindow()

# https://stackoverflow.com/questions/53541138/how-to-add-multiline-text-dynamically-in-tkinter-python