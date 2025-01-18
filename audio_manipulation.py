import librosa
import librosa.display

# Global variables
song = None
sr = None
path = None

# Load the file path
def print_file_path(filepath):
    print(f"File path received: {filepath}")
    path = filepath


def amplitude_envelope(path):
    song, sr = librosa.load(path, mono=False, sr=None)
    print(f"File size: {song.size}")

    print(song)

    sample_duration = 1 / sr
    print(f"Duration of one sample: {sample_duration:.6f} seconds")

    song_duration = sample_duration * song.shape[1]
    print(f"Duration of the signal: {song_duration:.6f} seconds")
