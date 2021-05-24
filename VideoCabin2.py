from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import sys
import glob
import subprocess
from typing import Collection
import owncloud
import os
import ctypes
from shutil import copyfile

# Path is the path selected at the moment, initialPath is always the path at the start of the application
path = str(sys.argv[1])
initialPath = path

# Get all files in the specified path when starting the script
files = glob.glob(path + "/*.mkv")

# Empty global list variables for later use
filesToUse = []
files_durations = []
useButtons = []

# Opens a file with the specified program, e.g. VLC
# TODO: Program path needs to be adjusted -> Maybe add a catch if the path does not exist, prompting the user to search for it?
def playVideo(file):
    # Debug
    # print(str(file))
    p = subprocess.Popen(["D:/Program Files/VideoLAN/VLC/vlc.exe", file])

# Method for changing the working directory
def getFolderPath(labelDirectory, labelVideoFiles):
    # Update path and label
    path = str(filedialog.askdirectory())
    labelDirectory.config(text="Your directory: " + path)
    # Update video file number label for new path
    files = glob.glob(path + "/*.mkv")
    labelVideoFiles.config(text=str(len(files)) + " video files found.")

# Method for resetting the directory to the one the script has been called with
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
    useButtons[i].config(text="Unused", bg="red", fg="white", command= lambda file=file, i=i: useFile(file,i))
    # Debug
    print(filesToUse)

# Add the video file to the list of files to use, change button to green and text on it to "used"
def useFile(file,i):
    filesToUse.append(file)
    useButtons[i].config(text="Used", bg="green", fg="white", command= lambda file=file, i=i: unuseFile(file,i))
    # Files are being sorted after every time they get added, so the original order is kept
    # TODO: Maybe add a way to let the user sort themselves? Could be complicated, especially on touchscreen
    filesToUse.sort()
    # Debug
    print(filesToUse)

# Method to upload a file to sciebo with a given username and password
def uploadToSciebo(*values):
    # Debug - Password! Careful not to show
    # print(values)
    if(values[0] == "" or values[1] == "" or values[2] == ""):
        messagebox.showerror("Error", "Please enter username, password and file name!")
    else:
        sciebo = owncloud.Client('https://th-koeln.sciebo.de')
        sciebo.login(values[0], values[1])

        # Get the list of directories
        # This does not do anything yet, maybe later TODO: add a way to create a folder, if it does not exist, and upload to there
        dirList = sciebo.list("/")

        # If the upload is successfull, close the window. TODO: Do something when it is not successfull (maybe print an error?)
        if(sciebo.put_file(str(values[2]) + ".mkv", path + "/output.mkv")):
            values[3].destroy()

# PopUp window for entering sciebo account information and file title
def uploadPopup():
    window = Toplevel()
    window.title("Upload")

    # A lot of GUI stuff, asking for password, username and filename. Password is a censored field.
    # maybe TODO: Toggle for show password

    # Row 0
    label_username = Label(window, text="Username:")
    label_username.grid(column=0, row=0, padx=5, pady=5)

    entry_username = Entry(window, width=30)
    entry_username.grid(column=1, row=0, padx=5, pady=5)
    
    # Row 1
    label_password = Label(window, text="Password:")
    label_password.grid(column=0, row=1, padx=5, pady=5)

    entry_password = Entry(window, show="*", width=30)
    entry_password.grid(column=1, row=1, padx=5, pady=5)

    # Row 2
    label_filename = Label(window, text="File name:")
    label_filename.grid(column=0, row=2, padx=5, pady=5)

    entry_filename = Entry(window, width=30)
    entry_filename.grid(column=1, row=2, padx=5, pady=5)

    # Row 3
    label_hintUpload = Label(window, text="The file will be uploaded to the root directory of your sciebo account with the file name you entered above.")
    label_hintUpload.grid(row=3, columnspan=2, padx=5, pady=5)

    # Row 4
    label_hintUpload = Label(window, text="")
    label_hintUpload.grid(row=4, columnspan=2, padx=5, pady=5)

    # Row 5
    button_loginSciebo = Button(window, text="Upload", command=lambda: uploadToSciebo(entry_username.get(), entry_password.get(), entry_filename.get(), window))
    button_loginSciebo.grid(column=1, row=5, pady=5, padx=5)

    button_cancel = Button(window, text="Cancel", command= lambda: window.destroy())
    button_cancel.grid(column=0, row=5, pady=5, padx=5)

    window.mainloop()

# Copy output file to connected USB flash drive. For now, the drive must be specified beforehand
def copyToDrive():
    # TODO: Find path? Prompt user to find path?
    drivePath = "E:"
    copyfile(path+"/output.mkv",drivePath+"/output.mkv")

# Open the directory with the output file
def openOutputDir():
    # TODO: Maybe copy the file to an output directory?
    os.startfile(path)

# Window for uploading and/or copying the file to a hard drive
def upload():
    windowNew = Tk()
    windowNew.title("Video Cabin Merger - Upload")

    # Buttons for upload, copying and showing in explorer
    button_upload = Button(text="Upload output file to your accoung @sciebo.th-koeln.de", command=uploadPopup).grid(column=0, row=0, padx=20, pady=15)
    button_copyToDrive = Button(text="Copy output file to connected USB flash drive", command=copyToDrive).grid(column=0, row=1, padx=20,pady=15)
    button_showInExplorer = Button(text="Show output file in explorer",command=openOutputDir).grid(column=0,row=2, pady=15, padx=20)

    windowNew.mainloop()

def mergeFiles(windowOld):
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
    # TODO: Optionally, ffmpeg's xfades can be used for fades inbetween, this offers a wieder variety of animations, maybe let the user could choose the animation via dropdown
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

    # TODO: If output path should be changed, do it here. Also create a new outputPath string variable with the information, to find it again later
    cmd_merge.append(path + "\\output.mkv")

    # Debug
    #print(cmd_merge)
    for cmd in cmd_merge:
        print(cmd)

    # check_call() instead of run() freezes the application until the subprocess is finished - perhaps not perfect, but it stops the user from interrupting the process
    #subprocess.run(cmd_merge)

    # TODO: ENABLE AGAIN!!
    #subprocess.check_call(cmd_merge)

    windowOld.destroy()
    upload()


# Window for selecting the video files
def videoFileSelectionWindow(window_old):
    window_old.destroy()
    
    windowNew = Tk()
    windowNew.title("Video Cabin Merge Manager - File Selection")

    i = 0
    i_row = 0
    i_col = 0

    # Create a title, buttons and checkbox for every video
    for file in files:
        # One frame object contains the name of the clip, a button to view the clip (for example in VLC) and a button to add or remove a clip from the list of clips
        # TODO: Frame formatting
        frame = Frame(windowNew, borderwidth=2, relief="solid")
        frame.grid(column=i_col, row=i_row)

        label_fileName = Label(frame, text=os.path.basename(file))
        label_fileName.grid(column=0, row=0, padx=5, pady=5)

        # Play button starts playing the file
        playButton = Button(frame, text="Play", command= lambda file=file: playVideo(file))
        playButton.grid(column=0, row=1, padx=5, pady=5)

        # Use Button is green by default, all files are added to the list. Pressing the button makes it turn red, the file is deleted from the list
        # Pressing the button again turns it green again, the file is again added, always in the same order (hopefully?) TODO: Test this
        useButton = Button(frame, text="Used", bg="green", fg="white", command= lambda file=file, i=i: unuseFile(file,i))
        useButton.grid(column=0, row=2, padx=5,pady=5)

        # Since everything is dynamic, row and column numbers need to count up like this
        i += 1
        i_col += 1
        # Change the value x for 'i_col == x' for the amount of objects in one row, for example x=3 means 3 objects per row
        if(i_col == 3):
            i_row += 2
            i_col = 0

        filesToUse.append(file)
        useButtons.append(useButton)

    # Values for space between the video cards
    windowNew.columnconfigure((0,i_col),pad=30)
    windowNew.rowconfigure((0,i_row),pad=30)

    mergeButton = Button(windowNew, text="Merge video files", command= lambda: mergeFiles(windowNew))
    # TODO: Change the following line to something less stupid
    mergeButton.grid(column = (int)((i_col+1)/2), row = i_row+1, pady=5,padx=5)

    windowNew.mainloop()

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

    button_changeDirectory = Button(window, text="Change directory", command= lambda: getFolderPath(label_directory, label_videoFiles))
    button_changeDirectory.grid(column=1, row=0, padx=5, pady=5)

    button_resetDirectory = Button(window, text="Reset directory", command= lambda: setInitialPath(label_directory, label_videoFiles))
    button_resetDirectory.grid(column=2, row=0, padx=5, pady=5)

    # Row 2
    button_next = Button(window, text="Continue", command= lambda: videoFileSelectionWindow(window))
    button_next.grid(column=0, row=2, padx=5, pady=5)

    window.mainloop()

introWindow()

# https://stackoverflow.com/questions/14910858/how-to-specify-where-a-tkinter-window-opens