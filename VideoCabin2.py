# tkinter for GUI
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font
from tkinter.ttk import Style
from typing import Collection, Sized

import threading

# glob for finding files
import glob

# subprocess and os for operating system operations
import subprocess
import os
import shutil

# owncloud for upload to sciebo
import owncloud

# shutil for copying files between partitions
from shutil import copyfile

# datetime and re for creating files and directories with dates and times
from datetime import datetime

# Important! In OBS, check 'Generate file name without space' in the output settings

# Path to the recorded video files from OBS
path = "D:/obs_scripts/python/videoSource"
path2 = "C:/Users/Video-Selfie/Videos/VideoCabinFiles"

# The directory the output file is created at
outputPath = "D:/obs_scripts/python/Output"
outputPath2 = "C:/Users/Video-Selfie/Videos/Output"
globalOutputFilePath = ""
outputFilePath = ""

vlcPath = "D:/Program Files/VideoLAN/VLC/vlc.exe"
vlcPath2 = "C:/Program Files/VideoLAN/VLC/vlc.exe"

instructionsPath = "python D:/GitHub/VideoCabinPython/VideoCabinInstructions.py"

bgColor = '#1e1e1e'
btnColor = '#4c4c4c'
fgColor = '#ffffff'

initialPath = path

# Variables for the pages of frames, in case the user records more than 12 video files
frameCounter = 0
filesInFrameCounter = 0
pageCounter = 0
frames = {}

# Get all files in the specified path when starting the script, then remove those marked as trimmed, although there should not be any at this point
files = glob.glob(path + "/*.mkv")
for file in files:
    if "TRIM_" in file:
        files.remove(file)
for file in files:
    if "UNTRIMMED_" in file:
        files.remove(file)

# Empty global list variables for later use
filesToUse = []
files_durations = []
useButtons = []

# Fixed textsize for every font
textSize = 18

class VideoCabin2:
    def __init__(self) -> None:
        pass

    def backToInstructions(windowOld):
        windowOld.destroy()
        os.system(instructionsPath)

    # Creates an output folder with the current date and time, so every output is saved
    def createOutputFolder():
        global outputFilePath

        # Since creating a directory with spaces is not possible with os.mkdir, spaces need to be turned into underscores
        now = str(datetime.now())
        translate_table = str.maketrans({' ': '_', ':': '_'})
        now = now.translate(translate_table)

        # Create the unique output folder for the user, based on time and date
        now = now[:-7]
        outputFilePath = outputPath + "/Output_"+now
        os.mkdir(outputFilePath)

        print("Output file path: " + str(outputFilePath))

        return outputFilePath

    # Opens a file with the specified program, e.g. VLC
    def playVideo(file):
        p = subprocess.Popen([vlcPath, "file:///"+str(file)])

    # Method for changing the working directory
    # We do not use this anymore
    def getFolderPath(labelDirectory, labelVideoFiles):
        # Update path and label
        path = str(filedialog.askdirectory())
        labelDirectory.config(text="Your directory: " + path)
        # Update video file number label for new path
        files = glob.glob(path + "/*.mkv")
        labelVideoFiles.config(text=str(len(files)) + " video files found.")

    # Method for resetting the directory to the one the script has been called with
    # We do not use this anymore
    def setInitialPath(labelDirectory, labelVideoFiles):
        # Update path and label
        path = initialPath
        labelDirectory.config(text="Your directory: " + path)
        # Update video file number label for path
        files = glob.glob(path + "/*.mkv")
        labelVideoFiles.config(text=str(len(files)) + " video files found.")

    # Remove the file from the list of files to use and change the button color to red and the text to "unused"
    def unuseFile(file,i):
        filesToUse.remove(file)
        useButtons[i].config(text="Nicht benutzen", bg="red", fg="white", command= lambda file=file, i=i: VideoCabin2.useFile(file,i))
        # Debug
        print(filesToUse)

    # Add the video file to the list of files to use, change button to green and text on it to "used"
    def useFile(file,i):
        filesToUse.append(file)
        useButtons[i].config(text="Benutzen", bg="green", fg="white", command= lambda file=file, i=i: VideoCabin2.unuseFile(file,i))
        # Files are being sorted after every time they get added, so the original order is kept
        # TODO: Maybe add a way to let the user sort themselves? Could be complicated, especially on touchscreen
        filesToUse.sort()
        # Debug
        print(filesToUse)

    # Moves all video files to a temporary folder
    def moveToTemp(outputFilePath):
        filelist = glob.glob(os.path.join(path, "*"))
        os.mkdir(outputFilePath+"/videoFiles")
        for file in filelist:
            #os.replace(file, os.path.join(tempPath + "/" + os.path.basename(file)))
            os.replace(file, outputFilePath+"/videoFiles/"+os.path.basename(file))

    # Deletes everything from the temporary folder
    # This has been replaced by copying the files to a folder in the output folder
    def deleteFromTemp():
        filelist = glob.glob(os.path.join(tempPath, "*"))
        for file in filelist:
            os.remove(file)

    # Method to upload a file to sciebo with a given username and password
    def uploadToSciebo(*values):
        # Debug - Password! Careful not to show
        # print(values)
        if(values[0] == "" or values[1] == "" or values[2] == ""):
            messagebox.showerror("Error", "Bitte geben sie Nutzername, Passwort und Dateiname an!!")
        else:
            sciebo = owncloud.Client('https://th-koeln.sciebo.de')
            sciebo.login(values[0], values[1])

            # Get the list of directories
            # This does not do anything yet, maybe later TODO: add a way to create a folder, if it does not exist, and upload to there
            dirList = sciebo.list("/")

            # If the upload is successfull, close the window. TODO: Do something when it is not successfull (maybe print an error?)
            if(sciebo.put_file(str(values[2]) + ".mkv", values[4] + "/output.mkv")):
                values[3].destroy()

    # PopUp window for entering sciebo account information and file title
    def uploadPopup(outputFilePath):
        window = Toplevel()
        window.title("Upload")
        window.configure(background=bgColor)

        # A lot of GUI stuff, asking for password, username and filename. Password is a censored field.
        # maybe TODO: Toggle for show password

        # Row 0
        label_username = Label(window, text="Nutzername:", fg=fgColor, bg=bgColor)
        label_username.grid(column=0, row=0, padx=5, pady=5)

        entry_username = Entry(window, width=30)
        entry_username.grid(column=1, row=0, padx=5, pady=5)
        
        # Row 1
        label_password = Label(window, text="Passwort:", fg=fgColor, bg=bgColor)
        label_password.grid(column=0, row=1, padx=5, pady=5)

        entry_password = Entry(window, show="*", width=30)
        entry_password.grid(column=1, row=1, padx=5, pady=5)

        # Row 2
        label_filename = Label(window, text="Dateiname:", fg=fgColor, bg=bgColor)
        label_filename.grid(column=0, row=2, padx=5, pady=5)

        entry_filename = Entry(window, width=30)
        entry_filename.grid(column=1, row=2, padx=5, pady=5)

        # Row 3
        label_hintUpload = Label(window, text="Die Datei wird zum Hauptverzeichnis Ihres Sciebo Accounts hochgeladen, mit dem Dateinamen den Sie angegeben haben.", fg=fgColor, bg=bgColor)
        label_hintUpload.grid(row=3, columnspan=2, padx=5, pady=5)

        # Row 4
        label_hintUpload = Label(window, text="", bg=bgColor)
        label_hintUpload.grid(row=4, columnspan=2, padx=5, pady=5)

        # Row 5
        button_loginSciebo = Button(window, text="Upload", command=lambda: VideoCabin2.uploadToSciebo(entry_username.get(), entry_password.get(), entry_filename.get(), window, outputFilePath), bg=btnColor, fg=fgColor)
        button_loginSciebo.grid(column=1, row=5, pady=5, padx=5)

        button_cancel = Button(window, text="Cancel", command= lambda: window.destroy(), bg=btnColor, fg=fgColor)
        button_cancel.grid(column=0, row=5, pady=5, padx=5)

        window.mainloop()

    # Copy output file to connected USB flash drive. For now, the drive must be specified beforehand -> This should be ok, since it should not change on the computer the script runs on
    def copyToDrive(outputFilePath):
        # TODO: Find path? Prompt user to find path?
        drivePath = "G:"
        copyfile(outputFilePath+"/output.mkv",drivePath+"/output.mkv")

    # Open the directory with the output file
    def openOutputDir(outputFilePath):
        os.startfile(outputFilePath)

    # Window for uploading and/or copying the file to a hard drive
    def upload(outputFilePath):
        #deleteFromTemp()
        VideoCabin2.moveToTemp(outputFilePath)

        windowNew = Tk()
        windowNew.title("Video Cabin Merger - Upload")
        windowNew.attributes('-fullscreen', True)
        windowNew.configure(background=bgColor)

        txtFont = ("Helvetica",20)

        # Buttons for upload, copying and showing in explorer
        button_upload = Button(text="Dateiupload zu Ihrem Sciebo Account @sciebo.th-koeln.de", command= lambda: VideoCabin2.uploadPopup(outputFilePath), font=txtFont, bg=btnColor, fg=fgColor).grid(column=0, row=0, padx=20, pady=15)
        button_copyToDrive = Button(text="Ausgabedatei auf einen angeschlossenen USB Stick kopieren", command= lambda: VideoCabin2.copyToDrive(outputFilePath), font=txtFont, bg=btnColor, fg=fgColor).grid(column=0, row=1, padx=20,pady=15)
        button_showInExplorer = Button(text="Ausgabedatei im Explorer anzeigen", font=txtFont,command= lambda: VideoCabin2.openOutputDir(outputFilePath), bg=btnColor, fg=fgColor).grid(column=0,row=2, pady=15, padx=20)
        button_deleteEverything = Button(text="Videodateien und zusammengeführtes Video löschen", command= lambda: VideoCabin2.deleteEverythingCheck(windowNew), font=txtFont, bg="red", fg=fgColor).grid(column=0, row=3, padx=15, pady=30)

        # Exit button
        button_exit = Button(text="Beenden", command= lambda: windowNew.destroy(), font=txtFont, bg=btnColor, fg=fgColor).grid(column=0, row=4, pady=40)

        windowNew.mainloop()

    def deleteEverythingCheck(windowOld):
        deleteWindow = Toplevel(windowOld)
        deleteWindow.geometry(str(960) + "x" + str(520) + "+" +  str(480) + "+" + str(270))
        deleteWindow.configure(background=bgColor)
        txtFont = ("Helvetica",20)

        label_areYouSure = Label(deleteWindow, text="Alle Dateien werden permanent von diesem Computer gelöscht. Bitte stellen Sie sicher, dass Sie Ihre Daten exportiert haben.", wraplength=800, font=txtFont, bg=bgColor, fg=fgColor).grid(column=0, row=0, pady=15)
        label_areYouSure2 = Label(deleteWindow, text="Sind Sie sicher, dass Sie alle Dateien löschen wollen?", font=txtFont, wraplength=800, bg=bgColor, fg=fgColor).grid(column=0, row=1, pady=15)

        btn_confirm = Button(deleteWindow, text="Löschen", font=txtFont, bg="red", fg=fgColor, command= lambda: VideoCabin2.deleteEverything(deleteWindow)).grid(column=0, row=2, padx=5, pady=20)
        btn_cancel = Button(deleteWindow, text="Abbrechen", font=txtFont, bg=btnColor, fg=fgColor, command= lambda: VideoCabin2.cancelDeleteEverything(deleteWindow)).grid(column=0, row=3, padx=5, pady=20)

    def deleteEverything(windowOld):
        shutil.rmtree(outputFilePath)
        windowOld.destroy()

    def cancelDeleteEverything(windowOld):
        windowOld.destroy()

    # Simple messagebox asking if the user is sure they want to continue
    def areYouSure(windowOld, outputFilePath):
        result = msgBox = messagebox.askokcancel("Weiter", "Sind Sie sicher?", icon='warning')
        if result == True:
            windowOld.destroy()
            VideoCabin2.upload(outputFilePath)

    # Method to start the merge process. To prevent freezing the GUI and allowing an information about the process, it has been moved to another thread.
    def startMergeThread(windowOld, i_row, frame):
        txtFont = ("Helvetica",20)
        windowMergeInProgress = Toplevel(windowOld)
        windowMergeInProgress.geometry("800" + "x" + "400" + "+" + "600" + "+" + "250")
        windowMergeInProgress.grab_set()
        windowMergeInProgress.attributes('-disabled', True)
        windowMergeInProgress.configure(background=bgColor)

        label_mergeInProgress = Label(windowMergeInProgress, text="Zusammenführen, bitte warten.", font=txtFont, fg=fgColor)
        label_mergeInProgress.place(in_=windowMergeInProgress, anchor="c", relx=.5, rely=.2)
        label_mergeInProgress.configure(background=bgColor)
        label_mergeInProgress2 = Label(windowMergeInProgress, text="Dies kann einige Minuten dauern.", font=txtFont, fg=fgColor)
        label_mergeInProgress2.place(in_=windowMergeInProgress, anchor="c", relx=.5, rely=.4)
        label_mergeInProgress2.configure(background=bgColor)

        threading.Thread(target= lambda: VideoCabin2.mergeFiles(windowOld, i_row, frame, windowMergeInProgress)).start()

    # Method for merging files. From the list of files to merge, a new list is created with the durations of the video files. Then, a ffmpeg command is created and executed via console.
    def mergeFiles(windowOld, i_row, frame, windowPopup):
        txtFont = ("Helvetica",20)

        # Creates a unique output folder
        outputFilePath = VideoCabin2.createOutputFolder()

        # Get the durations of the different video files, important for fades between
        files_durations = []
        for file in filesToUse:
            cmd = ['ffprobe', '-i', file, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=%s' % ("p=0")]
            duration = subprocess.check_output(cmd)
            # TODO: Test this for larger values to check if conversion to float still works
            # Append duration to a new list for durations
            files_durations.append(float(duration))

        # Debug
        # print(files_durations)

        # Create string array for the cmd command
        cmd_merge = ['ffmpeg']
        cmd_merge.append('-y')
        # Every video is added via '-i <File>'
        for file in filesToUse:
            cmd_merge.append('-i')
            cmd_merge.append(file)

        # After the videos are all added, enter the complex filter setting for fades between
        cmd_merge.append('-filter_complex')

        # counter for the following loop
        i = int(0)

        complexFilterString = ""
        complexFilterString2 = ""

        # Complex filter settings is a very long argument, therefore the string is created piece by piece
        # duration of "fade type in" specifies the fade in duration at the start and between clips, only duration is required
        # duration of "fade type out" specifies the fade out duration, but also requires an offset, which is calculated by the length of the clip
        # this needs to be done for every clip that is used
        # TODO: Optionally, ffmpeg's xfades can be used for fades inbetween, this offers a wieder variety of animations, maybe let the user could choose the animation via dropdown -> still artifacts, no idea why
        for file in filesToUse:
            complexFilterString += "[" + str(i) + ":v]fade=type=in:duration=0.5,fade=type=out:duration=0.5:start_time=" + str(files_durations[i]-0.5) + ",setpts=PTS-STARTPTS[v" + str(i) + "]; "
            complexFilterString2 += "[v" + str(i) + "][" + str(i) + ":a]"
            i += 1

        complexFilterString2 += "concat=n=" + str(len(filesToUse)) + ":v=1:a=1[v][a]"
        complexFilterString += complexFilterString2

        cmd_merge.append(complexFilterString)

        cmd_merge.append("-map")
        cmd_merge.append("[v]")
        cmd_merge.append("-map")
        cmd_merge.append("[a]")

        cmd_merge.append(outputFilePath + "\\output.mkv")

        # Debug
        #print(cmd_merge)
        #for cmd in cmd_merge:
            #print(cmd)

        # check_call() instead of run() freezes the application until the subprocess is finished - perhaps not perfect, but it stops the user from interrupting the process
        # TODO: ENABLE AGAIN!!
        subprocess.check_call(cmd_merge)

        #mergingInProgressPopup.destroy()

        #messagebox.showinfo("Fertig", "Zusammenführen beendet!")

        windowPopup.destroy()

        button_playOutput = Button(frame, text="Zusammengeführte Datei abspielen", command= lambda: VideoCabin2.playVideo(outputFilePath+"/output.mkv"), font=txtFont, bg=btnColor, fg=fgColor)
        button_playOutput.grid(column=0, row=2, pady=10, padx=10)

        button_continue = Button(frame, text="Weiter", font=txtFont, command= lambda: VideoCabin2.areYouSure(windowOld, outputFilePath), bg=btnColor, fg=fgColor)
        button_continue.grid(column=0,row=3, pady=20)

        frame_text = Frame(windowOld)
        frame_text.grid(column=0, row=4)
        frame_text.configure(background=bgColor)

        label_instruction = Label(frame_text, text="Wenn Sie unzufrieden mit dem Ergebnis sind, können Sie die Dateien erneut zusammenführen. Wenn nicht, drücken Sie auf \"Weiter\".", font=txtFont, fg=fgColor)
        label_instruction.grid(columnspan=5, row=0)
        label_instruction.configure(background=bgColor)
        label_warning = Label(frame_text, text="Bitte beachten Sie, dass Sie nicht zu dieser Ansicht zurückkehren können!", font=txtFont, fg="Red")
        label_warning.grid(columnspan=5, row=1)
        label_warning.configure(background=bgColor)


    # Window for selecting the video files
    def videoFileSelectionWindow(window_old):
        # This was previously needed to destroy the first window, since this is now the starting window, it must be disabled
        #window_old.destroy()

        global frameCounter
        global filesInFrameCounter
        global pageCounter
        global frames

        windowNew = Tk()
        windowNew.title("Video Cabin Merge Manager - File Selection")
        windowNew.attributes('-fullscreen', True)

        windowNew.configure(background=bgColor)

        i = 0
        i_row = 0
        i_col = 0

        txtFont = ("Helvetica",18)

        # Create 10 frames for video files, for a maximum storage of 120 video files
        # Hide all frames but the first one
        frame_videoFiles0 = Frame(windowNew)
        frame_videoFiles0.grid(column=0, row=0)
        #frame_videoFiles0.grid_forget()

        frame_videoFiles1 = Frame(windowNew)
        frame_videoFiles1.grid(column=0, row=0)
        frame_videoFiles1.grid_forget()

        frame_videoFiles2 = Frame(windowNew)
        frame_videoFiles2.grid(column=0, row=0)
        frame_videoFiles1.grid_forget()

        frame_videoFiles3 = Frame(windowNew)
        frame_videoFiles3.grid(column=0, row=0)
        frame_videoFiles1.grid_forget()

        frame_videoFiles4 = Frame(windowNew)
        frame_videoFiles4.grid(column=0, row=0)
        frame_videoFiles1.grid_forget()

        frame_videoFiles5 = Frame(windowNew)
        frame_videoFiles5.grid(column=0, row=0)
        frame_videoFiles1.grid_forget()

        frame_videoFiles6 = Frame(windowNew)
        frame_videoFiles6.grid(column=0, row=0)
        frame_videoFiles1.grid_forget()

        frame_videoFiles7 = Frame(windowNew)
        frame_videoFiles7.grid(column=0, row=0)
        frame_videoFiles1.grid_forget()

        frame_videoFiles8 = Frame(windowNew)
        frame_videoFiles8.grid(column=0, row=0)
        frame_videoFiles1.grid_forget()

        frame_videoFiles9 = Frame(windowNew)
        frame_videoFiles9.grid(column=0, row=0)
        frame_videoFiles1.grid_forget()

        #frameCounter = 0
        #filesInFrameCounter = 0
        #pageCounter = 0

        frames = {0: frame_videoFiles0,
                  1: frame_videoFiles1,
                  2: frame_videoFiles2,
                  3: frame_videoFiles3,
                  4: frame_videoFiles4,
                  5: frame_videoFiles5,
                  6: frame_videoFiles6,
                  7: frame_videoFiles7,
                  8: frame_videoFiles8,
                  9: frame_videoFiles9 }

        # Create a title, buttons and checkbox for every video
        for file in files:
            filesInFrameCounter += 1

            # One frame object contains the name of the clip, a button to view the clip (for example in VLC) and a button to add or remove a clip from the list of clips
            frame = Frame(frames[frameCounter], borderwidth=1, relief="solid", highlightbackground=fgColor, highlightcolor=fgColor, highlightthickness=1)
            frame.grid(column=i_col, row=i_row)

            frame.configure(background=bgColor)

            label_fileName = Label(frame, text=os.path.basename(file), font=txtFont)
            label_fileName.grid(column=0, row=0, padx=5, pady=5)

            label_fileName.configure(background=bgColor, fg=fgColor)

            # Play button starts playing the file
            playButton = Button(frame, text="Vorschau", command= lambda file=file: VideoCabin2.playVideo(file), font=txtFont, bg=btnColor, fg=fgColor)
            playButton.grid(column=0, row=1, padx=5, pady=5)

            # Use Button is green by default, all files are added to the list. Pressing the button makes it turn red, the file is deleted from the list
            # Pressing the button again turns it green again, the file is again added, always in the same order (hopefully?) TODO: Test this
            useButton = Button(frame, text="Benutzen", bg="green", fg="white", command= lambda file=file, i=i: VideoCabin2.unuseFile(file,i), font=txtFont)
            useButton.grid(column=0, row=2, padx=5,pady=5)

            trimMenuButton = Button(frame, text="Zuschneiden", command= lambda file=file, i=i: VideoCabin2.trimVideoFileWindow(file,i,windowNew), font=txtFont, bg=btnColor, fg=fgColor)
            trimMenuButton.grid(column=0, row=3, padx=5,pady=5)

            deleteFileButton = Button(frame, text="Löschen", command= lambda file=file, i=i: VideoCabin2.deleteVideoFile(file, windowNew), font=txtFont, bg=btnColor, fg=fgColor)
            deleteFileButton.grid(column=0, row=4, padx=5, pady=5)

            # Since everything is dynamic, row and column numbers need to count up like this
            i += 1
            i_col += 1
            # Change the value x for 'i_col == x' for the amount of objects in one row, for example x=3 means 3 objects per row
            if(i_col == 6):
                i_row += 2
                i_col = 0

            filesToUse.append(file)
            useButtons.append(useButton)

            if(filesInFrameCounter == 12):
                filesInFrameCounter = 0
                frameCounter += 1

        # Values for space between the video cards
        #windowNew.columnconfigure((0,i_col),pad=0)
        #windowNew.rowconfigure((0,i_row),pad=0)

        frame_forwardAndBackward = Frame(windowNew)
        frame_forwardAndBackward.grid(column=0, row=1)
        frame_forwardAndBackward.configure(background=bgColor)

        # frameCounter: The total amount of frames created, 12 video files per frame, default 1 frame (framecounter = 0). For example, 23 video files will create 3 frames
        # pageCounter: The page we are currently on. If <= 12 files, only one page.
        label_page = Label(frame_forwardAndBackward, text="Seite " + str(pageCounter+1))
        label_page.grid(column=1, row=0, padx=5, pady=10)
        label_page.configure(background=bgColor, fg=fgColor)

        def forward(label):
            global pageCounter
            global frameCounter
            global frames
            pageCounter += 1
            if(pageCounter <= frameCounter):
                print("forward yes")
                frames[pageCounter-1].grid_forget()
                frames[pageCounter].grid(column=0, row=0)
                # Since we are counting up from 0, we have to add 1 to start with page 1
                label.config(text="Seite " + str(pageCounter+1))
            else:
                pageCounter -= 1

        def backward(label):
            global pageCounter
            global frameCounter
            global frames
            pageCounter -= 1
            if(pageCounter >= 0):
                print("backward yes")
                frames[pageCounter+1].grid_forget()
                frames[pageCounter].grid(column=0, row=0)
                label.config(text="Seite " + str(pageCounter+1))
            else:
                pageCounter += 1

        if(frameCounter > 0):
            button_back = Button(frame_forwardAndBackward, text="<", font=txtFont, command= lambda: backward(label_page), bg=btnColor, fg=fgColor)
            button_back.grid(column=0, row=0, padx=5, pady=10)
            button_forward = Button(frame_forwardAndBackward, text=">", font=txtFont, command= lambda: forward(label_page), bg=btnColor, fg=fgColor)
            button_forward.grid(column=2, row=0, padx=5, pady=10)

        frame_mergeButton = Frame(windowNew)
        frame_mergeButton.grid(column=0, row=2)
        frame_mergeButton.configure(background=bgColor)

        mergeButton = Button(frame_mergeButton, text="Zusammenführen", command= lambda: VideoCabin2.startMergeThread(windowNew, i_row, frame_mergeButton), font=txtFont, bg=btnColor, fg=fgColor)
        mergeButton.grid(column = 0, row = 0, pady=20,padx=5)

        backButton = Button(frame_mergeButton, text="Zurück zur Anleitung", font=txtFont, command= lambda: VideoCabin2.backToInstructions(windowNew), bg=btnColor, fg=fgColor)
        backButton.grid(column = 0, row = 1, pady=20, padx=5)

        windowNew.mainloop()

    def deleteVideoFile(file, windowOld):
        areYouSureWindow = Toplevel(windowOld)
        areYouSureWindow.geometry("800" + "x" + "400" + "+" + "600" + "+" + "250")
        areYouSureWindow.grab_set()
        areYouSureWindow.configure(background=bgColor)

        textFont = ("Helvetica",28)

        label_areYouSure = Label(areYouSureWindow, text="Sind Sie sicher dass Sie das Video löschen möchten?", font=textFont, wraplength=700, fg=fgColor)
        label_areYouSure.place(in_=areYouSureWindow, anchor="c", relx=.5, rely=.2)
        label_areYouSure.configure(background=bgColor)
        
        buttonFrame = Frame(areYouSureWindow, bg=bgColor)
        buttonFrame.place(in_=areYouSureWindow, anchor="c", relx=.5, rely=.6)
        button_cancel = Button(buttonFrame, text="Löschen", font=textFont, bg=btnColor, fg=fgColor, command= lambda: VideoCabin2.deleteConfirmed(file, windowOld, areYouSureWindow)).grid(row=0, padx=10, pady=10)
        button_delete = Button(buttonFrame, text="Abbrechen", font=textFont, bg=btnColor, fg=fgColor, command= lambda: areYouSureWindow.destroy()).grid(row=1, padx=10, pady=10)

    def deleteConfirmed(file, windowOld, youSureWindow):
        os.remove(file)
        youSureWindow.destroy()
        windowOld.destroy()
        os.system("python D:/GitHub/VideoCabinPython/VideoCabin2.py")

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

    def trimCancel(windowOld, file):
        # Check if a trim file has been created and if yes, delete it, then close the window
        if(os.path.isfile(os.path.dirname(file)+"/TRIM_"+os.path.basename(file))):
            os.remove(os.path.dirname(file)+"/TRIM_"+os.path.basename(file))
        windowOld.destroy()

    def trimApply(windowOld, file):
        # To be sure, check for the file
        if(os.path.isfile(os.path.dirname(file)+"/TRIM_"+os.path.basename(file))):
            # If it is there, remove the old file and rename the new file
            os.rename(file, os.path.dirname(file)+"/UNTRIMMED_"+os.path.basename(file))
            os.rename(os.path.dirname(file)+"/TRIM_"+os.path.basename(file), file)

        windowOld.destroy()

    def trimVideoFileWindow(file, i, windowOld):
        trimWindow = Toplevel(windowOld)
        trimWindow.geometry(str(960) + "x" + str(520) + "+" +  str(480) + "+" + str(270))
        trimWindow.configure(background=bgColor)

        txtFont = ("Helvetica",20)

        # Let the user only interact with this window, as long as it is open
        trimWindow.grab_set()

        frame2 = Frame(trimWindow, borderwidth=1)
        frame2.configure(background=bgColor)
     
        frame2.place(in_=trimWindow, anchor="c", relx=.5, rely=.1)
        playButton = Button(frame2, text="Vorschau", command= lambda: VideoCabin2.playVideo(file), font=txtFont, bg=btnColor, fg=fgColor)
        playButton.grid(column=1, row=0, padx=5,pady=5)

        frame3 = Frame(trimWindow, borderwidth=1)
        frame3.place(in_=trimWindow, anchor="c", relx=.5, rely=.3)
        frame3.configure(background=bgColor)

        duration = StringVar(trimWindow)
        spinbox = Spinbox(frame3, from_=0, to = 10, width=3, font=('Helvetica', 40), textvariable=duration)
        spinbox.grid(column=0, row=0)
        spinbox.configure(background=bgColor, fg=fgColor)

        frame4 = Frame(trimWindow, borderwidth=1)
        frame4.place(in_=trimWindow, anchor="c", relx=.5, rely=.4)
        label_trimTimeText = Label(frame4, text="Sekunden am Ende des Videos abschneiden", font=txtFont)
        label_trimTimeText.grid(column=1, row=2)
        label_trimTimeText.configure(background=bgColor, fg=fgColor)
        frame4.configure(background=bgColor)

        frame6 = Frame(trimWindow, borderwidth=1)
        frame6.place(in_=trimWindow, anchor="c", relx=.5, rely=.65)
        button_previewTrim = Button(frame6, text="Vorschau zugeschnittenes Video", font=txtFont, bg=btnColor, fg=fgColor, state=DISABLED, command= lambda: VideoCabin2.playVideo(os.path.dirname(file)+"/TRIM_"+os.path.basename(file)))
        button_previewTrim.grid(column=0, row=0)
        frame6.configure(background=bgColor)

        frame7 = Frame(trimWindow, borderwidth=1)
        frame7.place(in_=trimWindow, anchor="c", relx=.5, rely=.8)
        button_accept = Button(frame7, text="Zuschneiden bestätigen", state=DISABLED, font=txtFont, command= lambda: VideoCabin2.trimApply(trimWindow, file), bg=btnColor, fg=fgColor)
        button_accept.grid(column=0, row=0, padx=5)
        button_cancel = Button(frame7, text="Abbrechen", font=txtFont, command= lambda: VideoCabin2.trimCancel(trimWindow, file), bg=btnColor, fg=fgColor)
        button_cancel.grid(column=1, row=0, padx=5)
        frame7.configure(background=bgColor)

        frame5 = Frame(trimWindow, borderwidth=1)
        frame5.place(in_=trimWindow, anchor="c", relx=.5, rely=.5)
        button_trim = Button(frame5, text="Zuschneiden", font=txtFont, command= lambda: VideoCabin2.trimVideoFile(file, duration.get(), button_previewTrim, button_accept), bg=btnColor, fg=fgColor)
        button_trim.grid(column=0, row=0)
        frame5.configure(background=bgColor)



    # This has been disabled
    def introWindow():
        # Set GUI window start settings
        window = Tk()
        window.title("Video Cabin Merge Manager - Start")

        # Row 1
        label_videoFiles = Label(window, text=str(len(files)) + " video files found.")
        label_videoFiles.grid(column=0, row=1, padx=5, pady=5)

        # Row 0
        label_directory = Label(window, text="Your directory: " + path)
        label_directory.grid(column=0, row=0, padx=5, pady=5)

        button_changeDirectory = Button(window, text="Change directory", command= lambda: VideoCabin2.getFolderPath(label_directory, label_videoFiles))
        button_changeDirectory.grid(column=1, row=0, padx=5, pady=5)

        button_resetDirectory = Button(window, text="Reset directory", command= lambda: VideoCabin2.setInitialPath(label_directory, label_videoFiles))
        button_resetDirectory.grid(column=2, row=0, padx=5, pady=5)

        # Row 2
        button_next = Button(window, text="Continue", command= lambda: VideoCabin2.videoFileSelectionWindow(window))
        button_next.grid(column=0, row=2, padx=5, pady=5)

        window.mainloop()

# Only start the main routine if more than one file is present in the video file directory
if(len(files) > 1):
    VideoCabin2.videoFileSelectionWindow(None)
else:
    # And do not do anything if there are no files
    # TODO: Maybe an error?
    if(len(files) > 0):
        # If there is one file, rename it and move it to the output folder
        # Create a uniquie output folder with time and date
        outputFilePath = VideoCabin2.createOutputFolder()

        # Move the single video file to that folder and rename it to output
        # TODO: Fade in/out?
        os.replace(files[0],outputFilePath+"/output.mkv")

        # Open the export window
        VideoCabin2.upload(outputFilePath)
    else:
        # Error message if no video files are found in the folder
        window = Tk()
        window.withdraw()
        messagebox.showerror("Error", "Keine Videodateien gefunden!")