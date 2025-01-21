import ttkbootstrap as tb
from tkinter import Label, ttk
from components.file_uploader import FileUploader

# Main Application
root = tb.Window(themename="solar")
root.title("Audio Manipulation")
root.geometry("900x700")

# Configure layout
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# Notebook for plots
notebook = ttk.Notebook(root)
notebook.grid(row=1, column=0, sticky="nsew")

# Label to display selected file path
label = Label(root, text="No file selected")
label.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

# File uploader component
uploader = FileUploader(label, notebook)

# Upload button
button = tb.Button(root, text="Open File", bootstyle="primary", command=uploader.open_file)
button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

# Start the app
root.mainloop()
