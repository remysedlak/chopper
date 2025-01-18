import ttkbootstrap as tb
import audio_manipulation as am
from tkinter import filedialog, Tk, Frame, TOP, BOTH, Label
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Method to retrieve user file and send file to AM
def openfile():
    filepath = filedialog.askopenfile() # Open the windows file dialog
    if filepath:
        file = open(filepath.name, "r") # Python opens the file

        am.print_file_path(filepath.name) #print filepath
        song, sr = am.find_sample_duration(filepath.name) # Get amplitude envelope information

        # Update the view to show the uploaded file path
        label.configure(text="file path: " + filepath.name)

        # Create the plot
        fig = am.plot_creation(song, sr)

        # Embed the plot in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1, padx=5, pady=5)

        # Python closes the File
        file.close()

# Setting the theme of the window and size
root = tb.Window(themename="solar")
root.title("Audio Manipulation")
root.geometry("800x800")

# Create a frame for the plot
frame = Frame(root)
frame.pack(side=TOP, fill=BOTH, expand=1)

# Label to show the file path
label = Label(root, text="No file selected")
label.pack(side=TOP, fill=BOTH, expand=1)

# Upload button
button = tb.Button(root, text="Open File", bootstyle="primary", command=openfile)
button.pack(fill="x", padx=5, pady=5)

# Start the app
root.mainloop()