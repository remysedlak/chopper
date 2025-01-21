from tkinter import filedialog
from src.components.plotter import Plotter

class FileUploader:
    def __init__(self, label, notebook):
        self.label = label
        self.notebook = notebook

    def open_file(self):
        filepath = filedialog.askopenfile()
        if filepath:
            self.label.configure(text="File path: " + filepath.name)

            # Create and handle plots
            plotter = Plotter(filepath.name, self.notebook)
            plotter.generate_plots()
