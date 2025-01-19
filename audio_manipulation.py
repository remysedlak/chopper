import librosa
import librosa.display
import IPython.display as ipd
from itertools import cycle
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp

FRAME_SIZE = 1024
HOP_LENGTH = 512

def print_file_path(filepath):
    print(f"File path received: {filepath}")

def find_sample_duration(path):

    # Get song signal and sample rate from path
    song, sr = librosa.load(path)
    # Get sample duration in seconds
    sample_duration = 1 / sr
    # Get song duration in seconds
    song_duration = sample_duration * song.shape[0] 

    print(f"Duration of one sample: {sample_duration:.6f} seconds")
    print(f"Sample rate: {sr}")
    print(f"Duration of the signal: {song_duration:.6f} seconds")

    return song, sr

# Calculates the audio envelope of a signal
def audio_envelope(signal):
    return np.array([max(signal[i:i+FRAME_SIZE]) for i in range(0, signal.size, HOP_LENGTH)])

# Returns the RMSE of a signal using librosa
def root_mean_square_energy(signal):
    return librosa.feature.rms(y=signal, frame_length=FRAME_SIZE, hop_length=HOP_LENGTH)[0]

# Returns the zero crossing rate of a signal using librosa
def zero_crossing_rate(signal):
    return librosa.feature.zero_crossing_rate(y=signal, frame_length=FRAME_SIZE, hop_length=HOP_LENGTH)[0]

# Self implementation of RMSE, in case of replacing librosa option
def rms(signal):
    #rms for each frame
    rms = []
    # from beginning to end, stepping through each frame
    for i in range(0, len(signal), FRAME_SIZE):
        rms_current_frame = np.sqrt(np.sum(signal[i:i+FRAME_SIZE]**2) / FRAME_SIZE)
        rms.append(rms_current_frame) # add each value to the rms list
    return np.array(rms)

def fourier_transform(signal, sr):
    # SciPy fast fourier trasnform function
    ft = sp.fft.fft(signal)
    # Absolute value of fft = magnitude (y axis of the spectrum)
    magnitude = np.abs(ft)
    # Distributed between 0 hz and the sampling rate, 
    # divided in steps of the magnitude array length
    frequency = np.linspace(0, sr, len(magnitude))
    return frequency, magnitude

# Creates a plot of the frequency spectrum of a signal, from FFT
def create_frequency_plot(signal, sr):
    fig, ax = plt.subplots(figsize=(3,2))
    frequency, magnitude = fourier_transform(signal, sr)
    ax.plot(frequency[:5000], magnitude[:5000])
    ax.set_title("Frequency Spectrum")
    return fig

# Creates a plot of the amplitude envelope of a signal
def create_amplitude_envelope_plot(song, sr):
    fig, ax = plt.subplots(figsize=(3,2)) # Create a figure
    # Create a time array along with the amplitude in time
    song_envelope = audio_envelope(song)
    
    frames = range(0, song_envelope.size)
    t = librosa.frames_to_time(frames, hop_length=HOP_LENGTH)

    librosa.display.waveshow(song, sr=sr, ax=ax, alpha=0.5)
    ax.plot(t, song_envelope, color="r")
    ax.set_title("File Waveform")
    ax.set_ylim(-1, 1)

    return fig

# Creates a plot of the RMSE of a signal
def create_rmse_plot(song, sr):

    fig, ax = plt.subplots(figsize=(3,1))

    # Create a time array along with the amplitude in time
    song_rmse = root_mean_square_energy(song)
    
    frames = range(0, song_rmse.size)
    t = librosa.frames_to_time(frames, hop_length=HOP_LENGTH)

    librosa.display.waveshow(song, sr=sr, ax=ax, alpha=0.5)
    ax.plot(t, song_rmse, color="r")
    ax.set_title("File Waveform")
    ax.set_ylim(-1, 1)

    return fig
    
def create_zcr_plot(song, sr):

    fig, ax = plt.subplots(figsize=(3,1))

    # Create a time array along with the amplitude in time
    song_zcr = zero_crossing_rate(song)
    
    frames = range(0, song_zcr.size)
    t = librosa.frames_to_time(frames, hop_length=HOP_LENGTH)

    librosa.display.waveshow(song, sr=sr, ax=ax, alpha=0.5)
    ax.plot(t, song_zcr, color="r")
    ax.set_title("File Waveform")
    ax.set_ylim(-1, 1)

    return fig