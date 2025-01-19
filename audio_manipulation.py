import librosa
import librosa.display
import IPython.display as ipd
from itertools import cycle
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp

FRAME_SIZE = 1024
HOP_LENGTH = 512

class AudioProcessor:
    def __init__(self, path):
        self.path = path
        self.song, self.sr = librosa.load(path)
        self.sample_duration = 1 / self.sr
        self.song_duration = self.sample_duration * self.song.shape[0]
        self.frequency, self.magnitude = self.fourier_transform(self.song, self.sr)
        self.song_envelope = self.audio_envelope(self.song)
        self.song_rmse = self.root_mean_square_energy(self.song)
        self.song_zcr = self.zero_crossing_rate(self.song)

    def print_file_path(self):
        print(f"File path received: {self.path}")

    def find_sample_duration(self):
        print(f"Duration of one sample: {self.sample_duration:.6f} seconds")
        print(f"Sample rate: {self.sr}")
        print(f"Duration of the signal: {self.song_duration:.6f} seconds")
        return self.song, self.sr

    def audio_envelope(self, signal):
        return np.array([max(signal[i:i+FRAME_SIZE]) for i in range(0, signal.size, HOP_LENGTH)])

    def root_mean_square_energy(self, signal):
        return librosa.feature.rms(y=signal, frame_length=FRAME_SIZE, hop_length=HOP_LENGTH)[0]

    def zero_crossing_rate(self, signal):
        return librosa.feature.zero_crossing_rate(y=signal, frame_length=FRAME_SIZE, hop_length=HOP_LENGTH)[0]

    def rms(self, signal):
        rms = []
        for i in range(0, len(signal), FRAME_SIZE):
            rms_current_frame = np.sqrt(np.sum(signal[i:i+FRAME_SIZE]**2) / FRAME_SIZE)
            rms.append(rms_current_frame)
        return np.array(rms)

    def fourier_transform(self, signal, sr):
        ft = sp.fft.fft(signal)
        magnitude = np.absolute(ft)
        frequency = np.linspace(0, sr, len(magnitude))
        return frequency, magnitude

    def create_sinusoidal_wave_plot(self, frequency, duration, sr):
        f = 523
        phase = 0
        t = np.linspace(0, duration, int(sr * duration), endpoint=False)
        sin = 0.5 * np.sin(2 * np.pi * (f * t - phase))
        fig, ax = plt.subplots(figsize=(5, 1))
        ax.plot(t[10000:10400], sin[10000:10400], color="r")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")
        ax.set_title("Sinusoidal Wave")
        return fig

    def create_frequency_plot(self):
        fig, ax = plt.subplots(figsize=(5, 1))
        ax.plot(self.frequency[:5000], self.magnitude[:5000])
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Magnitude")
        ax.set_title("Frequency Spectrum")
        return fig

    def create_amplitude_envelope_plot(self):
        fig, ax = plt.subplots(figsize=(5, 1))
        frames = range(0, self.song_envelope.size)
        t = librosa.frames_to_time(frames, hop_length=HOP_LENGTH)
        librosa.display.waveshow(self.song, sr=self.sr, ax=ax, alpha=0.5)
        ax.plot(t, self.song_envelope, color="r")
        ax.set_title("Amplitude Envelope")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")
        return fig

    def create_rmse_plot(self):
        fig, ax = plt.subplots(figsize=(5, 1))
        frames = range(0, self.song_rmse.size)
        t = librosa.frames_to_time(frames, hop_length=HOP_LENGTH)
        librosa.display.waveshow(self.song, sr=self.sr, ax=ax, alpha=0.5)
        ax.plot(t, self.song_rmse, color="b")
        ax.set_title("Root Mean Square Energy")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("RMSE")
        return fig

    def create_zcr_plot(self):
        fig, ax = plt.subplots(figsize=(5, 1))
        frames = range(0, self.song_zcr.size)
        t = librosa.frames_to_time(frames, hop_length=HOP_LENGTH)
        librosa.display.waveshow(self.song, sr=self.sr, ax=ax, alpha=0.5)
        ax.plot(t, self.song_zcr, color="g")
        ax.set_title("Zero Crossing Rate")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("ZCR")
        return fig