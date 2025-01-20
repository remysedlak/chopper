import librosa
import librosa.display
import librosa.feature
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp

FRAME_SIZE = 1028
HOP_LENGTH = 256

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
        self.s_song, self.y_song = self.short_time_fourier_transform() # Spectrogram
        self.mel_spectrogram = librosa.feature.melspectrogram(y=self.song, sr=self.sr, 
                                    n_fft=FRAME_SIZE, hop_length=HOP_LENGTH, n_mels=128)
        self.mfcc = librosa.feature.mfcc(y=self.song, n_mfcc=13, sr=self.sr) #MFCCs
        self.mfcc_delta1, self.mfcc_delta2 = self.mfcc_delta() # 1st and 2nd Derivative of MFCCs
        self.cc_mfcc = self.mfcc + self.mfcc_delta1+self.mfcc_delta2 #Concatenated MFCCs
        self.ber = self.band_energy_ratio(2000)
        self.sc = librosa.feature.spectral_centroid(y=self.song, sr= self.sr, n_fft=FRAME_SIZE, hop_length=HOP_LENGTH)[0]
        self.bandwidth = librosa.feature.spectral_bandwidth(y=self.song, sr= self.sr, n_fft=FRAME_SIZE, hop_length=HOP_LENGTH)[0]
        self.constant_q = librosa.cqt(self.song, sr=self.sr, hop_length=HOP_LENGTH)

    def print_file_info(self):
        print(f"File path received: {self.path}")
        print(f"Duration of one sample: {self.sample_duration:.6f} seconds")
        print(f"Sample rate: {self.sr}")
        print(f"Duration of the signal: {self.song_duration:.6f} seconds")

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

    # FFT returns the magnitude and frequency for an entire signal
    def fast_fourier_transform(self, song, sr):
        ft = sp.fft.fft(self.song)
        magnitude = np.absolute(ft)
        frequency = np.linspace(0, self.sr, len(magnitude))
        return frequency, magnitude

    # STFT returns the magnitude and frequency for a signal, chunked in frames
    def short_time_fourier_transform(self):
        # Returns a duple. (half of frame_size/2 + 1, number of frames)
        s_song = librosa.stft(self.song, n_fft=FRAME_SIZE, hop_length=HOP_LENGTH)
        y_song = np.abs(s_song) ** 2 # Moving from complex numbers to magnitude
        return s_song, y_song

    def mfcc_delta(self):
        mfcc_delta1 = librosa.feature.delta(self.mfcc)
        mfcc_delta2 = librosa.feature.delta(self.mfcc, order = 2)
        return mfcc_delta1, mfcc_delta2

    def split_frequency_bin(self, split_frequency=2000):
        f_range = self.sr / 2 # Nyquist theorem
        f_delta_per_bin = f_range / self.s_song.shape[0]
        split_f_bin = np.floor(split_frequency / f_delta_per_bin) #10.1 --> 10, 10.9 --> 10
        return int(split_f_bin)

    def band_energy_ratio(self, split_frequency=2000):
        split_frequency_bin = self.split_frequency_bin(split_frequency)
        # Move to Color Spectrum
        power_spec = np.abs(self.s_song) **2
        power_spec = power_spec.T

        band_energy_ratio = []
        # Calculate the band energy ratio for each frame
        for f_in_frame in power_spec:
            sum_power_low_f = np.sum(f_in_frame[:split_frequency_bin])
            sum_power_high_f = np.sum(f_in_frame[split_frequency_bin:])
            ber_current_frame = sum_power_low_f / sum_power_high_f
            band_energy_ratio.append(ber_current_frame)
        return np.array(band_energy_ratio)



    # To truly move from time domain to frequency domain, compare signal and sinus
    # High magnitude showes simularities between the sample and a certain frequency
    def create_sinusoidal_wave_plot(self):
        samples = range(len(self.song))
        t = librosa.samples_to_time(samples, sr=self.sr)
        
        # Find the dominant frequency of the signal
        frequency, magnitude = self.fast_fourier_transform(self.song, self.sr)
        dominant_frequency = frequency[np.argmax(magnitude)]
        
        phase = 0.75 # We want the phase that will maximize the area of the fill_between
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
        # Display the waveform
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
        # Display the waveform
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

    def create_mfcc_plot(self):
        fig, ax = plt.subplots(figsize=(8, 6))
        img = librosa.display.specshow(self.mfcc_delta2, x_axis="time",
                                       sr=self.sr)
        ax.set_title("MFCC Delta 2")
        fig.colorbar(img, format="%+2.0f")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Mel")
        return fig

    def create_ber_plot(self):
        frames = range(len(self.ber))
        t = librosa.time_to_frames(frames, hop_length=HOP_LENGTH)
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(t, self.ber, color = 'r')
        return fig

    def create_spectral_centroid_plot(self):
        frames = range(len(self.sc))
        t = librosa.time_to_frames(frames, hop_length=HOP_LENGTH)
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(t, self.sc, color='y')
        return fig

    def create_bandwidth_plot(self):
        frames = range(len(self.bandwidth))
        t = librosa.time_to_frames(frames, hop_length=HOP_LENGTH)
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(t, self.bandwidth, color='g')
        return fig

    def create_cq_plot(self):
        chromagram = librosa.feature.chroma_cqt(y=self.song, sr=self.sr, hop_length=HOP_LENGTH)
        fig, ax = plt.subplots(figsize=(8, 6))
        librosa.display.specshow(chromagram, x_axis='time', y_axis='chroma', hop_length=HOP_LENGTH, cmap='coolwarm')
        return fig