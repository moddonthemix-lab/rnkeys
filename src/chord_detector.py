"""
Chord detection module using chroma features and pattern matching
"""
import librosa
import numpy as np
from typing import List, Tuple, Dict
from dataclasses import dataclass


@dataclass
class ChordSegment:
    """Represents a detected chord with timing information"""
    chord_name: str
    start_time: float
    end_time: float
    confidence: float


class ChordDetector:
    """Detects chords from audio using chromagram analysis"""

    # Chord templates (pitch class profiles)
    CHORD_TEMPLATES = {
        'maj': np.array([1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]),  # Major: Root, M3, P5
        'min': np.array([1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]),  # Minor: Root, m3, P5
        'dim': np.array([1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0]),  # Diminished
        'aug': np.array([1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]),  # Augmented
        '7': np.array([1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0]),    # Dominant 7th
        'maj7': np.array([1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1]), # Major 7th
        'min7': np.array([1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0]), # Minor 7th
    }

    NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    def __init__(self, hop_length: int = 512):
        self.hop_length = hop_length

    def detect_chords(self, audio_data: np.ndarray, sr: int,
                     segment_length: float = 2.0) -> List[ChordSegment]:
        """
        Detect chords in the audio

        Args:
            audio_data: Audio time series
            sr: Sample rate
            segment_length: Length of each segment to analyze (seconds)

        Returns:
            List of detected chord segments
        """
        print("Detecting chords...")

        # Compute chromagram
        chromagram = librosa.feature.chroma_cqt(
            y=audio_data,
            sr=sr,
            hop_length=self.hop_length
        )

        # Calculate number of frames per segment
        frames_per_segment = int(segment_length * sr / self.hop_length)

        chords = []
        num_frames = chromagram.shape[1]

        for i in range(0, num_frames, frames_per_segment):
            end_frame = min(i + frames_per_segment, num_frames)

            # Average chroma over the segment
            segment_chroma = np.mean(chromagram[:, i:end_frame], axis=1)

            # Detect chord
            chord_name, confidence = self._match_chord(segment_chroma)

            # Convert frame indices to time
            start_time = librosa.frames_to_time(i, sr=sr, hop_length=self.hop_length)
            end_time = librosa.frames_to_time(end_frame, sr=sr, hop_length=self.hop_length)

            # Only add chord if confidence is reasonable
            if confidence > 0.5:
                chords.append(ChordSegment(
                    chord_name=chord_name,
                    start_time=start_time,
                    end_time=end_time,
                    confidence=confidence
                ))

        # Merge consecutive identical chords
        merged_chords = self._merge_consecutive_chords(chords)

        print(f"Detected {len(merged_chords)} chord segments")
        return merged_chords

    def _match_chord(self, chroma: np.ndarray) -> Tuple[str, float]:
        """
        Match a chroma vector to the closest chord template

        Args:
            chroma: 12-dimensional chroma vector

        Returns:
            Tuple of (chord_name, confidence)
        """
        best_chord = "N"  # No chord
        best_confidence = 0.0

        # Normalize chroma
        if np.sum(chroma) > 0:
            chroma = chroma / np.sum(chroma)

        # Try all root notes and chord types
        for root_idx, root_note in enumerate(self.NOTE_NAMES):
            for chord_type, template in self.CHORD_TEMPLATES.items():
                # Rotate template to match root note
                rotated_template = np.roll(template, root_idx)

                # Normalize template
                if np.sum(rotated_template) > 0:
                    rotated_template = rotated_template / np.sum(rotated_template)

                # Calculate correlation
                correlation = np.corrcoef(chroma, rotated_template)[0, 1]

                if correlation > best_confidence:
                    best_confidence = correlation
                    chord_suffix = '' if chord_type == 'maj' else chord_type
                    if chord_type == 'min':
                        chord_suffix = 'm'
                    best_chord = f"{root_note}{chord_suffix}"

        return best_chord, best_confidence

    def _merge_consecutive_chords(self, chords: List[ChordSegment]) -> List[ChordSegment]:
        """Merge consecutive identical chords"""
        if not chords:
            return []

        merged = []
        current = chords[0]

        for chord in chords[1:]:
            if chord.chord_name == current.chord_name:
                # Extend current chord
                current = ChordSegment(
                    chord_name=current.chord_name,
                    start_time=current.start_time,
                    end_time=chord.end_time,
                    confidence=max(current.confidence, chord.confidence)
                )
            else:
                merged.append(current)
                current = chord

        merged.append(current)
        return merged

    def chords_to_progression(self, chords: List[ChordSegment]) -> List[str]:
        """
        Convert chord segments to a simple progression list

        Args:
            chords: List of chord segments

        Returns:
            List of unique chord names in order
        """
        return [chord.chord_name for chord in chords]
