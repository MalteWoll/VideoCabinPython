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

# counter variable for controlling the order in which instructional windows are opened up
orderControlCounter = 0

# Path to video files
videoFileDir = "D:/obs_scripts/python/videoSource"

# Path to images files
imageFilesDir = "C:/Users/malte/Dropbox/Studium/PAM3/guiImages"

# Path to the .exe of the video player to be used
videoPlayerDir = "D:/Program Files/VideoLAN/VLC/vlc.exe"

# Image files
audioLevelImg = imageFilesDir + "/audioLevel.JPG"
audioKnob = imageFilesDir + "/audioPlaceholder.jpg"
hdmiCable = imageFilesDir + "/hdmiCable.jpg"

# Some parameters for formatting text
labelWrapLength = windowWidth-100
paddingX = 10
paddingY = 10
textFontStyle = "Helvetica"
textFontSize = 20
textFontSizeSmaller = 16

textWelcomeMessage1 = "Welcome to the Video Cabin! Please follow the instructions to learn how to create your videos."
textWelcomeMessage2 = "Press the 'Continue' button to follow the instructions. If you are already familiar with the application, you can skip this tutorial by pressing the 'Skip' button."

textAudioInstructions1 = "We need to make sure your voice can be heard, so let's first calibrate the audio signal."
textAudioInstructions2 = "To do so, please speak in a volume as if you were recording, and stand where you would stand."
textAudioInstructions3 = "While speaking, please observe the audio gauge (??) on the bottom left side of this monitor. The audio level should be within the green area while you are speaking, roughly in the middle of the bar, as shown below."
textAudioInstructions4 = "If the audio level is green, great! You can continue. If not, look at the rotary knob on the device in front of you, which is pictured below."
textAudioInstructions5 = "If your recorded audio was too low (the bar was too far on the left side), slightly turn the know to the right, and try speaking again. If it was too high (the bar was in the yellow or red), slightly turn the knob to the left, and try speaking again."

textHardwareSetup1 = "To use the presentation from your laptop, please place the laptop in the area below the camera in front of you. Then, connect the HDMI cable (image below) to the laptop."

textFileControlIntro = "After recording a video clip, you can rewatch it here. If you are unhappy with it, you may delete it. Please be aware that you can only delete the last clip you recorded."

textButtonContinue = "Continue"
textButtonSkip = "Skip"
textButtonBack = "Back"
textButtonDelete = "Delete"
textButtonCancel = "Cancel"
textButtonRewatch = "Rewatch last video clip"
textButtonDeleteLatest = "Delete last video clip"
textButtonFinish = "Finish recording and start merging clips"

textDeleteAreYouSure = "Are you sure you want to delete the last clip?"

class VideoCabinInstructions:
    def __init__(self) -> None:
        pass

    # To make switching around the order of the windows easier while in development, we use this method to define the order and let the buttons point to this function
    def orderControl(direction, windowOld):
        # This is the order the windows are opened in
        options = {0: VideoCabinInstructions.introWindow,
                   1: VideoCabinInstructions.hardwareSetup,
                   2: VideoCabinInstructions.audioCalibration,
                   3: VideoCabinInstructions.fileControl}
        
        # To use the variable, we need to clarify that it is a global one
        global orderControlCounter

        tempCounter = orderControlCounter

        if(direction == 'continue'):
            orderControlCounter += 1
        if(direction == 'back'):
            orderControlCounter -= 1
        if(direction == 'skip'):
            orderControlCounter = int(len(options)-1)

        if(orderControlCounter >= 0 and orderControlCounter < len(options)):
            options[orderControlCounter](windowOld)
            
        # Displaying errors
        if(orderControlCounter < 0):
            print("orderControlCounter < 0, something went wrong.")
            # In case of error, the counter variable needs to be set back
            orderControlCounter = tempCounter
        if(orderControlCounter >= len(options)):
            print("You went too far! This option is not (yet) defined.")
            orderControlCounter = tempCounter

    # Get the size of an image and dynamically resize it to fit on the GUI window.
    # Since most images have a greater width than height, it should be enough to scale on that axis. TODO: If not, first check which side is larger.
    def resizeImg(img, resizeFactor):
        # Find the factor the images needs to be scaled with to fit into the window
        scalingFactor = (img.size[0] / windowWidth) * resizeFactor

        # Calculate the new values of the window, depending on the previous found factor
        newSizeX = (img.size[0] / scalingFactor)
        newSizeY = (img.size[1] / scalingFactor)

        # Reduce the size of the image by another value, to leave some room at the sides of the GUI window
        newSizeX = int(newSizeX * 0.9)
        newSizeY = int(newSizeY * 0.9)

        # Debug
        #print(str(newSizeX) + ", " + str(newSizeY))

        imgResize = img.resize((newSizeX, newSizeY), Image.ANTIALIAS)

        return imgResize

    def playLatestVideo():
        # Get all video files
        files = glob.glob(videoFileDir + "/*.mkv")
        # Play the last one in the list
        if(len(files) > 0):
            p = subprocess.Popen([videoPlayerDir, "file:///"+str(files[len(files)-1])])

    def startMergeControl(windowOld):
        if(windowOld is not None):
            windowOld.destroy()
        os.system("python D:/GitHub/VideoCabinPython/VideoCabin2.py")

    def deleteLatestVideo(windowOld):
        def removeFile(windowOld):
            # Delete the file
            if(len(files) > 0):
                os.remove(str(files[len(files)-1]))
            windowOld.destroy()

        # Get all video files
        files = glob.glob(videoFileDir + "/*.mkv")

        popUpWidth = int(0.5 * windowWidth)
        popUpHeight = int(0.3 * windowHeight)

        areYouSureWindow = tk.Toplevel(windowOld)
        areYouSureWindow.geometry(str(popUpWidth) + "x" + str(popUpHeight) + "+" + str(windowPositionX + int(windowWidth * 0.25)) + "+" + str(int(windowPositionY + 40)))
        textFont = (textFontStyle,textFontSize)

        label_areYouSure = Label(areYouSureWindow, text=textDeleteAreYouSure, font=textFont, wraplength=int(popUpWidth-20)).grid(row=0, padx=paddingX, pady=paddingY)

        button_cancel = Button(areYouSureWindow, text=textButtonCancel, font=textFont, command= lambda: areYouSureWindow.destroy()).grid(row=1, padx=paddingX, pady=paddingY)
        button_delete = Button(areYouSureWindow, text=textButtonDelete, font=textFont, command= lambda: removeFile(areYouSureWindow)).grid(row=2, padx=paddingX, pady=paddingY)

    # Window for reviewing the last clip recorded and to delete it, if needed
    def fileControl(windowOld):
        if(windowOld is not None):
            windowOld.destroy()

        windowNew = tk.Tk()
        windowNew.geometry(str(windowWidth) + "x" + str(windowHeight) + "+" + str(windowPositionX) + "+" + str(windowPositionY))
        windowNew.title("Video Files")
        textFont = (textFontStyle,textFontSize)

        text_intro = Label(windowNew, text=textFileControlIntro, font=textFont, wraplength=labelWrapLength).grid(row=0, padx=paddingX, pady=paddingY)

        button_rewatchLatest = Button(windowNew, text=textButtonRewatch, font=textFont, command=VideoCabinInstructions.playLatestVideo).grid(row=1, padx=paddingX, pady=paddingY)
        button_deleteLatest = Button(windowNew, text=textButtonDeleteLatest, font=textFont, command= lambda: VideoCabinInstructions.deleteLatestVideo(windowNew)).grid(row=2, padx=paddingX, pady=paddingY)
        button_finish = Button(windowNew, text=textButtonFinish, font=textFont, command= lambda: VideoCabinInstructions.startMergeControl(windowNew)).grid(row=3, padx=paddingX, pady=paddingY)

        windowNew.mainloop()
        

    # Instructions for audio calibration
    def audioCalibration(windowOld):
        if(windowOld is not None):
            windowOld.destroy()
        
        windowNew = tk.Tk()
        windowNew.geometry(str(windowWidth) + "x" + str(windowHeight) + "+" + str(windowPositionX) + "+" + str(windowPositionY))
        windowNew.title("Audio calibration")

        textFont = (textFontStyle,textFontSizeSmaller)
        text_audio1 = Label(windowNew, text=textAudioInstructions1, font=textFont, wraplength=labelWrapLength )
        text_audio1.grid(row=0, padx=paddingX, pady=paddingY)
        text_audio2 = Label(windowNew, text=textAudioInstructions2, font=textFont, wraplength=labelWrapLength )
        text_audio2.grid(row=1, padx=paddingX, pady=paddingY)
        text_audio3 = Label(windowNew, text=textAudioInstructions3, font=textFont, wraplength=labelWrapLength )
        text_audio3.grid(row=2, padx=paddingX, pady=paddingY)

        # Load the image and resize it
        img = VideoCabinInstructions.resizeImg(Image.open(audioLevelImg), 1)
        img = ImageTk.PhotoImage(img)

        labelAudioLevelImg = Label(windowNew, image=img).grid(row=3, padx=paddingX, pady=paddingY)

        text_audio4 = Label(windowNew, text=textAudioInstructions4, font=textFont, wraplength=labelWrapLength )
        text_audio4.grid(row=4, padx=paddingX, pady=paddingY)

        # TODO: Add (real) pictures
        img2 = VideoCabinInstructions.resizeImg(Image.open(audioKnob), 2)
        img2 = ImageTk.PhotoImage(img2)

        labelAudioKnow = Label(windowNew, image=img2).grid(row=5, padx=paddingX, pady=paddingY)

        text_audio5 = Label(windowNew, text=textAudioInstructions5, font=textFont, wraplength=labelWrapLength )
        text_audio5.grid(row=6, padx=paddingX, pady=paddingY)

        button_continue = Button(windowNew, text=textButtonContinue, font=textFont, command= lambda: VideoCabinInstructions.orderControl("continue", windowNew)).grid(row=7, padx=paddingX, pady=paddingY)
        button_back = Button(windowNew, text=textButtonBack, font=textFont, command= lambda: VideoCabinInstructions.orderControl("back", windowNew)).grid(row=8, padx=paddingX, pady=paddingY)

        windowNew.mainloop()

    def introWindow(windowOld):
        if(windowOld is not None):
            windowOld.destroy()

        windowNew = tk.Tk()
        windowNew.title("Instructions")
        windowNew.geometry(str(windowWidth) + "x" + str(windowHeight) + "+" + str(windowPositionX) + "+" + str(windowPositionY))

        textFont = (textFontStyle,textFontSize)

        # Welcome messages
        label_welcome1 = Label(windowNew, text=textWelcomeMessage1, font=textFont, wraplength=labelWrapLength )
        label_welcome1.grid(row=0, padx=paddingX, pady=50)
        label_welcome2 = Label(windowNew, text=textWelcomeMessage2, font=textFont, wraplength=labelWrapLength )
        label_welcome2.grid(row=1, padx=paddingX, pady=50)

        # Buttons
        button_continue = Button(windowNew, text=textButtonContinue, font=textFont, command= lambda: VideoCabinInstructions.orderControl("continue", windowNew))
        button_continue.grid(row=2, padx=paddingX, pady=10)
        button_skip = Button(windowNew, text=textButtonSkip, font=textFont, command= lambda: VideoCabinInstructions.orderControl("skip", windowNew))
        button_skip.grid(row=3, padx=paddingX, pady=10)

        windowNew.mainloop()

    def hardwareSetup(windowOld):
        if(windowOld is not None):
            windowOld.destroy()

        windowNew = tk.Tk()
        windowNew.title("Hardware Setup")
        windowNew.geometry(str(windowWidth) + "x" + str(windowHeight) + "+" + str(windowPositionX) + "+" + str(windowPositionY))

        textFont = (textFontStyle,textFontSize)

        label_hardwareSetup1 = Label(windowNew, text=textHardwareSetup1, font=textFont, wraplength=labelWrapLength).grid(row=0, padx=paddingX, pady=paddingY)

        imgHDMI = VideoCabinInstructions.resizeImg(Image.open(hdmiCable),2)
        imgHDMI = ImageTk.PhotoImage(imgHDMI)

        label_imgHDMI = Label(windowNew, image = imgHDMI).grid(row = 1, padx=paddingX, pady=paddingY)

        button_continue = Button(windowNew, text=textButtonContinue, font=textFont, command= lambda: VideoCabinInstructions.orderControl("continue", windowNew)).grid(row=2, padx=paddingX, pady=paddingY)
        button_back = Button(windowNew, text=textButtonBack, font=textFont, command= lambda: VideoCabinInstructions.orderControl("back", windowNew)).grid(row=3, padx=paddingX, pady=paddingY)

        windowNew.mainloop()

def main():
  VideoCabinInstructions.orderControl(None, None)
  
if __name__== "__main__":
  main()