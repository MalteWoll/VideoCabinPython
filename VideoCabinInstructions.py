# tkinter for GUI
import tkinter as tk
from tkinter import Label
from tkinter import Button

# For loading images
from PIL import ImageTk, Image

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

# for window positioning, these need to be set to the appropriate resolution
desktopResolutionX = 1920
desktopResolutionY = 1080

# these parameters need to be set to set the window size we want
windowWidth = int(desktopResolutionX / 2.5)
windowHeight = desktopResolutionY

# these parameters need to be set to place the window where we want it to be
windowPositionX = 0 - windowWidth
windowPositionY = 0

# Path to images files
imageFilesDir = "C:/Users/malte/Dropbox/Studium/PAM3/guiImages"

# Image files
audioLevelImg = imageFilesDir + "/audioLevel.JPG"

# Some parameters for formatting text
labelWrapLength = windowWidth-100
paddingX = 20
paddingY = 20
textFontStyle = "Helvetica"
textFontSize = 20

textWelcomeMessage1 = "Welcome to the Video Cabin! Please follow the instructions to learn how to create your videos."
textWelcomeMessage2 = "Press the 'Continue' button to follow the instructions. If you are already familiar with the application, you can skip this tutorial by pressing the 'Skip' button."

textAudioInstructions1 = "We need to make sure your voice can be heard, so let's first calibrate the audio signal."
textAudioInstructions2 = "To do so, please speak in a volume as if you were recording, and stand where you would stand."
textAudioInstructions3 = "While speaking, please observe the audio gauge (??) on the bottom left side of this monitor. The audio level should be within the green area while you are speaking, as shown below."

textButtonContinue = "Continue"
textButtonSkip = "Skip"

# Window for reviewing the last clip recorded and to delete it, if needed
def fileControl(windowOld):
    if(windowOld is not None):
        windowOld.destroy()

# Instructions for audio calibration
def audioCalibration(windowOld):
    if(windowOld is not None):
        windowOld.destroy()
    
    windowNew = tk.Tk()
    windowNew.geometry(str(windowWidth) + "x" + str(windowHeight) + "+" + str(windowPositionX) + "+" + str(windowPositionY))
    windowNew.title = "Audio calibration"

    textFont = (textFontStyle,textFontSize)
    text_audio1 = Label(windowNew, text=textAudioInstructions1, font=textFont, wraplength=labelWrapLength )
    text_audio1.grid(row=0, padx=paddingX, pady=paddingY)
    text_audio2 = Label(windowNew, text=textAudioInstructions2, font=textFont, wraplength=labelWrapLength )
    text_audio2.grid(row=1, padx=paddingX, pady=paddingY)
    text_audio3 = Label(windowNew, text=textAudioInstructions3, font=textFont, wraplength=labelWrapLength )
    text_audio3.grid(row=2, padx=paddingX, pady=paddingY)

    img = Image.open(audioLevelImg)

    windowNew.mainloop()


# The first window the user is presented with
def introWindow(windowOld):
    if(windowOld is not None):
        windowOld.destroy()

    windowNew = tk.Tk()
    windowNew.geometry(str(windowWidth) + "x" + str(windowHeight) + "+" + str(windowPositionX) + "+" + str(windowPositionY))
    windowNew.title = "Instructions"

    textFont = (textFontStyle,textFontSize)

    # Welcome messages
    label_welcome1 = Label(windowNew, text=textWelcomeMessage1, font=textFont, wraplength=labelWrapLength )
    label_welcome1.grid(row=0, padx=paddingX, pady=50)
    label_welcome2 = Label(windowNew, text=textWelcomeMessage2, font=textFont, wraplength=labelWrapLength )
    label_welcome2.grid(row=1, padx=paddingX, pady=50)

    # Buttons
    button_continue = Button(windowNew, text=textButtonContinue, font=textFont, command= lambda: audioCalibration(windowNew))
    button_continue.grid(row=2, padx=paddingX, pady=10)
    button_skip = Button(windowNew, text=textButtonSkip, font=textFont, command= lambda: fileControl(windowNew))
    button_skip.grid(row=3, padx=paddingX, pady=10)

    windowNew.mainloop()

# Script starts here
introWindow(None)