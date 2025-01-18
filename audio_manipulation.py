import librosa
import librosa.display
import IPython.display as ipd
from itertools import cycle
import matplotlib.pyplot as plt
import numpy as np

def print_file_path(filepath):
    print(f"File path received: {filepath}")

def amplitude_envelope(path):
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

    librosa.display.waveshow(song, sr=sr, ax=ax, alpha=0.5)
    ax.set_title("File Waveform")
    ax.set_ylim(-1, 1)

    return fig