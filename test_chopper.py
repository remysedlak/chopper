import ttkbootstrap as tb
import audio_manipulation as am
from tkinter import filedialog, Tk, Frame, Label
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Method to retrieve user file and send file to AM
def openfile():
    filepath = filedialog.askopenfile() # Open the windows file dialog
    if filepath:
        file = open(filepath.name, "r") # Python opens the file

        am.print_file_path(filepath.name) #print filepath
        song, sr = am.find_sample_duration(filepath.name) # Get amplitude envelope information

        # Update the view to show the uploaded file path
        label.configure(text="file path: " + filepath.name)

        # Create the amplitude envelope plot
        ae_fig = am.create_amplitude_envelope_plot(song, sr)
        ae_canvas = FigureCanvasTkAgg(ae_fig, master=frame)
        ae_canvas.draw()
        ae_canvas.get_tk_widget().grid(row=0, column=0, padx=5, pady=5)

        # Create the zero crossing rate plot
        fft_fig = am.create_frequency_plot(song, sr)
        fft_canvas = FigureCanvasTkAgg(fft_fig, master=frame)
        fft_canvas.draw()
        fft_canvas.get_tk_widget().grid(row=1, column=0, padx=5, pady=5)

        # Python closes the File
        file.close()

# Setting the theme of the window and size
root = tb.Window(themename="solar")
root.title("Audio Manipulation")
root.geometry("800x600")

# Configure grid layout
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# Create a frame for the plots
frame = Frame(root)
frame.grid(row=1, column=0, sticky="nsew")

# Configure grid layout for the frame
frame.grid_rowconfigure(0, weight=1)
frame.grid_rowconfigure(1, weight=1)
frame.grid_columnconfigure(0, weight=1)

# Label to show the file path
label = Label(root, text="No file selected")
label.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

# Upload button
button = tb.Button(root, text="Open File", bootstyle="primary", command=openfile)
button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

# Start the app
root.mainloop()