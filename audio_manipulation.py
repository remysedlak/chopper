import librosa
import librosa.display
import IPython.display as ipd
from itertools import cycle
import matplotlib.pyplot as plt
import numpy as np

FRAME_SIZE = 1024
HOP_LENGTH = 512

def print_file_path(filepath):
    print(f"File path received: {filepath}")

def find_sample_duration(path):
    y, sr = librosa.load(path)
    print(f"Sample rate: {sr}")
    sample_duration = 1 / sr
    print(f"Duration of one sample: {sample_duration:.6f} seconds")
    song_duration = sample_duration * y.shape[0]
    print(f"Duration of the signal: {song_duration:.6f} seconds")
    return y, sr

def plot_creation(song, sr):
    # Ensure song is a numpy.ndarray
    if not isinstance(song, np.ndarray):
        raise ValueError("Audio data must be of type numpy.ndarray")

    # Create a figure
    fig, ax = plt.subplots(figsize=(15, 17))

    # Create a time array along with the amplitude in time
    song_envelope = audio_envelope(song)
    frames = range(0, song_envelope.size)
    t = librosa.frames_to_time(frames, hop_length=HOP_LENGTH)

    librosa.display.waveshow(song, sr=sr, ax=ax, alpha=0.5)
    ax.plot(t, song_envelope, color="r")
    ax.set_title("File Waveform")
    ax.set_ylim(-1, 1)

    return fig

# calculate the audio envelope
def audio_envelope(signal):
    return np.array([max(signal[i:i+FRAME_SIZE]) for i in range(0, signal.size, HOP_LENGTH)])