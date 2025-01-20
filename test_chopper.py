import ttkbootstrap as tb
from tkinter import filedialog, Tk, Frame, Label
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from audio_manipulation import AudioProcessor

# Method to retrieve user file and send file to AM
def openfile():
    filepath = filedialog.askopenfile() # Open the windows file dialog
    if filepath:
        processor = AudioProcessor(filepath.name)
        processor.print_file_path()
        song, sr = processor.find_sample_duration()

        # Update the view to show the uploaded file path
        label.configure(text="file path: " + filepath.name)

        # # Create the amplitude envelope plot
        # ae_fig = processor.create_amplitude_envelope_plot()
        # ae_canvas = FigureCanvasTkAgg(ae_fig, master=frame)
        # ae_canvas.draw()
        # ae_canvas.get_tk_widget().grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # # Create the RMSE plot
        # rmse_fig = processor.create_rmse_plot()
        # rmse_canvas = FigureCanvasTkAgg(rmse_fig, master=frame)
        # rmse_canvas.draw()
        # rmse_canvas.get_tk_widget().grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # # Create the ZCR plot
        # zcr_fig = processor.create_zcr_plot()
        # zcr_canvas = FigureCanvasTkAgg(zcr_fig, master=frame)
        # zcr_canvas.draw()
        # zcr_canvas.get_tk_widget().grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

        # Create the sinusoidal wave plot
        sw_fig = processor.create_sinusoidal_wave_plot()
        sw_canvas = FigureCanvasTkAgg(sw_fig, master=frame)
        sw_canvas.draw()
        sw_canvas.get_tk_widget().grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

        # Create the magnitude plot
        mag_fig = processor.create_magnitude_spectrum_plot()
        mag_canvas = FigureCanvasTkAgg(mag_fig, master=frame)
        mag_canvas.draw()
        mag_canvas.get_tk_widget().grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

# Setting the theme of the window and size
root = tb.Window(themename="solar")
root.title("Audio Manipulation")
root.geometry("500x500")

# Configure grid layout
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# Create a frame for the plots
frame = Frame(root)
frame.grid(row=1, column=0, sticky="nsew")

# Configure grid layout for the frame
frame.grid_rowconfigure(0, weight=1)
frame.grid_rowconfigure(1, weight=1)
frame.grid_rowconfigure(2, weight=1)
frame.grid_columnconfigure(0, weight=1)

# Label to show the file path
label = Label(root, text="No file selected")
label.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

# Upload button
button = tb.Button(root, text="Open File", bootstyle="primary", command=openfile)
button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

# Start the app
root.mainloop()