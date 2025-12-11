"""
MIDI file generation module
"""
import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage
from typing import List, Optional
import os
from .chord_detector import ChordSegment


class MIDIGenerator:
    """Generates MIDI files from chords and melody"""

    # Chord to MIDI notes mapping
    CHORD_INTERVALS = {
        'maj': [0, 4, 7],
        'min': [0, 3, 7],
        'm': [0, 3, 7],
        'dim': [0, 3, 6],
        'aug': [0, 4, 8],
        '7': [0, 4, 7, 10],
        'maj7': [0, 4, 7, 11],
        'min7': [0, 3, 7, 10],
        'm7': [0, 3, 7, 10],
        'sus2': [0, 2, 7],
        'sus4': [0, 5, 7],
    }

    NOTE_TO_MIDI = {
        'C': 60, 'C#': 61, 'D': 62, 'D#': 63, 'E': 64, 'F': 65,
        'F#': 66, 'G': 67, 'G#': 68, 'A': 69, 'A#': 70, 'B': 71
    }

    def __init__(self, tempo: float = 120.0):
        self.tempo = tempo
        self.ticks_per_beat = 480

    def create_midi_from_chords_and_melody(
        self,
        chords: List[ChordSegment],
        melody_notes: List[dict],
        output_path: str,
        key: str = 'C',
        mode: str = 'major'
    ) -> str:
        """
        Create a MIDI file with separate tracks for chords and melody

        Args:
            chords: List of chord segments
            melody_notes: List of melody notes
            output_path: Path to save MIDI file
            key: Musical key
            mode: Musical mode (major/minor)

        Returns:
            Path to created MIDI file
        """
        print(f"Generating MIDI file: {output_path}")

        mid = MidiFile(ticks_per_beat=self.ticks_per_beat)

        # Create tracks
        meta_track = MidiTrack()
        chord_track = MidiTrack()
        melody_track = MidiTrack()

        mid.tracks.append(meta_track)
        mid.tracks.append(chord_track)
        mid.tracks.append(melody_track)

        # Add meta information
        tempo_microseconds = mido.bpm2tempo(self.tempo)
        meta_track.append(MetaMessage('set_tempo', tempo=tempo_microseconds, time=0))
        meta_track.append(MetaMessage('key_signature', key=key, time=0))
        meta_track.append(MetaMessage('time_signature', numerator=4, denominator=4, time=0))

        # Add track names
        chord_track.append(MetaMessage('track_name', name='Chords', time=0))
        melody_track.append(MetaMessage('track_name', name='Melody', time=0))

        # Add chord progression to chord track
        self._add_chords_to_track(chord_track, chords)

        # Add melody to melody track
        self._add_melody_to_track(melody_track, melody_notes)

        # Save MIDI file
        mid.save(output_path)
        print(f"MIDI file saved: {output_path}")

        return output_path

    def _add_chords_to_track(self, track: MidiTrack, chords: List[ChordSegment]):
        """Add chord progression to a MIDI track"""
        current_time = 0.0

        for chord in chords:
            # Parse chord name
            chord_notes = self._parse_chord(chord.chord_name)

            if not chord_notes:
                continue

            # Calculate time delta in ticks
            start_ticks = self._seconds_to_ticks(chord.start_time)
            delta_time = start_ticks - int(current_time * self.ticks_per_beat)

            if delta_time < 0:
                delta_time = 0

            # Add note on messages
            for i, note in enumerate(chord_notes):
                time_delta = delta_time if i == 0 else 0
                track.append(Message('note_on',
                                   note=note,
                                   velocity=80,
                                   time=time_delta))

            current_time = chord.start_time

            # Calculate note duration
            duration = chord.end_time - chord.start_time
            duration_ticks = int(duration * self.ticks_per_beat * self.tempo / 60)

            # Add note off messages
            for i, note in enumerate(chord_notes):
                time_delta = duration_ticks if i == 0 else 0
                track.append(Message('note_off',
                                   note=note,
                                   velocity=0,
                                   time=time_delta))

            current_time = chord.end_time

    def _add_melody_to_track(self, track: MidiTrack, melody_notes: List[dict]):
        """Add melody notes to a MIDI track"""
        if not melody_notes:
            return

        current_time = 0.0

        # Sort notes by start time
        sorted_notes = sorted(melody_notes, key=lambda x: x['start'])

        for note in sorted_notes:
            # Calculate delta time
            start_ticks = self._seconds_to_ticks(note['start'])
            delta_time = start_ticks - int(current_time * self.ticks_per_beat)

            if delta_time < 0:
                delta_time = 0

            # Note on
            track.append(Message('note_on',
                               note=note['pitch'],
                               velocity=note.get('velocity', 90),
                               time=delta_time))

            current_time = note['start']

            # Calculate note duration
            duration = note['end'] - note['start']
            duration_ticks = self._seconds_to_ticks(duration)

            # Note off
            track.append(Message('note_off',
                               note=note['pitch'],
                               velocity=0,
                               time=duration_ticks))

            current_time = note['end']

    def _parse_chord(self, chord_name: str) -> List[int]:
        """
        Parse chord name and return MIDI note numbers

        Args:
            chord_name: Chord name (e.g., 'Cmaj', 'Am', 'G7')

        Returns:
            List of MIDI note numbers
        """
        if chord_name == 'N' or not chord_name:
            return []

        # Extract root note
        root = chord_name[0]
        if len(chord_name) > 1 and chord_name[1] == '#':
            root += '#'
            chord_type = chord_name[2:] if len(chord_name) > 2 else 'maj'
        else:
            chord_type = chord_name[1:] if len(chord_name) > 1 else 'maj'

        # Default to major if type not recognized
        if not chord_type or chord_type not in self.CHORD_INTERVALS:
            chord_type = 'maj'

        # Get root MIDI note (use octave 4 as base)
        if root not in self.NOTE_TO_MIDI:
            return []

        root_midi = self.NOTE_TO_MIDI[root]

        # Get chord intervals
        intervals = self.CHORD_INTERVALS.get(chord_type, [0, 4, 7])

        # Build chord notes
        chord_notes = [root_midi + interval for interval in intervals]

        return chord_notes

    def _seconds_to_ticks(self, seconds: float) -> int:
        """Convert seconds to MIDI ticks"""
        # ticks = seconds * (ticks_per_beat * BPM / 60)
        return int(seconds * self.ticks_per_beat * self.tempo / 60)

    def create_chord_only_midi(self, chords: List[ChordSegment], output_path: str) -> str:
        """Create MIDI file with only chord progression"""
        mid = MidiFile(ticks_per_beat=self.ticks_per_beat)
        track = MidiTrack()
        mid.tracks.append(track)

        # Add tempo
        tempo_microseconds = mido.bpm2tempo(self.tempo)
        track.append(MetaMessage('set_tempo', tempo=tempo_microseconds, time=0))
        track.append(MetaMessage('track_name', name='Chords', time=0))

        self._add_chords_to_track(track, chords)

        mid.save(output_path)
        return output_path
