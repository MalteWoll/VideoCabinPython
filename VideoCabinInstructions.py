# Author: Malte Wollermann

# tkinter for GUI
import tkinter as tk
from tkinter import Grid, Label
from tkinter import Button
import tkinter

from threading import Thread

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

import time

# for window positioning, these need to be set to the appropriate resolution
desktopResolutionX = 1920
desktopResolutionY = 1080

# these parameters need to be set to set the window size we want
windowWidth = int(desktopResolutionX / 2.5)
windowHeight = desktopResolutionY

# these parameters need to be set to place the window where we want it to be
windowPositionX = 0 + 1920 - windowWidth
windowPositionY = 0

# counter variable for controlling the order in which instructional windows are opened up
orderControlCounter = 0

# Path to video files
videoFileDir = "D:/obs_scripts/python/videoSource"
videoFileDir2 = "C:/Users/Video-Selfie/Videos/VideoCabinFiles"

# Path to images files
imageFilesDir = "C:/Users/malte/OneDrive/Bilder/GUIimages"
imageFilesDir2 = "C:/Users/Video-Selfie/Videos/GUIimages"

# Path to the .exe of the video player to be used
videoPlayerDir = "D:/Program Files/VideoLAN/VLC/vlc.exe"
videoPlayerDir2 = "C:/Program Files/VideoLAN/VLC/vlc.exe"

# Path to OBS
obsDir = "D:/Program Files/obs-studio/bin/64bit"
obsDirExe = "D:/Program Files/obs-studio/bin/64bit/obs64.exe"
obsDir2 = "C:/Program Files/obs-studio/bin/64bit"
obsDirExe2 = "C:/Program Files/obs-studio/bin/64bit/obs64.exe"

mergerDir = "D:/GitHub/VideoCabinPython/VideoCabin2.py"
mergerDir2 = "C:/Users/Video-Selfie/Videos/VideoCabin2.py"

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
imagePathExtendMonitor = imageFilesDir + "/notifications.jpg"
imagePathProject = imageFilesDir + "/project.jpg"
imagePathProject2 = imageFilesDir + "/project2.jpg"
imagePathBauchbinde = imageFilesDir + "/bauchbinde.jpg"
imagePathBauchbindeButton = imageFilesDir + "/bauchbinde_button.jpg"
imagePathRecordButton = imageFilesDir + "/record_button.jpg"
imagePathPiPButton = imageFilesDir + "/PiP_button.jpg"
imagePathPiP2Button = imageFilesDir + "/PiP_button2.jpg"
imagePathPresLargeButton = imageFilesDir + "/presLarge_button.jpg"
imagePathPresSmallButton = imageFilesDir + "/presSmall_button.jpg"
imagePathBackgroundButton = imageFilesDir + "/background_button.jpg"
imagePathBackgrounds = imageFilesDir + "/backgrounds.jpg"
imagePathPiP1 = imageFilesDir + "/scene_PiP1.jpg"
imagePathPiP2 = imageFilesDir + "/scene_PiP2.jpg"
imagePathPresLarge = imageFilesDir + "/scene_presLarge.jpg"
imagePathPresSmall = imageFilesDir + "/scene_presSmall.jpg"
imagePathBackground = imageFilesDir + "/scene_backGround.jpg"

# Some parameters for formatting text
labelWrapLength = windowWidth-100
paddingX = 10
paddingY = 10
textFontStyle = "Helvetica"
textFontSize = 20
textFontSizeSmaller = 16

textWelcomeMessage1 = "Willkommen zur Video Cabin! Bitte folgen Sie dieser Anleitung, um Ihre eigenen Video zu erstellen."
textWelcomeMessage2 = "Drücken Sie auf den \"Weiter\" Button um die Anleitung zu durchlaufen. Wenn Sie mit dem Aufbau bereits vertraut sind, können Sie den \"Überspringen\" Button drücken."

textPhantomPower1 = "Bitte drücken Sie auf den 48V Knopf auf dem Audio Interface auf Ihrer linken Seite (siehe Bild)."
textPhantomPower2 = "\"48V\" sollte danach rot leuchten."

textStartOBS1 = "Bitte drücken Sie auf den Button unter diesem Text, um die Aufnahmesoftware zu starten."

textCameraOn1 = "Schalten Sie nun die Kamera ein. Drehen Sie dafür den Drehknopf oben auf der Kamera auf \"ON\" (Siehe Bild)."
textCameraOn2 = "Zusätzlich muss der Live View eingeschaltet werden. Drücken Sie dafür auf den \"LV\" Knopf auf der Kamera, wie im Bild gezeigt."

textLaptop1 = "Platzieren Sie Ihren Laptop auf dem Dafür vorgesehenen Platz, unterhalb der Kamera. Stellen Sie sicher, dass der Bildschirm nicht die Kamera blockiert."
textLaptop2 = "Verbinden Sie den Laptop mit dem dafür vorgesehenen HDMI Kabel. Wenn Ihr Laptop keinen Anschluss für HDMI hat, benutzen Sie einen der bereitgelegten Adapter."

textCheckOBS = "Auf dem rechten Monitor sollte nun der Desktophintergrund ihres Laptops zu sehen sein. Falls der Monitor schwarz bleibt, drücken Sie bitte auf den Button um die Aufnahmesoftware neuzustarten."
textCheckOBS2 = "Wenn der rechte Monitor nicht mehr schwarz ist, drücken Sie wie gewohnt auf \"Weiter\""

textLaptop3 = "Der Bildschirm muss zunächst erweitert werden. Klicken Sie dafür auf dem Laptop auf das Sprechblasen Symbol in der unteren rechten Ecke des Bildschirms."
textLaptop4 = "Klicken Sie dann auf den Button \"Projizieren\" am unteren Rand des Bildschirms (siehe unten). Wenn der Button nicht angezeigt wird, klicken Sie zuerst auf \"Erweitern\"."
textLaptop5 = "Klicken Sie dann auf \"Erweitern\" (siehe Bild)."

textPresenter1 = "Nehmen Sie den Presenter und schieben Sie den USB Anschluss heraus, wie im Bild gezeigt."
textPresenter2 = "Verbinden Sie den USB Anschluss mit einem der USB Ports Ihres Laptops."
textPresenter3 = "Starten Sie Powerpoint auf Ihrem Laptop und starten Sie Ihre Präsentation. Sie können nun mit dem Presenter vor und zurück in Ihren Folien gehen."

textRecordControl1 = "Möchten Sie eine Bauchbinde verwenden? Falls ja, geben Sie bitte Ihren Namen (und/oder Fakultät oder andere Informationen) in das Feld auf der linken Bildschirmseite ein."
textRecordControl2 = "Im Folgenden erhalten Sie eine kurze Übersicht über die verschiedenen Szenen, die Sie verwenden können."
textRecordControl3 = "Mit dem ersten Button, \"Picture in Picture 1\", werden Sie in groß angezeigt, während die Präsentation in einem Fenster daneben gezeigt wird."
textRecordControl4 = "Mit dem zweiten Button, \"Picture in Picture 2\", wird die Präsentation in groß angezeigt, während Sie in einem kleinen Fenster in der oberen Ecke des Bildes zu sehen sind."
textRecordControl5 = "Mit dem dritten Button, \"Präsentation groß\", wird die Präsentation in groß auf dem Fernseher hinter Ihnen angezeigt."
textRecordControl6 = "Probieren Sie die verschiedenen Szenen aus um herauszufinden, welche am Besten zu Ihrer Präsentation passt. Sie können diese natürlich jederzeit umstellen."
textRecordControl7 = "Wenn Sie Ihren Namen per Bauchbinde einblenden wollen, drücken Sie auf den Button der unter diesem Text beispielhaft angezeigt wird. Die Bauchbinde wird 5 Sekunden angezeigt und verschwindet dann wieder."
textRecordControl8 = "Mit dem vierten Button, \"Präsentation klein\", wird die Präsentation in etwas verkleinerter Größe hinter Ihnen angezeigt, sodass Sie sie möglichst nicht verdecken."
textRecordControl9 = "Mit dem letzten der fünf Buttons, \"Hintergrund\", wird lediglich ein Hintergrund auf dem Fernseher angezeigt, vor dem Sie stehen. Das ist sinnvoll, wenn Sie keine Präsentation abspielen wollen."

textRecordControl10 = "Sie können außerdem zwischen drei Hintergründen wählen. Diese wählen Sie, wie unten abgebildet, in der letzten Reihe der Buttons aus."

textAudioInstructions1 = "Stellen Sie sich aufrecht auf die Markierung auf dem Boden, als würden Sie präsentieren, und reden Sie in normaler Lautstärke. Überprüfen Sie die Lautstärke auf dem linken Monitor (siehe Bild). Das Lautstärkelevel sollte im gelben Bereich liegen."
textAudioInstructions2 = "Wenn die Lautstärke im grünen Bereich liegt, drehen Sie den Knopf auf dem Audio Interface im Uhrzeigersinn (siehe Bild) und reden Sie erneut in normaler Lautstärke. Liegt die Lautstärke im roten Bereich, drehen Sie den Knopf gegen den Uhrzeigersinn."

textRecording1 = "Machen Sie nun eine Testaufnahme! Drücken Sie auf den \"Aufnahme\" Button auf der linken Bildschirmseite, nach fünf Sekunden Countdown beginnt die Aufnahme. Wenn Sie eine Bauchbinde verwenden wollen, drücken Sie vorher auf \"Bauchbinde\"."
textRecording2 = "Reden Sie einige Sätze und gehen Sie durch Ihre Folien, um ein Gefühl für den Aufbau zu bekommen. Beenden Sie die Aufnahme durch erneutes Drücken des \"Aufnahme\" Buttons."
textRecording4 = "Sie können so viele Aufnahmen machen wie sie wollen. Sie können auf den nächsten Seiten nach einer Aufnahme das jeweils letzte Video anschauen, löschen, oder zuschneiden."
textRecording3 = ""

textReviewVideo = "Drücken Sie den Button unterhalb um das letzte Video erneut anzusehen. Bitte schließen Sie danach das Fenster des Videoplayers durch Drücken des Kreuzes in der oberen rechten Ecke."
textDeleteVideo = "Drücken Sie auf den Button unterhalb um das letzte aufgenommene Video permanent zu löschen."
textTrimVideo = "Drücken Sie auf den Button unterhalb um bis zu 10 Sekunden am Ende des Videos wegzuschneiden. Sie können das geschnittene Video dann ansehen und dann bestätigen, dass Sie es behalten wollen. Falls nicht, können Sie erneut schneiden oder abbrechen."
textFinish = "Drücken Sie auf den Button unterhalb um die Aufnahmen zu beenden und zum Bildschirm für das Zusammenführen der Videos zu gelangen."

textFileControlIntro = "Not sure what's here."

textButtonContinue = "Weiter"
textButtonSkip = "Überspringen"
textButtonBack = "Zurück"
textButtonDelete = "Löschen"
textButtonCancel = "Abbrechen"
textButtonRewatch = "Letztes Video ansehen"
textButtonDeleteLatest = "Letztes Video löschen"
textButtonFinish = "Aufnehmen beenden und Videos zusammenführen"
textButtonStartOBS = "Aufnahmesoftware starten"
textButtonTrimLatest = "Letztes Video zuschneiden"

textDeleteAreYouSure = "Sind Sie sicher dass Sie das letzte Video löschen wollen?"

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
                   4: VideoCabinInstructions.instructions_laptop1,
                   5: VideoCabinInstructions.instructions_laptop2,
                   6: VideoCabinInstructions.instructions_laptop3,
                   7: VideoCabinInstructions.instructions_checkOBS,
                   8: VideoCabinInstructions.instructions_presenter,
                   9: VideoCabinInstructions.instructions_recordControl1,
                   10: VideoCabinInstructions.instructions_recordControl2,
                   11: VideoCabinInstructions.instructions_recordControl3,
                   12: VideoCabinInstructions.instructions_recordControl4,
                   13: VideoCabinInstructions.instructions_audioLevel,
                   14: VideoCabinInstructions.instructions_recording,
                   15: VideoCabinInstructions.fileControl}
        
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
        for file in files:
            if "TRIM_" in file:
                files.remove(file)
        for file in files:
            if "UNTRIMMED_" in file:
                files.remove(file)
        # Play the last one in the list
        if(len(files) > 0):
            p = subprocess.Popen([videoPlayerDir, "file:///"+str(files[len(files)-1])])

    def startMergeControl(windowOld):
        if(windowOld is not None):
            windowOld.destroy()
        os.system("python " + mergerDir)

    @staticmethod
    def startOBS():
        # OBS requires you to be in the same directory before starting it, otherwise the start fails with an error
        t = Thread(target = lambda: os.system("cd " + "\"" + obsDir + "\"" + "& call " + "\""  + obsDirExe + "\""))
        t.start()

    def deleteLatestVideo(windowOld):
        def removeFile(windowOld):
            # Delete the file
            if(len(files) > 0):
                os.remove(str(files[len(files)-1]))
            windowOld.destroy()

        # Get all video files
        files = glob.glob(videoFileDir + "/*.mkv")
        for file in files:
            if "TRIM_" in file:
                files.remove(file)
        for file in files:
            if "UNTRIMMED_" in file:
                files.remove(file)

        popUpWidth = int(0.5 * windowWidth)
        popUpHeight = int(0.3 * windowHeight)

        areYouSureWindow = tk.Toplevel(windowOld)
        areYouSureWindow.geometry(str(popUpWidth) + "x" + str(popUpHeight) + "+" + str(windowPositionX + int(windowWidth * 0.25)) + "+" + str(int(windowPositionY + 40)))
        textFont = (textFontStyle,textFontSize)

        label_areYouSure = Label(areYouSureWindow, text=textDeleteAreYouSure, font=textFont, wraplength=int(popUpWidth-20)).grid(row=0, padx=paddingX, pady=paddingY)

        button_cancel = Button(areYouSureWindow, text=textButtonCancel, font=textFont, command= lambda: areYouSureWindow.destroy()).grid(row=1, padx=paddingX, pady=paddingY)
        button_delete = Button(areYouSureWindow, text=textButtonDelete, font=textFont, command= lambda: removeFile(areYouSureWindow)).grid(row=2, padx=paddingX, pady=paddingY)

    def trimLatestVideo(windowOld):
        # Get all video files
        files = glob.glob(videoFileDir + "/*.mkv")
        for file in files:
            if "TRIM_" in file:
                files.remove(file)
        for file in files:
            if "UNTRIMMED_" in file:
                files.remove(file)

        popUpWidth = int(0.7 * windowWidth)
        popUpHeight = int(0.5 * windowHeight)

        trimWindow = tk.Toplevel(windowOld)
        trimWindow.geometry(str(popUpWidth) + "x" + str(popUpHeight) + "+" + str(windowPositionX + int(windowWidth * 0.25)) + "+" + str(int(windowPositionY + 40)))
        txtFont = (textFontStyle,textFontSize)

        if(len(files) > 0):
            file = files[len(files)-1]

        # Let the user only interact with this window, as long as it is open
        trimWindow.grab_set()

        frame2 = tk.Frame(trimWindow, borderwidth=1)
     
        frame2.place(in_=trimWindow, anchor="c", relx=.5, rely=.1)
        playButton = Button(frame2, text="Play Video", command= lambda: VideoCabinInstructions.playVideo(file), font=txtFont)
        playButton.grid(column=1, row=0, padx=5,pady=5)

        frame3 = tk.Frame(trimWindow, borderwidth=1)
        frame3.place(in_=trimWindow, anchor="c", relx=.5, rely=.3)

        duration = tk.StringVar(trimWindow)
        spinbox = tk.Spinbox(frame3, from_=0, to = 10, width=3, font=('Helvetica', 40), textvariable=duration)
        spinbox.grid(column=0, row=0)

        frame4 = tk.Frame(trimWindow, borderwidth=1)
        frame4.place(in_=trimWindow, anchor="c", relx=.5, rely=.4)
        label_trimTimeText = Label(frame4, text="Sekunden am Ende des Videos schneiden", font=txtFont).grid(column=1, row=2)

        frame6 = tk.Frame(trimWindow, borderwidth=1)
        frame6.place(in_=trimWindow, anchor="c", relx=.5, rely=.65)
        button_previewTrim = Button(frame6, text="Videovorschau zugeschnittenes Video", font=txtFont, state='disabled', command= lambda: VideoCabinInstructions.playVideo(os.path.dirname(file)+"/TRIM_"+os.path.basename(file)))
        button_previewTrim.grid(column=0, row=0)

        frame7 = tk.Frame(trimWindow, borderwidth=1)
        frame7.place(in_=trimWindow, anchor="c", relx=.5, rely=.8)
        button_accept = Button(frame7, text="Zuschneiden bestätigen", state='disabled', font=txtFont, command= lambda: VideoCabinInstructions.trimApply(trimWindow, file))
        button_accept.grid(column=0, row=0, padx=5)
        button_cancel = Button(frame7, text="Abbrechen", font=txtFont, command= lambda: VideoCabinInstructions.trimCancel(trimWindow, file))
        button_cancel.grid(column=1, row=0, padx=5)

        frame5 = tk.Frame(trimWindow, borderwidth=1)
        frame5.place(in_=trimWindow, anchor="c", relx=.5, rely=.5)
        button_trim = Button(frame5, text="Zuschneiden", font=txtFont, command= lambda: VideoCabinInstructions.trimVideoFile(file, duration.get(), button_previewTrim, button_accept))
        button_trim.grid(column=0, row=0)

    def trimCancel(windowOld, file):
        # Check if the file is still opened in VLC and if yes, kill the process to make sure the file can be renamed
        try:
            os.system("taskkill /f /im vlc.exe")
        except:
            print("VLC was not running, no need to kill process.")
        # To make sure the process has been killed before continuing, we freeze the application for a second
        time.sleep(1)
        # Check if a trim file has been created and if yes, delete it, then close the window
        if(os.path.isfile(os.path.dirname(file)+"/TRIM_"+os.path.basename(file))):
            os.remove(os.path.dirname(file)+"/TRIM_"+os.path.basename(file))
        windowOld.destroy()

    def trimApply(windowOld, file):
        # Check if the file is still opened in VLC and if yes, kill the process to make sure the file can be renamed
        try:
            os.system("taskkill /f /im vlc.exe")
        except:
            print("VLC was not running, no need to kill process.")
        # To make sure the process has been killed before continuing, we freeze the application for a second
        time.sleep(1)
        # To be sure, check for the file
        if(os.path.isfile(os.path.dirname(file)+"/TRIM_"+os.path.basename(file))):
            # If it is there, remove the old file and rename the new file
            os.rename(file, os.path.dirname(file)+"/UNTRIMMED_"+os.path.basename(file))
            os.rename(os.path.dirname(file)+"/TRIM_"+os.path.basename(file), file)
        windowOld.destroy()

    def trimVideoFile(file, durationToTrim, button, button2):
        # Debug
        print(file + ", " + durationToTrim)

        # Get the duration of the video file
        cmd = ['ffprobe', '-i', file, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=%s' % ("p=0")]
        duration = float(subprocess.check_output(cmd))

        # Debug
        #print(duration)

        if(duration < float(durationToTrim)):
            messagebox.showerror(title="Error", message="Error: Trimming duration is longer than clip duration!")
        else:  
            if(os.path.isfile(os.path.dirname(file) + "/TRIM_" + os.path.basename(file))):
                os.remove(os.path.dirname(file) + "/TRIM_" + os.path.basename(file))
            dur = duration - float(durationToTrim)
            # Create the name for the temporary file
            trimmedFileName = os.path.dirname(file) + "/TRIM_" + os.path.basename(file)
            cmd2 = ['ffmpeg', '-ss', '0', '-i', file, '-t', str(dur), '-c', 'copy', trimmedFileName]
            subprocess.check_call(cmd2)

            # Set the buttons to active, since now there is a video to preview
            button.config(state="normal")
            button2.config(state="normal")

    def playVideo(file):
        # Debug
        #print(str(file))
        p = subprocess.Popen([videoPlayerDir, "file:///"+str(file)])

    # Window for reviewing the last clip recorded and to delete it, if needed
    def fileControl(windowOld):
        if(windowOld is not None):
            windowOld.destroy()

        windowNew = tk.Tk()
        windowNew.geometry(str(windowWidth) + "x" + str(windowHeight) + "+" + str(windowPositionX) + "+" + str(windowPositionY))
        windowNew.title("Video Files")
        textFont = (textFontStyle,textFontSize)

        button_back = Button(windowNew, text="Zurück zur Anleitung", font=textFont, command= lambda: VideoCabinInstructions.orderControl("back", windowNew)).grid(row=8, padx=paddingX, pady=paddingY)

        label_reviewText = Label(windowNew, text=textReviewVideo, wraplength=labelWrapLength, font=textFont).grid(row=0, padx=paddingX, pady=paddingY)
        button_rewatchLatest = Button(windowNew, text=textButtonRewatch, font=textFont, command=VideoCabinInstructions.playLatestVideo).grid(row=1, padx=paddingX, pady=paddingY)

        label_deleteLast = Label(windowNew, text=textDeleteVideo, wraplength=labelWrapLength, font=textFont).grid(row=2, padx=paddingX, pady=paddingY)
        button_deleteLatest = Button(windowNew, text=textButtonDeleteLatest, bg="red", font=textFont, command= lambda: VideoCabinInstructions.deleteLatestVideo(windowNew)).grid(row=3, padx=paddingX, pady=paddingY)
        
        label_trimLast = Label(windowNew, text=textTrimVideo, wraplength=labelWrapLength, font=textFont).grid(row=4, padx=paddingX, pady=paddingY)
        button_trimLatest = Button(windowNew, text=textButtonTrimLatest, font=textFont, command= lambda: VideoCabinInstructions.trimLatestVideo(windowNew)).grid(row=5, padx=paddingX, pady=paddingY)

        label_finish = Label(windowNew, text=textFinish, wraplength=labelWrapLength, font=textFont).grid(row=6, padx=paddingX, pady=paddingY)
        button_finish = Button(windowNew, text=textButtonFinish, font=textFont, command= lambda: VideoCabinInstructions.startMergeControl(windowNew)).grid(row=7, padx=paddingX, pady=paddingY)

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

    def instructions_laptop1(windowOld):
        if(windowOld is not None):
            windowOld.destroy()

        windowNew = tk.Tk()
        windowNew.geometry(str(windowWidth) + "x" + str(windowHeight) + "+" + str(windowPositionX) + "+" + str(windowPositionY))
        windowNew.title("Laptop Setup")
        textFont = (textFontStyle,textFontSize)

        label_laptop1 = Label(windowNew, text=textLaptop1, font=textFont, wraplength=labelWrapLength).grid(row=0, padx=paddingX, pady=paddingY)
        label_laptop2 = Label(windowNew, text=textLaptop3, font=textFont, wraplength=labelWrapLength).grid(row=1, padx=paddingX, pady=paddingY)

        img_notification = VideoCabinInstructions.resizeImg(Image.open(imagePathExtendMonitor), 8)
        img_notification = ImageTk.PhotoImage(img_notification)
        label_img_notification = Label(windowNew, image=img_notification)
        label_img_notification.grid(row=2, padx=paddingX, pady=paddingY)
        label_img_notification.image = img_notification

        label_laptop3 = Label(windowNew, text=textLaptop4, font=textFont, wraplength=labelWrapLength).grid(row=3, padx=paddingX, pady=paddingY)

        img_project = VideoCabinInstructions.resizeImg(Image.open(imagePathProject), 2)
        img_project = ImageTk.PhotoImage(img_project)
        label_img_project = Label(windowNew, image=img_project)
        label_img_project.grid(row=4, padx=paddingX, pady=paddingY)
        label_img_project.image = img_project

        button_continue = Button(windowNew, text=textButtonContinue, font=textFont, command= lambda: VideoCabinInstructions.orderControl("continue", windowNew)).grid(row=6, padx=paddingX, pady=paddingY)
        button_back = Button(windowNew, text=textButtonBack, font=textFont, command= lambda: VideoCabinInstructions.orderControl("back", windowNew)).grid(row=7, padx=paddingX, pady=paddingY)

    def restartOBS():
        # First, kill the OBS process
        os.system("taskkill /f /im obs64.exe")
        # Wait one second to make sure it's killed
        time.sleep(1)
        # Restart OBS
        VideoCabinInstructions.startOBS()

    def instructions_checkOBS(windowOld):
        if(windowOld is not None):
            windowOld.destroy()

        windowNew = tk.Tk()
        windowNew.geometry(str(windowWidth) + "x" + str(windowHeight) + "+" + str(windowPositionX) + "+" + str(windowPositionY))
        windowNew.title("Check OBS")
        textFont = (textFontStyle,textFontSize)

        label_checkOBS1 = Label(windowNew, text=textCheckOBS, font=textFont, wraplength=labelWrapLength).grid(row=0, padx=paddingX, pady=paddingY)

        button_restartOBS = Button(windowNew, text="Neustart Aufnahmesoftware", font=textFont, command=VideoCabinInstructions.restartOBS)
        button_restartOBS.grid(row=1, padx=paddingX, pady=paddingY)

        label_checkOBS2 = Label(windowNew, text=textCheckOBS2, font=textFont, wraplength=labelWrapLength).grid(row=2, padx=paddingX, pady=paddingY)

        button_continue = Button(windowNew, text=textButtonContinue, font=textFont, command= lambda: VideoCabinInstructions.orderControl("continue", windowNew)).grid(row=4, padx=paddingX, pady=paddingY)
        button_back = Button(windowNew, text=textButtonBack, font=textFont, command= lambda: VideoCabinInstructions.orderControl("back", windowNew)).grid(row=5, padx=paddingX, pady=paddingY)

    def instructions_laptop2(windowOld):
        if(windowOld is not None):
            windowOld.destroy()

        windowNew = tk.Tk()
        windowNew.geometry(str(windowWidth) + "x" + str(windowHeight) + "+" + str(windowPositionX) + "+" + str(windowPositionY))
        windowNew.title("Laptop Setup")
        textFont = (textFontStyle,textFontSize)

        label_laptop1 = Label(windowNew, text=textLaptop5, font=textFont, wraplength=labelWrapLength).grid(row=0, padx=paddingX, pady=paddingY)

        img_project = VideoCabinInstructions.resizeImg(Image.open(imagePathProject2), 3)
        img_project = ImageTk.PhotoImage(img_project)
        label_img_project = Label(windowNew, image=img_project)
        label_img_project.grid(row=1, padx=paddingX, pady=paddingY)
        label_img_project.image = img_project

        button_continue = Button(windowNew, text=textButtonContinue, font=textFont, command= lambda: VideoCabinInstructions.orderControl("continue", windowNew)).grid(row=6, padx=paddingX, pady=paddingY)
        button_back = Button(windowNew, text=textButtonBack, font=textFont, command= lambda: VideoCabinInstructions.orderControl("back", windowNew)).grid(row=7, padx=paddingX, pady=paddingY)

    def instructions_laptop3(windowOld):
        if(windowOld is not None):
            windowOld.destroy()

        windowNew = tk.Tk()
        windowNew.geometry(str(windowWidth) + "x" + str(windowHeight) + "+" + str(windowPositionX) + "+" + str(windowPositionY))
        windowNew.title("Laptop Setup")
        textFont = (textFontStyle,textFontSize)

        label_laptop1 = Label(windowNew, text=textLaptop2, font=textFont, wraplength=labelWrapLength).grid(row=0, padx=paddingX, pady=paddingY)

        img_laptopHDMI = VideoCabinInstructions.resizeImg(Image.open(imagePathLaptopHMDI), 1)
        img_laptopHDMI = ImageTk.PhotoImage(img_laptopHDMI)
        label_img_laptopHDMI = Label(windowNew, image=img_laptopHDMI)  
        label_img_laptopHDMI.grid(row=1, padx=paddingX, pady=paddingY)
        label_img_laptopHDMI.image = img_laptopHDMI

        button_continue = Button(windowNew, text=textButtonContinue, font=textFont, command= lambda: VideoCabinInstructions.orderControl("continue", windowNew)).grid(row=2, padx=paddingX, pady=paddingY)
        button_back = Button(windowNew, text=textButtonBack, font=textFont, command= lambda: VideoCabinInstructions.orderControl("back", windowNew)).grid(row=3, padx=paddingX, pady=paddingY)

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

        img_bauchbinde = VideoCabinInstructions.resizeImg(Image.open(imagePathBauchbinde), 1.5)
        img_bauchbinde = ImageTk.PhotoImage(img_bauchbinde)
        label_img_bauchbinde = Label(windowNew, image=img_bauchbinde)
        label_img_bauchbinde.grid(row=1, padx=paddingX, pady=paddingY)
        label_img_bauchbinde.image = img_bauchbinde

        label_recordControl2 = Label(windowNew, text=textRecordControl2, font=textFont, wraplength=labelWrapLength).grid(row=2, padx=paddingX, pady=paddingY)

        button_continue = Button(windowNew, text=textButtonContinue, font=textFont, command= lambda: VideoCabinInstructions.orderControl("continue", windowNew)).grid(row=3, padx=paddingX, pady=paddingY)
        button_back = Button(windowNew, text=textButtonBack, font=textFont, command= lambda: VideoCabinInstructions.orderControl("back", windowNew)).grid(row=4, padx=paddingX, pady=paddingY)

    def instructions_recordControl2(windowOld):
        if(windowOld is not None):
            windowOld.destroy()

        windowNew = tk.Tk()
        windowNew.geometry(str(windowWidth) + "x" + str(windowHeight) + "+" + str(windowPositionX) + "+" + str(windowPositionY))
        windowNew.title("Record Control 2")
        textFont = (textFontStyle,textFontSize)

        label_recordControl3 = Label(windowNew, text=textRecordControl3, font=textFont, wraplength=labelWrapLength).grid(row=0, padx=paddingX, pady=paddingY)

        img_pip1 = VideoCabinInstructions.resizeImg(Image.open(imagePathPiP1), 4)
        img_pip1 = ImageTk.PhotoImage(img_pip1)
        label_img_pip1 = Label(windowNew, image=img_pip1)
        label_img_pip1.grid(row=1, padx=paddingX, pady=paddingY)
        label_img_pip1.image = img_pip1

        label_recordControl4 = Label(windowNew, text=textRecordControl4, font=textFont, wraplength=labelWrapLength).grid(row=2, padx=paddingX, pady=paddingY)

        img_pip2 = VideoCabinInstructions.resizeImg(Image.open(imagePathPiP2), 4)
        img_pip2 = ImageTk.PhotoImage(img_pip2)
        label_img_pip2 = Label(windowNew, image=img_pip2)
        label_img_pip2.grid(row=3, padx=paddingX, pady=paddingY)
        label_img_pip2.image = img_pip2

        label_recordControl5 = Label(windowNew, text=textRecordControl5, font=textFont, wraplength=labelWrapLength).grid(row=4, padx=paddingX, pady=paddingY)

        img_presLarge = VideoCabinInstructions.resizeImg(Image.open(imagePathPresLarge), 4)
        img_presLarge = ImageTk.PhotoImage(img_presLarge)
        label_img_presLarge = Label(windowNew, image=img_presLarge)
        label_img_presLarge.grid(row=5, padx=paddingX, pady=paddingY)
        label_img_presLarge.image = img_presLarge

        button_continue = Button(windowNew, text=textButtonContinue, font=textFont, command= lambda: VideoCabinInstructions.orderControl("continue", windowNew)).grid(row=6, padx=paddingX, pady=paddingY)
        button_back = Button(windowNew, text=textButtonBack, font=textFont, command= lambda: VideoCabinInstructions.orderControl("back", windowNew)).grid(row=7, padx=paddingX, pady=paddingY)

    def instructions_recordControl4(windowOld):
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

    def instructions_recordControl3(windowOld):
        if(windowOld is not None):
            windowOld.destroy()

        windowNew = tk.Tk()
        windowNew.geometry(str(windowWidth) + "x" + str(windowHeight) + "+" + str(windowPositionX) + "+" + str(windowPositionY))
        windowNew.title("Record Control 2")
        textFont = (textFontStyle,textFontSize)

        label_recordControl1 = Label(windowNew, text=textRecordControl8, font=textFont, wraplength=labelWrapLength).grid(row=0, padx=paddingX, pady=paddingY)

        img_pip1 = VideoCabinInstructions.resizeImg(Image.open(imagePathPresSmall), 4)
        img_pip1 = ImageTk.PhotoImage(img_pip1)
        label_img_pip1 = Label(windowNew, image=img_pip1)
        label_img_pip1.grid(row=1, padx=paddingX, pady=paddingY)
        label_img_pip1.image = img_pip1

        label_recordControl2 = Label(windowNew, text=textRecordControl9, font=textFont, wraplength=labelWrapLength).grid(row=2, padx=paddingX, pady=paddingY)

        img_pip2 = VideoCabinInstructions.resizeImg(Image.open(imagePathBackground), 4)
        img_pip2 = ImageTk.PhotoImage(img_pip2)
        label_img_pip2 = Label(windowNew, image=img_pip2)
        label_img_pip2.grid(row=3, padx=paddingX, pady=paddingY)
        label_img_pip2.image = img_pip2

        button_continue = Button(windowNew, text=textButtonContinue, font=textFont, command= lambda: VideoCabinInstructions.orderControl("continue", windowNew)).grid(row=4, padx=paddingX, pady=paddingY)
        button_back = Button(windowNew, text=textButtonBack, font=textFont, command= lambda: VideoCabinInstructions.orderControl("back", windowNew)).grid(row=5, padx=paddingX, pady=paddingY)

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

        img_recordBtn = VideoCabinInstructions.resizeImg(Image.open(imagePathRecordButton), 5)
        img_recordBtn = ImageTk.PhotoImage(img_recordBtn)
        label_img_recordBtn = Label(windowNew, image=img_recordBtn)
        label_img_recordBtn.grid(row=1, padx=paddingX, pady=paddingY)
        label_img_recordBtn.image = img_recordBtn

        label_startRecording2 = Label(windowNew, text=textRecording2, font=textFont, wraplength=labelWrapLength).grid(row=2, padx=paddingX, pady=paddingY)
        label_startRecording3 = Label(windowNew, text=textRecording3, font=textFont, wraplength=labelWrapLength).grid(row=3, padx=paddingX, pady=paddingY)
        label_startRecording4 = Label(windowNew, text=textRecording4, font=textFont, wraplength=labelWrapLength).grid(row=4, padx=paddingX, pady=paddingY)

        button_continue = Button(windowNew, text=textButtonContinue, font=textFont, command= lambda: VideoCabinInstructions.orderControl("continue", windowNew)).grid(row=5, padx=paddingX, pady=paddingY)
        button_back = Button(windowNew, text=textButtonBack, font=textFont, command= lambda: VideoCabinInstructions.orderControl("back", windowNew)).grid(row=6, padx=paddingX, pady=paddingY)

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