from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.audio_processor import AudioProcessor
from tkinter import Frame

class Plotter:
    def __init__(self, file_path, notebook):
        self.file_path = file_path
        self.notebook = notebook
        self.processor = AudioProcessor(file_path)

    def create_frame(self, notebook, title):
        frame = Frame(notebook, width=800, height=600)
        frame.pack(fill="both", expand=True)
        notebook.add(frame, text=title)
        return frame

    def add_plot_to_frame(self, figure, frame):
        canvas = FigureCanvasTkAgg(figure, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def generate_plots(self):
        plots = {
            "AE": self.processor.create_amplitude_envelope_plot(),
            "RMSE": self.processor.create_rmse_plot(),
            "ZCR": self.processor.create_zcr_plot(),
            "Magnitude Spectrum": self.processor.create_magnitude_spectrum_plot(),
            "Spectrogram": self.processor.create_mel_spectrogram_plot(),
            "MFCC": self.processor.create_mfcc_plot(),
            "BER": self.processor.create_ber_plot(),
            "Spectral Centroid": self.processor.create_spectral_centroid_plot(),
            "Bandwidth": self.processor.create_bandwidth_plot(),
            "Q-Spec": self.processor.create_cq_plot(),
        }

        for title, figure in plots.items():
            frame = self.create_frame(self.notebook, title)
            self.add_plot_to_frame(figure, frame)
