"""
90s R&B Rhodes Piano Chord Progression Generator
Generates soulful, jazzy chord progressions
"""
import random
from typing import List, Tuple, Dict
from dataclasses import dataclass


@dataclass
class Chord:
    """Represents a chord with notes and timing"""
    root: int  # MIDI note number
    notes: List[int]  # MIDI note numbers for the chord
    start_time: float  # Start time in beats
    duration: float  # Duration in beats
    velocity: int  # MIDI velocity


class RhodesChordGenerator:
    """Generates 90s R&B style chord progressions for Rhodes/keys"""

    # Common 90s R&B progressions (in scale degrees)
    PROGRESSIONS = [
        # Classic R&B
        [1, 5, 6, 4],  # I-V-vi-IV (very common)
        [6, 4, 1, 5],  # vi-IV-I-V (emotional)
        [1, 6, 4, 5],  # I-vi-IV-V (doo-wop)
        [2, 5, 1],     # ii-V-I (jazz influence)
        [6, 4, 5, 1],  # vi-IV-V-I
        [1, 4, 5, 4],  # I-IV-V-IV (gospel)
        [1, 3, 4, 5],  # I-iii-IV-V
        [1, 4, 6, 5],  # I-IV-vi-V
    ]

    # Major scale intervals
    MAJOR_SCALE = [0, 2, 4, 5, 7, 9, 11]

    # Chord voicings (intervals from root)
    CHORD_TYPES = {
        'maj7': [0, 4, 7, 11],           # Major 7th
        'min7': [0, 3, 7, 10],           # Minor 7th
        'dom7': [0, 4, 7, 10],           # Dominant 7th
        'min9': [0, 3, 7, 10, 14],       # Minor 9th
        'maj9': [0, 4, 7, 11, 14],       # Major 9th
        'dom9': [0, 4, 7, 10, 14],       # Dominant 9th
        '6': [0, 4, 7, 9],               # Major 6th
        'min6': [0, 3, 7, 9],            # Minor 6th
        'sus2': [0, 2, 7],               # Suspended 2nd
        'sus4': [0, 5, 7],               # Suspended 4th
    }

    def __init__(self, key: str = 'C', bars: int = 4):
        """
        Initialize chord generator

        Args:
            key: Root key (C, D, E, F, G, A, B with optional # or b)
            bars: Number of bars to generate
        """
        self.bars = bars
        self.key_root = self._note_to_midi(key)
        self.beats = bars * 4

    def generate_progression(self, style: str = "smooth") -> List[Chord]:
        """
        Generate a chord progression

        Args:
            style: "smooth" (jazzy), "gospel" (more movement), "minimal" (sparse)

        Returns:
            List of chords
        """
        # Pick a progression
        progression = random.choice(self.PROGRESSIONS)

        chords = []

        if style == "minimal":
            # One chord per bar, long sustained
            for i, degree in enumerate(progression[:self.bars]):
                root = self._get_scale_note(degree)
                chord_type = self._get_chord_type_for_degree(degree)
                notes = self._build_chord(root, chord_type)

                chords.append(Chord(
                    root=root,
                    notes=notes,
                    start_time=i * 4,
                    duration=4.0,
                    velocity=random.randint(70, 90)
                ))

        elif style == "smooth":
            # Two chords per bar with variations
            progression_extended = progression * 2
            for i in range(min(self.bars * 2, len(progression_extended))):
                degree = progression_extended[i % len(progression)]
                root = self._get_scale_note(degree)
                chord_type = self._get_chord_type_for_degree(degree)
                notes = self._build_chord(root, chord_type)

                # Add some inversions for smooth voice leading
                if i > 0 and random.random() < 0.4:
                    notes = self._invert_chord(notes)

                chords.append(Chord(
                    root=root,
                    notes=notes,
                    start_time=(i * 2),
                    duration=2.0,
                    velocity=random.randint(65, 85)
                ))

        else:  # gospel - more rhythmic
            # Syncopated chords with rhythmic variations
            time = 0
            while time < self.beats:
                degree = progression[int(time / 4) % len(progression)]
                root = self._get_scale_note(degree)
                chord_type = self._get_chord_type_for_degree(degree)
                notes = self._build_chord(root, chord_type)

                # Vary durations for rhythm
                duration = random.choice([1.0, 1.5, 2.0, 0.5])

                chords.append(Chord(
                    root=root,
                    notes=notes,
                    start_time=time,
                    duration=duration,
                    velocity=random.randint(75, 95)
                ))

                time += duration

        return chords

    def generate_rhodes_stabs(self) -> List[Chord]:
        """
        Generate short Rhodes stabs (common in 90s R&B)

        Returns:
            List of short chord hits
        """
        stabs = []
        progression = random.choice(self.PROGRESSIONS)

        for bar in range(self.bars):
            # Stabs on syncopated beats
            stab_times = random.sample([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5], k=random.randint(2, 4))

            for time in stab_times:
                degree = progression[bar % len(progression)]
                root = self._get_scale_note(degree)
                chord_type = self._get_chord_type_for_degree(degree)
                notes = self._build_chord(root, chord_type)

                stabs.append(Chord(
                    root=root,
                    notes=notes,
                    start_time=bar * 4 + time,
                    duration=0.25,  # Short stabs
                    velocity=random.randint(80, 110)
                ))

        return sorted(stabs, key=lambda x: x.start_time)

    def _get_scale_note(self, degree: int) -> int:
        """Get MIDI note for a scale degree"""
        # Scale degree is 1-indexed
        scale_index = (degree - 1) % 7
        octave = (degree - 1) // 7
        return self.key_root + self.MAJOR_SCALE[scale_index] + (octave * 12)

    def _get_chord_type_for_degree(self, degree: int) -> str:
        """Get appropriate chord type for scale degree"""
        degree_in_scale = ((degree - 1) % 7) + 1

        # Common chord types for each degree in major scale
        chord_map = {
            1: random.choice(['maj7', 'maj9', '6']),      # I
            2: random.choice(['min7', 'min9']),           # ii
            3: random.choice(['min7', 'min9']),           # iii
            4: random.choice(['maj7', 'maj9', '6']),      # IV
            5: random.choice(['dom7', 'dom9']),           # V
            6: random.choice(['min7', 'min9', 'min6']),   # vi
            7: 'min7',                                     # vii (rarely used)
        }

        return chord_map.get(degree_in_scale, 'maj7')

    def _build_chord(self, root: int, chord_type: str) -> List[int]:
        """Build chord notes from root and type"""
        intervals = self.CHORD_TYPES.get(chord_type, [0, 4, 7])

        # Rhodes typically plays in middle register (C3-C5)
        # Adjust octave if needed
        if root < 48:  # Below C3
            root += 12
        elif root > 72:  # Above C5
            root -= 12

        notes = [root + interval for interval in intervals]
        return notes

    def _invert_chord(self, notes: List[int]) -> List[int]:
        """Invert chord for voice leading"""
        if len(notes) < 3:
            return notes

        # Move lowest note up an octave
        inverted = notes[1:] + [notes[0] + 12]
        return sorted(inverted)

    def _note_to_midi(self, note: str) -> int:
        """Convert note name to MIDI number (C4 = 60)"""
        note_map = {
            'C': 60, 'C#': 61, 'Db': 61,
            'D': 62, 'D#': 63, 'Eb': 63,
            'E': 64,
            'F': 65, 'F#': 66, 'Gb': 66,
            'G': 67, 'G#': 68, 'Ab': 68,
            'A': 69, 'A#': 70, 'Bb': 70,
            'B': 71,
        }
        return note_map.get(note, 60)
