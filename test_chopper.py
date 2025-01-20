import ttkbootstrap as tb
from tkinter import filedialog, Tk, Frame, Label, Scrollbar, Canvas
from ttkbootstrap import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from audio_manipulation import AudioProcessor

# Method to retrieve user file and send file to AM
def openfile():
    filepath = filedialog.askopenfile()  # Open the windows file dialog
    if filepath:
        processor = AudioProcessor(filepath.name)
        processor.print_file_info()

        # Update the view to show the uploaded file path
        label.configure(text="file path: " + filepath.name)

        # Clear existing tabs
        for tab in notebook.tabs():
            notebook.forget(tab)

        # Create the amplitude envelope plot
        ae_fig = processor.create_amplitude_envelope_plot()
        ae_canvas = FigureCanvasTkAgg(ae_fig, master=frame_ae)
        ae_canvas.draw()
        ae_canvas.get_tk_widget().pack()
        notebook.add(frame_ae, text="Amplitude Envelope")

        # Create the RMSE plot
        rmse_fig = processor.create_rmse_plot()
        rmse_canvas = FigureCanvasTkAgg(rmse_fig, master=frame_rmse)
        rmse_canvas.draw()
        rmse_canvas.get_tk_widget().pack()
        notebook.add(frame_rmse, text="RMSE")

        # Create the ZCR plot
        zcr_fig = processor.create_zcr_plot()
        zcr_canvas = FigureCanvasTkAgg(zcr_fig, master=frame_zcr)
        zcr_canvas.draw()
        zcr_canvas.get_tk_widget().pack()
        notebook.add(frame_zcr, text="ZCR")

        # Create the sinusoidal wave plot
        sw_fig = processor.create_sinusoidal_wave_plot()
        sw_canvas = FigureCanvasTkAgg(sw_fig, master=frame_sw)
        sw_canvas.draw()
        sw_canvas.get_tk_widget().pack()
        notebook.add(frame_sw, text="Sinusoidal Wave")

        # Create the magnitude plot
        mag_fig = processor.create_magnitude_spectrum_plot()
        mag_canvas = FigureCanvasTkAgg(mag_fig, master=frame_mag)
        mag_canvas.draw()
        mag_canvas.get_tk_widget().pack()
        notebook.add(frame_mag, text="Magnitude Spectrum")

        # Create the spectrogram plot with scrollbar
        sp_fig = processor.create_mel_spectrogram_plot()
        sp_canvas = FigureCanvasTkAgg(sp_fig, master=frame_sp)
        sp_canvas.draw()
        sp_canvas.get_tk_widget().pack()
        notebook.add(frame_sp, text="Spectrogram")

# Setting the theme of the window and size
root = tb.Window(themename="solar")
root.title("Audio Manipulation")
root.geometry("900x700")

# Configure grid layout
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# Create a notebook for the plots
notebook = ttk.Notebook(root)
notebook.grid(row=1, column=0, sticky="nsew")

# Create frames for each plot with fixed size
frame_ae = Frame(notebook, width=800, height=600)
frame_rmse = Frame(notebook, width=800, height=600)
frame_zcr = Frame(notebook, width=800, height=600)
frame_sw = Frame(notebook, width=800, height=600)
frame_mag = Frame(notebook, width=800, height=600)

# Create a frame and canvas for the spectrogram with scrollbar
frame_sp = Frame(notebook, width=800, height=600)
frame_sp.pack(fill="both", expand=True)
# Label to show the file path
label = Label(root, text="No file selected")
label.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

# Upload button
button = tb.Button(root, text="Open File", bootstyle="primary", command=openfile)
button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

# Start the app
root.mainloop()