# tkinter for GUI
import tkinter as tk
from tkinter import Grid, Label
from tkinter import Button
import tkinter

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
imageFilesDir = "C:/Users/malte/OneDrive/Bilder/GUIimages"

# Path to the .exe of the video player to be used
videoPlayerDir = "D:/Program Files/VideoLAN/VLC/vlc.exe"

# Path to OBS
obsDir = "D:/Program Files/obs-studio/bin/64bit"
obsDirExe = "D:/Program Files/obs-studio/bin/64bit/obs64.exe"

# Image file paths
imagePathPhantomPower1 = imageFilesDir + "/phantomPower1.jpg"
imagePathPhantomPower2 = imageFilesDir + "/phantomPower2.jpg"
imagePathCamera1 = imageFilesDir + "/camera1.jpg"
imagePathCamera2 = imageFilesDir + "/camera2.jpg"
imagePathLaptopHMDI = imageFilesDir + "/hdmiLaptop.jpg"
imagePathPresenter1 = imageFilesDir + "/presenter1.jpg"
imagePathPresenter2 = imageFilesDir + "/presenter2.jpg"
imagePathAudio1 = imageFilesDir + "/audiolevel1.jpg"
imagePathAudio2 = imageFilesDir + "/audioLevel2.jpg"

# Some parameters for formatting text
labelWrapLength = windowWidth-100
paddingX = 10
paddingY = 10
textFontStyle = "Helvetica"
textFontSize = 20
textFontSizeSmaller = 16

textWelcomeMessage1 = "Welcome to the Video Cabin! Please follow the instructions to learn how to create your videos."
textWelcomeMessage2 = "Press the 'Continue' button to follow the instructions. If you are already familiar with the application, you can skip this tutorial by pressing the 'Skip' button."

textPhantomPower1 = "To allow audio input, please press the 48V button on the front of the audio interface (the small red device) to your left. The exact location is pictured below."
textPhantomPower2 = "If successfull, the \"48V\" will glow red."

textStartOBS1 = "To start the recording software, press the button below."

textCameraOn1 = "Now the camera needs to be turned on. Turn the top right lever on the camera to \"ON\" (See the image below)."
textCameraOn2 = "Additionally, the live view needs to be enabled. To do so, press the \"LV\" button on the camera as shown in the image below."

textLaptop1 = "Place your laptop on the are in front of you, just below the camera. Make sure the screen does not block the camera."
textLaptop2 = "Connect the laptop with the HDMI cable. If the HDMI cable does not fit, try one of the adapters."

textPresenter1 = "Take the presenter from the desk. Slide out the USB device as shown in the images below."
textPresenter2 = "Connect the USB device to one of the USB ports of your laptop, as shown below."
textPresenter3 = "Start PowerPoint on your laptop and open your presentation. You can go back and forth within the slides with the presenter now."

textRecordControl1 = "You control your recordings with the buttons on the left side of this screens. First, type in your name (and/or field and faculty), if you want to show it at any points of the presentation."
textRecordControl2 = "You can switch between three scenes for your presentation. We will give you an overview how and what each scene looks like."
textRecordControl3 = "The first button, \"Fullscreen\" is used to show only the presentation, you will not be visible at all."
textRecordControl4 = "The second button, \"Totale\" is used to show the presentation on the TV in the background, with you standing on the side of it."
textRecordControl5 = "The third button, \"PiP\" is used for a picture-in-picture presentation with the presentation in fullscreen and you in the top right corner."
textRecordControl6 = "Feel free to try out the different scenes to find the one that you feel most comfortable with before you start recording. You can, of course, change the scene at any time."
textRecordControl7 = "If you want to blend in your name (and additional information you entered before), press the button shown below. The information will linger for 5 seconds, before fading out."

textAudioInstructions1 = "Stand between the floor markers and read the following sentence in your normal loudness. Check on the loudness meter on the left Monitor (image below). The level must be always between green and yellow."
textAudioInstructions2 = "If it's only green, adjust the level a little bit by turning the knob on the red audio interface (image below) clockwise. If it reaches the red zone, you must turn counterclockwise."

textRecording1 = "When you are ready to start, press the record button. After a five second countdown, the recording will begin. Pressing the button again will stop the recording."
textRecording2 = "You can record as many clips as you want. On the next page you have the ability to rewatch the last clip, and if you are unhappy with it to delete it."
textRecording3 = "When you are done with your recordings, you can merge the recorded clips. In the overview you can first rewatch them again, and then select or deselect the ones you wish to use."

textFileControlIntro = "Not sure what's here."

textButtonContinue = "Continue"
textButtonSkip = "Skip"
textButtonBack = "Back"
textButtonDelete = "Delete"
textButtonCancel = "Cancel"
textButtonRewatch = "Rewatch last video clip"
textButtonDeleteLatest = "Delete last video clip"
textButtonFinish = "Finish recording and start merging clips"
textButtonStartOBS = "Start recording software"

textDeleteAreYouSure = "Are you sure you want to delete the last clip?"

class VideoCabinInstructions:
    def __init__(self) -> None:
        pass

    # To make switching around the order of the windows easier while in development, we use this method to define the order and let the buttons point to this function
    def orderControl(direction, windowOld):
        # This is the order the windows are opened in
        options = {0: VideoCabinInstructions.introWindow,
                   1: VideoCabinInstructions.instructions_turnOnPhantom,
                   2: VideoCabinInstructions.instructions_openOBS,
                   3: VideoCabinInstructions.instructions_turnOnCamera,
                   4: VideoCabinInstructions.instructions_laptop,
                   5: VideoCabinInstructions.instructions_presenter,
                   6: VideoCabinInstructions.instructions_recordControl1,
                   7: VideoCabinInstructions.instructions_recordControl2,
                   8: VideoCabinInstructions.instructions_recordControl3,
                   9: VideoCabinInstructions.instructions_audioLevel,
                   10: VideoCabinInstructions.instructions_recording,
                   11: VideoCabinInstructions.fileControl}
        
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

    @staticmethod
    def startOBS():
        # OBS requires you to be in the same directory before starting it, otherwise the start fails with an error
        os.system("cd " + "\"" + obsDir + "\"" + "& call " + "\""  + obsDirExe + "\"")

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
        
    def instructions_turnOnPhantom(windowOld):
        if(windowOld is not None):
            windowOld.destroy()

        windowNew = tk.Tk()
        windowNew.geometry(str(windowWidth) + "x" + str(windowHeight) + "+" + str(windowPositionX) + "+" + str(windowPositionY))
        windowNew.title("Phantom Power")
        textFont = (textFontStyle,textFontSize)

        label_phantomPower1 = Label(windowNew, text=textPhantomPower1, font=textFont, wraplength=labelWrapLength).grid(row=0, padx=paddingX, pady=paddingY)

        img_phantomPower1 = ImageTk.PhotoImage(VideoCabinInstructions.resizeImg(Image.open(imagePathPhantomPower1), 1))
        label_img_phantomPower1 = Label(windowNew, image=img_phantomPower1)
        label_img_phantomPower1.grid(row=1, padx=paddingX, pady=paddingY)
        label_img_phantomPower1.image = img_phantomPower1

        label_phantomPower1 = Label(windowNew, text=textPhantomPower2, font=textFont, wraplength=labelWrapLength).grid(row=2, padx=paddingX, pady=paddingY)

        img_phantomPower2 = ImageTk.PhotoImage(VideoCabinInstructions.resizeImg(Image.open(imagePathPhantomPower2), 1))
        label_img_phantomPower2 = Label(windowNew, image=img_phantomPower2)
        label_img_phantomPower2.grid(row=3, padx=paddingX, pady=paddingY)
        label_img_phantomPower2.image = img_phantomPower2

        button_continue = Button(windowNew, text=textButtonContinue, font=textFont, command= lambda: VideoCabinInstructions.orderControl("continue", windowNew)).grid(row=4, padx=paddingX, pady=paddingY)
        button_back = Button(windowNew, text=textButtonBack, font=textFont, command= lambda: VideoCabinInstructions.orderControl("back", windowNew)).grid(row=5, padx=paddingX, pady=paddingY)

    def instructions_openOBS(windowOld):
        if(windowOld is not None):
            windowOld.destroy()

        windowNew = tk.Tk()
        windowNew.geometry(str(windowWidth) + "x" + str(windowHeight) + "+" + str(windowPositionX) + "+" + str(windowPositionY))
        windowNew.title("Start OBS")
        textFont = (textFontStyle,textFontSize)

        label_startOBS = Label(windowNew, text=textStartOBS1, font=textFont, wraplength=labelWrapLength).grid(row=0, padx=paddingX, pady=paddingY)

        button_startOBS = Button(windowNew, text=textButtonStartOBS, font=textFont, command= lambda: VideoCabinInstructions.startOBS()).grid(row=1, padx=paddingX, pady=paddingY)

        button_continue = Button(windowNew, text=textButtonContinue, font=textFont, command= lambda: VideoCabinInstructions.orderControl("continue", windowNew)).grid(row=2, padx=paddingX, pady=paddingY)
        button_back = Button(windowNew, text=textButtonBack, font=textFont, command= lambda: VideoCabinInstructions.orderControl("back", windowNew)).grid(row=3, padx=paddingX, pady=paddingY)

    def instructions_turnOnCamera(windowOld):
        if(windowOld is not None):
            windowOld.destroy()

        windowNew = tk.Tk()
        windowNew.geometry(str(windowWidth) + "x" + str(windowHeight) + "+" + str(windowPositionX) + "+" + str(windowPositionY))
        windowNew.title("Turn on camera")
        textFont = (textFontStyle,textFontSize)

        label_cameraOn1 = Label(windowNew, text=textCameraOn1, font=textFont, wraplength=labelWrapLength).grid(row=0, padx=paddingX, pady=paddingY)

        img_camera1 = VideoCabinInstructions.resizeImg(Image.open(imagePathCamera1), 2)
        img_camera1 = ImageTk.PhotoImage(img_camera1)
        label_img_camera1 = Label(windowNew, image=img_camera1)
        label_img_camera1.grid(row=1, padx=paddingX, pady=paddingY)
        label_img_camera1.image = img_camera1

        label_cameraOn2 = Label(windowNew, text=textCameraOn2, font=textFont, wraplength=labelWrapLength).grid(row=2, padx=paddingX, pady=paddingY)

        img_camera2 = VideoCabinInstructions.resizeImg(Image.open(imagePathCamera2), 2)
        img_camera2 = ImageTk.PhotoImage(img_camera2)
        label_img_camera2 = Label(windowNew, image=img_camera2)
        label_img_camera2.grid(row=3, padx=paddingX, pady=paddingY)
        label_img_camera2.image = img_camera2

        button_continue = Button(windowNew, text=textButtonContinue, font=textFont, command= lambda: VideoCabinInstructions.orderControl("continue", windowNew)).grid(row=4, padx=paddingX, pady=paddingY)
        button_back = Button(windowNew, text=textButtonBack, font=textFont, command= lambda: VideoCabinInstructions.orderControl("back", windowNew)).grid(row=5, padx=paddingX, pady=paddingY)

    def instructions_laptop(windowOld):
        if(windowOld is not None):
            windowOld.destroy()

        windowNew = tk.Tk()
        windowNew.geometry(str(windowWidth) + "x" + str(windowHeight) + "+" + str(windowPositionX) + "+" + str(windowPositionY))
        windowNew.title("Laptop Setup")
        textFont = (textFontStyle,textFontSize)

        label_laptop1 = Label(windowNew, text=textLaptop1, font=textFont, wraplength=labelWrapLength).grid(row=0, padx=paddingX, pady=paddingY)
        label_laptop2 = Label(windowNew, text=textLaptop2, font=textFont, wraplength=labelWrapLength).grid(row=1, padx=paddingX, pady=paddingY)

        img_laptopHDMI = VideoCabinInstructions.resizeImg(Image.open(imagePathLaptopHMDI), 1)
        img_laptopHDMI = ImageTk.PhotoImage(img_laptopHDMI)
        label_img_laptopHDMI = Label(windowNew, image=img_laptopHDMI)  
        label_img_laptopHDMI.grid(row=2, padx=paddingX, pady=paddingY)
        label_img_laptopHDMI.image = img_laptopHDMI

        button_continue = Button(windowNew, text=textButtonContinue, font=textFont, command= lambda: VideoCabinInstructions.orderControl("continue", windowNew)).grid(row=3, padx=paddingX, pady=paddingY)
        button_back = Button(windowNew, text=textButtonBack, font=textFont, command= lambda: VideoCabinInstructions.orderControl("back", windowNew)).grid(row=4, padx=paddingX, pady=paddingY)

    def instructions_presenter(windowOld):
        if(windowOld is not None):
            windowOld.destroy()

        windowNew = tk.Tk()
        windowNew.geometry(str(windowWidth) + "x" + str(windowHeight) + "+" + str(windowPositionX) + "+" + str(windowPositionY))
        windowNew.title("Connect Presenter")
        textFont = (textFontStyle,textFontSize)

        label_presenter1 = Label(windowNew, text=textPresenter1, font=textFont, wraplength=labelWrapLength).grid(row=0, padx=paddingX, pady=paddingY)

        img_presenter1 = VideoCabinInstructions.resizeImg(Image.open(imagePathPresenter1), 1)
        img_presenter1 = ImageTk.PhotoImage(img_presenter1)
        label_img_presenter1 = Label(windowNew, image=img_presenter1)
        label_img_presenter1.grid(row=1, padx=paddingX, pady=paddingY)
        label_img_presenter1.image = img_presenter1

        label_presenter2 = Label(windowNew, text=textPresenter2, font=textFont, wraplength=labelWrapLength).grid(row=2, padx=paddingX, pady=paddingY)

        img_presenter2 = VideoCabinInstructions.resizeImg(Image.open(imagePathPresenter2), 1.5)
        img_presenter2 = ImageTk.PhotoImage(img_presenter2)
        label_img_presenter2 = Label(windowNew, image=img_presenter2)
        label_img_presenter2.grid(row=3, padx=paddingX, pady=paddingY)
        label_img_presenter2.image = img_presenter2

        label_presenter3 = Label(windowNew, text=textPresenter3, font=textFont, wraplength=labelWrapLength).grid(row=4, padx=paddingX, pady=paddingY)

        button_continue = Button(windowNew, text=textButtonContinue, font=textFont, command= lambda: VideoCabinInstructions.orderControl("continue", windowNew)).grid(row=5, padx=paddingX, pady=paddingY)
        button_back = Button(windowNew, text=textButtonBack, font=textFont, command= lambda: VideoCabinInstructions.orderControl("back", windowNew)).grid(row=6, padx=paddingX, pady=paddingY)


    def instructions_recordControl1(windowOld):
        if(windowOld is not None):
            windowOld.destroy()

        windowNew = tk.Tk()
        windowNew.geometry(str(windowWidth) + "x" + str(windowHeight) + "+" + str(windowPositionX) + "+" + str(windowPositionY))
        windowNew.title("Record Control 1")
        textFont = (textFontStyle,textFontSize)

        label_recordControl1 = Label(windowNew, text=textRecordControl1, font=textFont, wraplength=labelWrapLength).grid(row=0, padx=paddingX, pady=paddingY)

        label_recordControl2 = Label(windowNew, text=textRecordControl2, font=textFont, wraplength=labelWrapLength).grid(row=1, padx=paddingX, pady=paddingY)

        button_continue = Button(windowNew, text=textButtonContinue, font=textFont, command= lambda: VideoCabinInstructions.orderControl("continue", windowNew)).grid(row=2, padx=paddingX, pady=paddingY)
        button_back = Button(windowNew, text=textButtonBack, font=textFont, command= lambda: VideoCabinInstructions.orderControl("back", windowNew)).grid(row=3, padx=paddingX, pady=paddingY)

    def instructions_recordControl2(windowOld):
        if(windowOld is not None):
            windowOld.destroy()

        windowNew = tk.Tk()
        windowNew.geometry(str(windowWidth) + "x" + str(windowHeight) + "+" + str(windowPositionX) + "+" + str(windowPositionY))
        windowNew.title("Record Control 2")
        textFont = (textFontStyle,textFontSize)

        label_recordControl3 = Label(windowNew, text=textRecordControl3, font=textFont, wraplength=labelWrapLength).grid(row=0, padx=paddingX, pady=paddingY)

        label_recordControl4 = Label(windowNew, text=textRecordControl4, font=textFont, wraplength=labelWrapLength).grid(row=1, padx=paddingX, pady=paddingY)

        label_recordControl5 = Label(windowNew, text=textRecordControl5, font=textFont, wraplength=labelWrapLength).grid(row=2, padx=paddingX, pady=paddingY)

        button_continue = Button(windowNew, text=textButtonContinue, font=textFont, command= lambda: VideoCabinInstructions.orderControl("continue", windowNew)).grid(row=3, padx=paddingX, pady=paddingY)
        button_back = Button(windowNew, text=textButtonBack, font=textFont, command= lambda: VideoCabinInstructions.orderControl("back", windowNew)).grid(row=4, padx=paddingX, pady=paddingY)

    def instructions_recordControl3(windowOld):
        if(windowOld is not None):
            windowOld.destroy()

        windowNew = tk.Tk()
        windowNew.geometry(str(windowWidth) + "x" + str(windowHeight) + "+" + str(windowPositionX) + "+" + str(windowPositionY))
        windowNew.title("Record Control 2")
        textFont = (textFontStyle,textFontSize)

        label_recordControl6 = Label(windowNew, text=textRecordControl6, font=textFont, wraplength=labelWrapLength).grid(row=0, padx=paddingX, pady=paddingY)

        label_recordControl7 = Label(windowNew, text=textRecordControl7, font=textFont, wraplength=labelWrapLength).grid(row=1, padx=paddingX, pady=paddingY)

        button_continue = Button(windowNew, text=textButtonContinue, font=textFont, command= lambda: VideoCabinInstructions.orderControl("continue", windowNew)).grid(row=2, padx=paddingX, pady=paddingY)
        button_back = Button(windowNew, text=textButtonBack, font=textFont, command= lambda: VideoCabinInstructions.orderControl("back", windowNew)).grid(row=3, padx=paddingX, pady=paddingY)

    def instructions_audioLevel(windowOld):
        if(windowOld is not None):
            windowOld.destroy()

        windowNew = tk.Tk()
        windowNew.geometry(str(windowWidth) + "x" + str(windowHeight) + "+" + str(windowPositionX) + "+" + str(windowPositionY))
        windowNew.title("Audio Level")
        textFont = (textFontStyle,textFontSize)

        label_audioLevel1 = Label(windowNew, text=textAudioInstructions1, font=textFont, wraplength=labelWrapLength).grid(row=0, padx=paddingX, pady=paddingY)

        img_audioLevel1 = VideoCabinInstructions.resizeImg(Image.open(imagePathAudio1), 1)
        img_audioLevel1 = ImageTk.PhotoImage(img_audioLevel1)
        label_img_audioLevel1 = Label(windowNew, image=img_audioLevel1)
        label_img_audioLevel1.grid(row=1, padx=paddingX, pady=paddingY)
        label_img_audioLevel1.image = img_audioLevel1

        label_audioLevel2 = Label(windowNew, text=textAudioInstructions2, font=textFont, wraplength=labelWrapLength).grid(row=2, padx=paddingX, pady=paddingY)

        img_audioLevel2 = VideoCabinInstructions.resizeImg(Image.open(imagePathAudio2), 1)
        img_audioLevel2 = ImageTk.PhotoImage(img_audioLevel2)
        label_img_audioLevel2 = Label(windowNew, image=img_audioLevel2)
        label_img_audioLevel2.grid(row=3, padx=paddingX, pady=paddingY)
        label_img_audioLevel2.image = img_audioLevel2

        button_continue = Button(windowNew, text=textButtonContinue, font=textFont, command= lambda: VideoCabinInstructions.orderControl("continue", windowNew)).grid(row=4, padx=paddingX, pady=paddingY)
        button_back = Button(windowNew, text=textButtonBack, font=textFont, command= lambda: VideoCabinInstructions.orderControl("back", windowNew)).grid(row=5, padx=paddingX, pady=paddingY)

    def instructions_recording(windowOld):
        if(windowOld is not None):
            windowOld.destroy()

        windowNew = tk.Tk()
        windowNew.geometry(str(windowWidth) + "x" + str(windowHeight) + "+" + str(windowPositionX) + "+" + str(windowPositionY))
        windowNew.title("Start Recording")
        textFont = (textFontStyle,textFontSize)

        label_startRecording1 = Label(windowNew, text=textRecording1, font=textFont, wraplength=labelWrapLength).grid(row=0, padx=paddingX, pady=paddingY)

        label_startRecording2 = Label(windowNew, text=textRecording2, font=textFont, wraplength=labelWrapLength).grid(row=1, padx=paddingX, pady=paddingY)

        label_startRecording3 = Label(windowNew, text=textRecording3, font=textFont, wraplength=labelWrapLength).grid(row=2, padx=paddingX, pady=paddingY)

        button_continue = Button(windowNew, text=textButtonContinue, font=textFont, command= lambda: VideoCabinInstructions.orderControl("continue", windowNew)).grid(row=3, padx=paddingX, pady=paddingY)
        button_back = Button(windowNew, text=textButtonBack, font=textFont, command= lambda: VideoCabinInstructions.orderControl("back", windowNew)).grid(row=4, padx=paddingX, pady=paddingY)

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



def main():
  VideoCabinInstructions.orderControl(None, None)
  
if __name__== "__main__":
  main()