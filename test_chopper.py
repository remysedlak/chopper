# Tkiner, the basic framework
from tkinter import *
# ttkbootstrap, the theme library
import ttkbootstrap as tb
# Import our python app with the audio logic
import audio_manipulation as am
# Import the filedialog to open files
from tkinter import filedialog

# Method to retrieve user file and send file to AM
def openfile():
    # Open the windows file dialog
    filepath = filedialog.askopenfile()
    # Python opens the file
    file = open(filepath.name, "r")
    # Audio manipulation methods
    am.print_file_path(filepath.name)
    am.amplitude_envelope(filepath.name)

    ## Python closes the File
    file.close()
    ## Update the view to show the uploaded file path
    label.configure(text="file path: " + filepath.name)

# Setting the theme of the window and size
root = tb.Window(themename="solar")
root.title("Test Chopper")
root.geometry("720x720")

# Create a label widget
# text is the text to be shown, bootstyle is the tb style
# there is also an second option for an attribute
# primary, inverse or primary, outline
label = tb.Label(text="No Break Selected", bootstyle="primary")
label.pack(padx=5, pady=5)

# Upload button
button = tb.Button(root, text="Open File", 
    bootstyle="primary", command=openfile)

button.pack(fill="x", padx=5, pady=5)
# Start the app
root.mainloop()
