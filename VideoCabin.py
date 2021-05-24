from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import *
import sys
import glob
import subprocess
import owncloud
import os

# Path needs to be called correctly when the script is started via command line (e.g. cmd 'python MergeManager.py C:/Users/Username/OBSVideos')
path = str(sys.argv[1])
initialPath = path
files = glob.glob(path + "/*.mkv")
files_durations = []
outputFile = None

# Set GUI window start settings
window = Tk()
#window.geometry('600x300')
window.title("Video Cabin Merge Manager")

# Function for changing the working directory
def getFolderPath():
    path = filedialog.askdirectory()
    # Change the label text after selecting a new directory
    label_welcome.config(text="Your directory: " + path)
    getVideoFilesInPath(path)

# Reset directory to initial path
def setInitialPath():
    path = initialPath
    label_welcome.config(text="Your directory: " + path)
    getVideoFilesInPath(path)

# Get all mkv files in the specified path and refresh info label
def getVideoFilesInPath(newpath):
    # Get files as an array, every entry is one complete path to the video file
    files = glob.glob(newpath + "/*.mkv")
    # Refresh label in the GUI
    label_filesFound.config(text=str(len(files)) + " video files found.")
    
    # Disable the merge button if no files are found
    # TODO: What to do when length = 1?
    if(len(files) == 0):
        button_merge.config(state="disabled")
    else:
        button_merge.config(state="normal") 

# Combine video files into one file
def mergeVideoFiles():
    # Get the durations of the different video files, important for fades between
    for file in files:
        cmd = ['ffprobe', '-i', file, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=%s' % ("p=0")]
        duration = subprocess.check_output(cmd)
        # TODO: Test this for larger values to check if conversion to float still works
        # Append duration to a new list for durations
        files_durations.append(float(duration))

    # Create string array for the cmd command
    cmd_merge = ['ffmpeg']
    # Every video is added via '-i <File>'
    for file in files:
        cmd_merge.append('-i')
        cmd_merge.append(file)

    # After the videos are all added, enter the complex filter setting for fades between
    cmd_merge.append('-filter_complex')

    # counter for the following loop
    i = int(0)

    complexFilterString = ""
    complexFilterString2 = ""

    # Complex filter settings is one long array entry, therefore the string is created piece by piece
    for file in files:
        complexFilterString += "[" + str(i) + ":v]fade=type=out:duration=0.5:start_time=" + str(files_durations[i]-0.5) + ",setpts=PTS-STARTPTS[v" + str(i) + "]; "
        complexFilterString2 += "[v" + str(i) + "][" + str(i) + ":a]"
        i += 1

    complexFilterString2 += "concat=n=" + str(len(files)) + ":v=1:a=1[v][a]"
    complexFilterString += complexFilterString2

    cmd_merge.append(complexFilterString)

    cmd_merge.append("-map")
    cmd_merge.append("[v]")
    cmd_merge.append("-map")
    cmd_merge.append("[a]")
    cmd_merge.append(path + "\\output.mkv")

    # Debug
    print(cmd_merge)

    subprocess.run(cmd_merge)

def uploadToSciebo(*values):
    # Debug - Password! Careful not to show
    # print(values)

    if(values[0] == "" or values[1] == "" or values[2] == ""):
        messagebox.showerror("Error", "Please enter username, password and file name!")
    else:
        sciebo = owncloud.Client('https://th-koeln.sciebo.de')
        sciebo.login(values[0], values[1])

        sciebo.put_file(str(values[2]) + ".mkv", path + "/output.mkv")


def uploadToScieboNewwindow():
    if(os.path.isfile(path + "/output.mkv")):
        scieboWindow = Toplevel(window)
        scieboWindow.title("Sciebo Upload")
        scieboWindow.geometry("300x200")

        # Row 0
        label_username = Label(scieboWindow, text="Username:")
        label_username.grid(column=0, row=0, padx=5, pady=5)

        entry_username = Entry(scieboWindow, width=30)
        entry_username.grid(column=1, row=0, padx=5, pady=5)
        
        # Row 1
        label_password = Label(scieboWindow, text="Password:")
        label_password.grid(column=0, row=1, padx=5, pady=5)

        entry_password = Entry(scieboWindow, show="*", width=30)
        entry_password.grid(column=1, row=1, padx=5, pady=5)

        # Row 2
        label_filename = Label(scieboWindow, text="File name:")
        label_filename.grid(column=0, row=2, padx=5, pady=5)

        entry_filename = Entry(scieboWindow, width=30)
        entry_filename.grid(column=1, row=2, padx=5, pady=5)

        # Row 3
        button_loginSciebo = Button(scieboWindow, text="Upload", command=lambda: uploadToSciebo(entry_username.get(), entry_password.get(), entry_filename.get()))
        button_loginSciebo.grid(column=1, row=3, pady=5, padx=5)
    else:
        # TODO: Here, again, what to do with only one video file?
        messagebox.showerror("No File found", "No output video file could be found. Did you merge your files?")

# https://gist.github.com/oldo/dc7ee7f28851922cca09
# Propably don't need that anymore

# ========================================== Setting up GUI elements ==========================================

# Row 0:
label_welcome = Label(window, text="Your directory: " + path)
label_welcome.grid(column=0, row=0, padx=5, pady=5)

button_changeDirectory = Button(window, text="Change directory", command=getFolderPath)
button_changeDirectory.grid(column=1, row=0, padx=5, pady=5)

button_resetDirectory = Button(window, text="Reset directory", command=setInitialPath)
button_resetDirectory.grid(column=2, row=0, padx=5, pady=5)

# Row 1:
label_filesFound = Label(window, text=str(len(files)) + " video files found")
label_filesFound.grid(column=0, row=1, padx=5, pady=5)

# Row 2:
button_merge = Button(window, text="Combine your video files", command=mergeVideoFiles)
button_merge.grid(column=0, row=2, padx=5, pady=5)

label_timeWarning = Label(window, text="(This may take a while)")
label_timeWarning.grid(column=1, row=2, padx=5, pady=5)

# Row 3:
label_row3 = Label(window, text="   \n   ")
label_row3.grid(column=0, row=3, padx=5, pady=20)

# Row 4:
button_upload = Button(window, text="Upload to your Sciebo Account", command=uploadToScieboNewwindow)
button_upload.grid(column=0, row=3, padx=5, pady=5)

# ========================================== End of GUI elements ==============================================


window.grid_columnconfigure(0, minsize=200)
window.mainloop()