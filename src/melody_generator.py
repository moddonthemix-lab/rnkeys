"""
90s R&B Lead Synth Melody Generator
Generates vocal-style melodic lines
"""
import random
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class Note:
    """Represents a single melody note"""
    pitch: int  # MIDI note number
    start_time: float  # Start time in beats
    duration: float  # Duration in beats
    velocity: int  # MIDI velocity


class LeadSynthGenerator:
    """Generates 90s R&B style lead synth melodies"""

    # Pentatonic scale (super common in R&B melodies)
    # Major pentatonic: 1, 2, 3, 5, 6
    MAJOR_PENTATONIC = [0, 2, 4, 7, 9]
    # Minor pentatonic: 1, b3, 4, 5, b7
    MINOR_PENTATONIC = [0, 3, 5, 7, 10]

    # Blues scale: 1, b3, 4, b5, 5, b7
    BLUES_SCALE = [0, 3, 5, 6, 7, 10]

    # Common melodic patterns
    MELODIC_CONTOURS = [
        [0, 1, 2, 1, 0],           # Rise and fall
        [0, 2, 1, 3, 2],           # Step up
        [3, 2, 1, 0],              # Descending
        [0, 1, 0, 2, 1, 0],        # Wave
        [0, 2, 4, 2, 0],           # Arc
        [0, -1, 1, 0],             # Neighbor tones
    ]

    def __init__(self, key: str = 'C', bars: int = 4, octave: int = 5):
        """
        Initialize melody generator

        Args:
            key: Root key
            bars: Number of bars
            octave: Starting octave for melody (4-6 typical)
        """
        self.bars = bars
        self.key_root = self._note_to_midi(key, octave)
        self.beats = bars * 4

    def generate_melody(self, style: str = "smooth", scale: str = "major_pentatonic") -> List[Note]:
        """
        Generate a lead melody

        Args:
            style: "smooth" (legato), "rhythmic" (more variation), "riff" (repeated pattern)
            scale: "major_pentatonic", "minor_pentatonic", "blues"

        Returns:
            List of melody notes
        """
        # Select scale
        if scale == "minor_pentatonic":
            scale_intervals = self.MINOR_PENTATONIC
        elif scale == "blues":
            scale_intervals = self.BLUES_SCALE
        else:
            scale_intervals = self.MAJOR_PENTATONIC

        melody = []

        if style == "smooth":
            # Longer notes, vocal-like phrasing
            time = 0
            while time < self.beats:
                # Pick note from scale
                scale_degree = random.randint(0, len(scale_intervals) - 1)
                pitch = self.key_root + scale_intervals[scale_degree]

                # Vary octave occasionally
                if random.random() < 0.3:
                    pitch += random.choice([-12, 12])

                # Longer note durations
                duration = random.choice([1.0, 1.5, 2.0, 2.5, 0.75])

                melody.append(Note(
                    pitch=pitch,
                    start_time=time,
                    duration=duration,
                    velocity=random.randint(80, 100)
                ))

                time += duration

                # Add rest occasionally
                if random.random() < 0.2:
                    time += random.choice([0.5, 1.0])

        elif style == "rhythmic":
            # More notes, syncopated rhythm
            time = 0
            while time < self.beats:
                scale_degree = random.randint(0, len(scale_intervals) - 1)
                pitch = self.key_root + scale_intervals[scale_degree]

                # Shorter, varied durations
                duration = random.choice([0.25, 0.5, 0.75, 1.0, 0.375])

                melody.append(Note(
                    pitch=pitch,
                    start_time=time,
                    duration=duration,
                    velocity=random.randint(70, 100)
                ))

                time += duration

                # More frequent rests
                if random.random() < 0.3:
                    time += 0.5

        else:  # riff style
            # Create a short pattern and repeat/vary it
            contour = random.choice(self.MELODIC_CONTOURS)

            # Build the riff
            riff_notes = []
            time = 0
            for step in contour:
                scale_degree = (step % len(scale_intervals))
                pitch = self.key_root + scale_intervals[scale_degree]

                if step > len(scale_intervals) - 1:
                    pitch += 12  # Go up an octave
                elif step < 0:
                    pitch -= 12  # Go down

                riff_notes.append((pitch, random.choice([0.5, 0.75, 1.0])))

            # Repeat the riff with variations
            bar_count = 0
            while bar_count < self.bars:
                for pitch, duration in riff_notes:
                    # Add variation to repeated riffs
                    if random.random() < 0.2:
                        pitch += random.choice([-2, 2, 12])

                    melody.append(Note(
                        pitch=pitch,
                        start_time=time,
                        duration=duration,
                        velocity=random.randint(75, 105)
                    ))

                    time += duration

                # Rest between riff repetitions
                time += random.choice([0.5, 1.0])
                bar_count = time // 4

        return melody[:int(self.beats / 0.5)]  # Limit total notes

    def generate_lead_line_with_slides(self) -> List[Note]:
        """
        Generate a melody with pitch slides/bends (very 90s R&B)

        Returns:
            List of notes (with some notes close together for slide effect)
        """
        melody = []
        time = 0

        while time < self.beats:
            # Main note
            scale_degree = random.randint(0, len(self.MAJOR_PENTATONIC) - 1)
            pitch = self.key_root + self.MAJOR_PENTATONIC[scale_degree]

            # Should we add a slide?
            if random.random() < 0.3:
                # Slide up from a semitone or whole tone below
                slide_from = pitch - random.choice([1, 2])
                melody.append(Note(
                    pitch=slide_from,
                    start_time=time,
                    duration=0.125,  # Very short
                    velocity=random.randint(60, 80)
                ))
                time += 0.125

            # Main note
            duration = random.choice([0.75, 1.0, 1.5, 2.0])
            melody.append(Note(
                pitch=pitch,
                start_time=time,
                duration=duration,
                velocity=random.randint(85, 105)
            ))

            time += duration

            # Rest
            if random.random() < 0.3:
                time += 0.5

        return melody

    def generate_call_and_response(self) -> Tuple[List[Note], List[Note]]:
        """
        Generate call and response pattern (2 bars each)

        Returns:
            Tuple of (call_melody, response_melody)
        """
        half_bars = self.bars // 2

        # Call (first half)
        call = []
        time = 0
        target_time = half_bars * 4

        while time < target_time:
            scale_degree = random.randint(0, len(self.MAJOR_PENTATONIC) - 1)
            pitch = self.key_root + self.MAJOR_PENTATONIC[scale_degree]
            duration = random.choice([0.5, 1.0, 1.5])

            call.append(Note(
                pitch=pitch,
                start_time=time,
                duration=duration,
                velocity=random.randint(80, 100)
            ))

            time += duration + random.choice([0, 0.5])

        # Response (second half, lower register)
        response = []
        time = target_time

        while time < self.beats:
            scale_degree = random.randint(0, len(self.MAJOR_PENTATONIC) - 1)
            pitch = (self.key_root - 12) + self.MAJOR_PENTATONIC[scale_degree]  # Octave lower
            duration = random.choice([0.5, 1.0, 1.5])

            response.append(Note(
                pitch=pitch,
                start_time=time,
                duration=duration,
                velocity=random.randint(75, 95)
            ))

            time += duration + random.choice([0, 0.5])

        return call, response

    def _note_to_midi(self, note: str, octave: int = 4) -> int:
        """Convert note name to MIDI number"""
        note_map = {
            'C': 0, 'C#': 1, 'Db': 1,
            'D': 2, 'D#': 3, 'Eb': 3,
            'E': 4,
            'F': 5, 'F#': 6, 'Gb': 6,
            'G': 7, 'G#': 8, 'Ab': 8,
            'A': 9, 'A#': 10, 'Bb': 10,
            'B': 11,
        }
        return (octave + 1) * 12 + note_map.get(note, 0)
