"""
Melody extraction module using basic-pitch (Spotify's audio-to-MIDI model)
"""
import numpy as np
from typing import List, Tuple, Optional
import tempfile
import os


class MelodyExtractor:
    """Extracts melody from audio and converts to MIDI notes"""

    def __init__(self):
        self.notes = []

    def extract_melody(self, audio_path: str) -> Tuple[List[dict], str]:
        """
        Extract melody from audio file using basic-pitch

        Args:
            audio_path: Path to audio file

        Returns:
            Tuple of (notes_list, midi_path)
            notes_list: List of dicts with 'pitch', 'start', 'end', 'velocity'
            midi_path: Path to generated MIDI file
        """
        print("Extracting melody using basic-pitch...")

        try:
            from basic_pitch.inference import predict
            from basic_pitch import ICASSP_2022_MODEL_PATH
        except ImportError:
            print("Warning: basic-pitch not installed. Installing it will improve melody extraction.")
            print("For now, using simplified melody extraction...")
            return self._extract_melody_simple(audio_path)

        # Create temp directory for output
        temp_dir = tempfile.mkdtemp()
        output_dir = temp_dir

        try:
            # Run basic-pitch prediction
            model_output, midi_data, note_events = predict(
                audio_path,
                ICASSP_2022_MODEL_PATH
            )

            # Convert note events to our format
            notes = []
            for start_time, end_time, pitch, velocity, _ in note_events:
                notes.append({
                    'pitch': int(pitch),
                    'start': float(start_time),
                    'end': float(end_time),
                    'velocity': int(velocity * 127) if velocity <= 1.0 else int(velocity)
                })

            # Save MIDI to temp file
            midi_path = os.path.join(output_dir, "melody.mid")
            if midi_data is not None:
                midi_data.write(midi_path)
            else:
                # Create MIDI from notes if midi_data is None
                midi_path = self._notes_to_midi_file(notes, midi_path)

            self.notes = notes
            print(f"Extracted {len(notes)} melody notes")

            return notes, midi_path

        except Exception as e:
            print(f"Error with basic-pitch: {e}")
            print("Falling back to simplified melody extraction...")
            return self._extract_melody_simple(audio_path)

    def _extract_melody_simple(self, audio_path: str) -> Tuple[List[dict], str]:
        """
        Simplified melody extraction using librosa pitch tracking
        Fallback when basic-pitch is not available
        """
        import librosa

        print("Using simplified melody extraction...")

        # Load audio
        y, sr = librosa.load(audio_path, sr=22050)

        # Extract pitch using piptrack
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr, fmin=librosa.note_to_hz('C2'),
                                                fmax=librosa.note_to_hz('C7'))

        # Get the pitch with highest magnitude at each frame
        notes = []
        hop_length = 512
        note_on = False
        current_note = None

        for i in range(pitches.shape[1]):
            index = magnitudes[:, i].argmax()
            pitch_hz = pitches[index, i]

            if pitch_hz > 0:
                # Convert Hz to MIDI note number
                midi_note = int(librosa.hz_to_midi(pitch_hz))
                time = librosa.frames_to_time(i, sr=sr, hop_length=hop_length)

                if not note_on:
                    # Start new note
                    current_note = {
                        'pitch': midi_note,
                        'start': time,
                        'end': time,
                        'velocity': 80
                    }
                    note_on = True
                elif abs(midi_note - current_note['pitch']) > 1:
                    # Pitch changed significantly, end current note and start new one
                    current_note['end'] = time
                    if current_note['end'] - current_note['start'] > 0.1:  # Min duration
                        notes.append(current_note)

                    current_note = {
                        'pitch': midi_note,
                        'start': time,
                        'end': time,
                        'velocity': 80
                    }
                else:
                    # Continue current note
                    current_note['end'] = time
            else:
                # No pitch detected
                if note_on and current_note is not None:
                    # End current note
                    if current_note['end'] - current_note['start'] > 0.1:
                        notes.append(current_note)
                    note_on = False
                    current_note = None

        # Save last note
        if note_on and current_note is not None:
            if current_note['end'] - current_note['start'] > 0.1:
                notes.append(current_note)

        # Create MIDI file
        midi_path = os.path.join(tempfile.gettempdir(), "melody_simple.mid")
        midi_path = self._notes_to_midi_file(notes, midi_path)

        self.notes = notes
        print(f"Extracted {len(notes)} melody notes (simplified method)")

        return notes, midi_path

    def _notes_to_midi_file(self, notes: List[dict], output_path: str) -> str:
        """Convert notes list to MIDI file"""
        import mido
        from mido import Message, MidiFile, MidiTrack

        mid = MidiFile()
        track = MidiTrack()
        mid.tracks.append(track)

        # Set tempo (500000 microseconds per beat = 120 BPM)
        track.append(mido.MetaMessage('set_tempo', tempo=500000))

        # Convert notes to MIDI messages
        # Sort notes by start time
        sorted_notes = sorted(notes, key=lambda x: x['start'])

        current_time = 0
        for note in sorted_notes:
            # Note on
            delta_time = int((note['start'] - current_time) * 480)  # Convert to ticks
            if delta_time < 0:
                delta_time = 0

            track.append(Message('note_on',
                               note=note['pitch'],
                               velocity=note['velocity'],
                               time=delta_time))

            current_time = note['start']

            # Note off
            note_duration = note['end'] - note['start']
            delta_time = int(note_duration * 480)

            track.append(Message('note_off',
                               note=note['pitch'],
                               velocity=0,
                               time=delta_time))

            current_time = note['end']

        mid.save(output_path)
        return output_path
