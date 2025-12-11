"""
Main converter module that orchestrates the audio-to-MIDI conversion
"""
import os
from typing import Optional, Tuple
from pathlib import Path

from .audio_processor import AudioProcessor
from .chord_detector import ChordDetector
from .melody_extractor import MelodyExtractor
from .midi_generator import MIDIGenerator


class SongToMIDIConverter:
    """Main converter class that coordinates the conversion process"""

    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        self.audio_processor = AudioProcessor()
        self.chord_detector = ChordDetector()
        self.melody_extractor = MelodyExtractor()
        self.midi_generator = None

        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)

    def convert(
        self,
        audio_file: str,
        output_name: Optional[str] = None,
        include_chords: bool = True,
        include_melody: bool = True,
        chord_segment_length: float = 2.0
    ) -> dict:
        """
        Convert an audio file to MIDI

        Args:
            audio_file: Path to input audio file
            output_name: Name for output files (without extension)
            include_chords: Whether to include chord detection
            include_melody: Whether to include melody extraction
            chord_segment_length: Length of segments for chord detection (seconds)

        Returns:
            Dictionary with conversion results and file paths
        """
        print("=" * 60)
        print("RNKeys - Song to MIDI Converter")
        print("=" * 60)
        print(f"Input file: {audio_file}")
        print()

        # Validate input file
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Audio file not found: {audio_file}")

        # Determine output name
        if output_name is None:
            output_name = Path(audio_file).stem

        # Step 1: Load and analyze audio
        print("[1/5] Loading and analyzing audio...")
        audio_data, duration = self.audio_processor.load_audio(audio_file)
        tempo = self.audio_processor.get_tempo()
        key, mode = self.audio_processor.get_key()
        print()

        # Initialize MIDI generator with detected tempo
        self.midi_generator = MIDIGenerator(tempo=tempo)

        results = {
            'duration': duration,
            'tempo': tempo,
            'key': key,
            'mode': mode,
            'chords': None,
            'melody_notes': None,
            'output_files': {}
        }

        # Step 2: Detect chords
        chords = None
        if include_chords:
            print("[2/5] Detecting chord progressions...")
            chords = self.chord_detector.detect_chords(
                audio_data,
                self.audio_processor.sample_rate,
                segment_length=chord_segment_length
            )
            results['chords'] = chords

            # Print chord progression
            print("\nChord Progression:")
            for i, chord in enumerate(chords[:20]):  # Show first 20
                print(f"  {chord.start_time:6.2f}s - {chord.end_time:6.2f}s: "
                      f"{chord.chord_name:6s} (confidence: {chord.confidence:.2f})")
            if len(chords) > 20:
                print(f"  ... and {len(chords) - 20} more chords")
            print()
        else:
            print("[2/5] Skipping chord detection (disabled)")
            print()

        # Step 3: Extract melody
        melody_notes = None
        if include_melody:
            print("[3/5] Extracting melody...")
            melody_notes, _ = self.melody_extractor.extract_melody(audio_file)
            results['melody_notes'] = melody_notes
            print(f"  Extracted {len(melody_notes)} melody notes")
            print()
        else:
            print("[3/5] Skipping melody extraction (disabled)")
            print()

        # Step 4: Generate MIDI files
        print("[4/5] Generating MIDI files...")

        if include_chords and include_melody and chords and melody_notes:
            # Generate combined MIDI
            output_path = os.path.join(self.output_dir, f"{output_name}_full.mid")
            self.midi_generator.create_midi_from_chords_and_melody(
                chords, melody_notes, output_path, key, mode
            )
            results['output_files']['full'] = output_path
            print(f"  Created: {output_path}")

        if include_chords and chords:
            # Generate chords-only MIDI
            output_path = os.path.join(self.output_dir, f"{output_name}_chords.mid")
            self.midi_generator.create_chord_only_midi(chords, output_path)
            results['output_files']['chords'] = output_path
            print(f"  Created: {output_path}")

        if include_melody and melody_notes:
            # Generate melody-only MIDI
            output_path = os.path.join(self.output_dir, f"{output_name}_melody.mid")
            self.midi_generator._add_melody_to_track(
                self._create_basic_midi_track(),
                melody_notes
            )
            # Save melody-only MIDI
            from mido import MidiFile, MidiTrack, MetaMessage
            mid = MidiFile(ticks_per_beat=480)
            track = self._create_basic_midi_track()
            mid.tracks.append(track)
            self.midi_generator._add_melody_to_track(track, melody_notes)
            mid.save(output_path)
            results['output_files']['melody'] = output_path
            print(f"  Created: {output_path}")

        print()

        # Step 5: Summary
        print("[5/5] Conversion complete!")
        print("=" * 60)
        print("Summary:")
        print(f"  Duration: {duration:.2f} seconds")
        print(f"  Tempo: {tempo:.1f} BPM")
        print(f"  Key: {key} {mode}")
        if chords:
            print(f"  Chords detected: {len(chords)}")
        if melody_notes:
            print(f"  Melody notes: {len(melody_notes)}")
        print()
        print("Output files:")
        for file_type, file_path in results['output_files'].items():
            print(f"  {file_type}: {file_path}")
        print("=" * 60)

        return results

    def _create_basic_midi_track(self):
        """Create a basic MIDI track with tempo settings"""
        from mido import MidiTrack, MetaMessage
        import mido

        track = MidiTrack()
        tempo_microseconds = mido.bpm2tempo(self.midi_generator.tempo)
        track.append(MetaMessage('set_tempo', tempo=tempo_microseconds, time=0))
        return track
