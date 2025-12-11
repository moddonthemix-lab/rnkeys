"""
Audio processing module for loading and analyzing audio files
"""
import librosa
import numpy as np
from typing import Tuple, Optional
import soundfile as sf


class AudioProcessor:
    """Handles audio file loading and preprocessing"""

    def __init__(self, sample_rate: int = 22050):
        self.sample_rate = sample_rate
        self.audio_data = None
        self.duration = None

    def load_audio(self, file_path: str) -> Tuple[np.ndarray, float]:
        """
        Load an audio file and return the audio data and duration

        Args:
            file_path: Path to the audio file

        Returns:
            Tuple of (audio_data, duration)
        """
        print(f"Loading audio file: {file_path}")

        # Load audio file
        self.audio_data, sr = librosa.load(file_path, sr=self.sample_rate, mono=True)
        self.duration = librosa.get_duration(y=self.audio_data, sr=self.sample_rate)

        print(f"Audio loaded: {self.duration:.2f} seconds, sample rate: {self.sample_rate} Hz")

        return self.audio_data, self.duration

    def get_tempo(self) -> float:
        """
        Detect the tempo (BPM) of the loaded audio

        Returns:
            Tempo in beats per minute
        """
        if self.audio_data is None:
            raise ValueError("No audio loaded. Call load_audio() first.")

        tempo, _ = librosa.beat.beat_track(y=self.audio_data, sr=self.sample_rate)

        # Handle case where tempo is an array
        if isinstance(tempo, np.ndarray):
            tempo = float(tempo[0]) if len(tempo) > 0 else 120.0

        print(f"Detected tempo: {tempo:.1f} BPM")
        return float(tempo)

    def get_key(self) -> Tuple[str, str]:
        """
        Detect the musical key of the audio

        Returns:
            Tuple of (key, mode) e.g. ('C', 'major')
        """
        if self.audio_data is None:
            raise ValueError("No audio loaded. Call load_audio() first.")

        # Extract chroma features
        chromagram = librosa.feature.chroma_cqt(y=self.audio_data, sr=self.sample_rate)

        # Average chroma across time
        chroma_avg = np.mean(chromagram, axis=1)

        # Key names
        key_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

        # Find the predominant pitch class
        key_idx = np.argmax(chroma_avg)
        key = key_names[key_idx]

        # Simple major/minor detection based on chroma profile
        # Major scale intervals: 0, 2, 4, 5, 7, 9, 11
        # Minor scale intervals: 0, 2, 3, 5, 7, 8, 10
        major_profile = np.array([1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1])
        minor_profile = np.array([1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0])

        # Rotate profiles to match detected key
        major_rotated = np.roll(major_profile, key_idx)
        minor_rotated = np.roll(minor_profile, key_idx)

        # Correlate with actual chroma
        major_corr = np.corrcoef(chroma_avg, major_rotated)[0, 1]
        minor_corr = np.corrcoef(chroma_avg, minor_rotated)[0, 1]

        mode = 'major' if major_corr > minor_corr else 'minor'

        print(f"Detected key: {key} {mode}")
        return key, mode

    def get_beat_times(self) -> np.ndarray:
        """
        Get the timing of beats in the audio

        Returns:
            Array of beat times in seconds
        """
        if self.audio_data is None:
            raise ValueError("No audio loaded. Call load_audio() first.")

        _, beat_frames = librosa.beat.beat_track(y=self.audio_data, sr=self.sample_rate)
        beat_times = librosa.frames_to_time(beat_frames, sr=self.sample_rate)

        print(f"Detected {len(beat_times)} beats")
        return beat_times
