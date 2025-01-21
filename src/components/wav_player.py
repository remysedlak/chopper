import tkinter as tk
from tkinter import filedialog
import pygame  # For playing audio

class WavPlayer(tk.frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(bg="lightgray")
        self.init_audio()
        self.create_widgets()

    def init_audio(self):
        pygame.mixer.init()
        self.current_song = None

    def create_widgets(self):
        self.play_button = tk.Button(self, text="Play", command=self.play_song)
        self.stop_button = tk.Button(self, text="Stop", command=self.stop_song)
        self.load_button = tk.Button(self, text="Load MP3", command=self.load_song)

        self.play_button.pack(side="left", padx=5, pady=5)
        self.stop_button.pack(side="left", padx=5, pady=5)
        self.load_button.pack(side="left", padx=5, pady=5)

    def load_song(self):
        file_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
        if file_path:
            self.current_song = file_path
            pygame.mixer.music.load(file_path)

    def play_song(self):
        if self.current_song:
            pygame.mixer.music.play()

    def stop_song(self):
        pygame.mixer.music.stop()

if __name__ == "__main__":
    import tkinter as tk

    # Create a root window for testing
    root = tk.Tk()
    root.title("Wav Player Test")
    root.geometry("400x100")

    # Instantiate and pack the MP3Player component
    mp3_player = WavPlayer(root)
    mp3_player.pack(fill="both", expand=True)

    # Run the Tkinter event loop
    root.mainloop()