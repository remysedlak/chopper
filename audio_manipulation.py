import librosa
import librosa.display
from itertools import cycle
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp

FRAME_SIZE = 2048
HOP_LENGTH = 512

class AudioProcessor:
    def __init__(self, path):
        self.path = path
        self.song, self.sr = librosa.load(path)
        self.sample_duration = 1 / self.sr
        self.song_duration = self.sample_duration * self.song.shape[0]
        self.frequency, self.magnitude = self.fast_fourier_transform(self.song, self.sr)
        self.song_envelope = self.audio_envelope(self.song)
        self.song_rmse = self.root_mean_square_energy(self.song)
        self.song_zcr = self.zero_crossing_rate(self.song)
        self.y_song = self.short_time_fourier_transform() # Spectrogram
        self.mel_spectrogram = librosa.feature.melspectrogram(y=self.song, sr=self.sr, 
                                    n_fft=FRAME_SIZE, hop_length=HOP_LENGTH, n_mels=128)
        

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

    def fast_fourier_transform(self, song, sr):
        ft = sp.fft.fft(self.song)
        magnitude = np.absolute(ft)
        frequency = np.linspace(0, self.sr, len(magnitude))
        return frequency, magnitude

    def short_time_fourier_transform(self):
        # Returns a duple. (half of frame_size/2 + 1, number of frames)
        s_song = librosa.stft(self.song, n_fft=FRAME_SIZE, hop_length=HOP_LENGTH)
        y_song = np.abs(s_song) ** 2 # Moving from complex numbers to magnitude
        return y_song

    # To truly move from time domain to frequency domain, compare signal and sinus
    # High magnitude showes simularities between the sample and a certain frequency
    def create_sinusoidal_wave_plot(self):
        samples = range(len(self.song))
        t = librosa.samples_to_time(samples, sr=self.sr)
        
        # Find the dominant frequency of the signal
        frequency, magnitude = self.fast_fourier_transform(self.song, self.sr)
        dominant_frequency = frequency[np.argmax(magnitude)]
        
        phase = 0.55 # We want the phase that will maximize the area of the fill_between
        sin = 0.1 * np.sin(2 * np.pi * (dominant_frequency * t - phase))
        
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(t[10000:10400], self.song[10000:10400], color="r")
        ax.plot(t[10000:10400], sin[10000:10400], color="b")

        ax.fill_between(t[10000:10400], sin[10000:10400] * self.song[10000:10400], color="g")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")
        ax.set_title("Sinusoidal Wave")
        return fig

    def create_frequency_plot(self):
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(self.frequency[:5000], self.magnitude[:5000])
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Magnitude")
        ax.set_title("Frequency Spectrum")
        return fig

    def create_amplitude_envelope_plot(self):
        fig, ax = plt.subplots(figsize=(8, 6))
        frames = range(0, self.song_envelope.size)
        t = librosa.frames_to_time(frames, hop_length=HOP_LENGTH)
        librosa.display.waveshow(self.song, sr=self.sr, ax=ax, alpha=0.5)
        ax.plot(t, self.song_envelope, color="r")
        ax.set_title("Amplitude Envelope")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")
        return fig

    def create_rmse_plot(self):
        fig, ax = plt.subplots(figsize=(8, 6))
        frames = range(0, self.song_rmse.size)
        t = librosa.frames_to_time(frames, hop_length=HOP_LENGTH)
        librosa.display.waveshow(self.song, sr=self.sr, ax=ax, alpha=0.5)
        ax.plot(t, self.song_rmse, color="b")
        ax.set_title("Root Mean Square Energy")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("RMSE")
        return fig

    def create_zcr_plot(self):
        fig, ax = plt.subplots(figsize=(8, 6))
        frames = range(0, self.song_zcr.size)
        t = librosa.frames_to_time(frames, hop_length=HOP_LENGTH)
        librosa.display.waveshow(self.song, sr=self.sr, ax=ax, alpha=0.5)
        ax.plot(t, self.song_zcr, color="g")
        ax.set_title("Zero Crossing Rate")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("ZCR")
        return fig

    def create_magnitude_spectrum_plot(self, f_ratio=0.1):
        num_f_bins = int(len(self.frequency) * f_ratio)
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(self.frequency[:num_f_bins], self.magnitude[:num_f_bins])
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Magnitude")
        ax.set_title("Magnitude Spectrum")
        return fig

    def create_spectrogram_plot(self):
        fig, ax = plt.subplots(figsize=(8, 6))
        librosa.display.specshow(librosa.power_to_db(self.y_song), sr=self.sr, hop_length=HOP_LENGTH, x_axis="time", y_axis="log", ax=ax)
        ax.set_title("Spectrogram")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Frequency (Hz)")
        return fig

    def create_mel_spectrogram_plot(self):
        fig, ax = plt.subplots(figsize=(8, 6))
        img = librosa.display.specshow(librosa.power_to_db(self.mel_spectrogram), x_axis="time", y_axis="mel", sr=self.sr)
        ax.set_title("Mel Spectrogram")
        fig.colorbar(img, format="%+2.0f")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Mel")
        return fig