# Tkiner, the basic framework
from tkinter import *
# ttkbootstrap, the theme library
import ttkbootstrap as tb
# Import our python app with the audio logic
import audio_manipulation as am
# Import the filedialog to open files
from tkinter import filedialog

def openfile():
    filepath = filedialog.askopenfile()
    file = open(filepath.name, "r")
    print(file.read())
    file.close()

# Just a random counter to display text logic
counter = 0
def change_counter():
    # counter needs to be global in order to be accessed in py
    global counter
    counter += 1
    label.config(text=counter)

# Setting the theme of the window and size
root = tb.Window(themename="solar")
root.title("Test Chopper")
root.geometry("720x720")

# Create a label widget
# text is the text to be shown, bootstyle is the tb style
# there is also an second option for an attribute
# primary, inverse or primary, outline
label = tb.Label(text="Hello, World!", bootstyle="primary")
label.pack(padx=5, pady=5)

# Button Widget 
b1 = tb.Button(root, text="Button 1", bootstyle="success, outline", 
    command=change_counter)

b1.pack(side=LEFT, padx=5, pady=10, fill="x")

button = tb.Button(root, text="Open File", 
    bootstyle="primary, outline", command=openfile)

button.pack()
# Start the app
root.mainloop()
