"""
MIDI Exporter - Creates MIDI files with separate tracks
"""
import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage
from typing import List, Dict
from pathlib import Path

from .drum_generator import DrumHit
from .chord_generator import Chord
from .melody_generator import Note


class MIDIExporter:
    """Exports patterns to MIDI file with separate tracks"""

    def __init__(self, tempo: int = 90, time_signature: tuple = (4, 4)):
        """
        Initialize MIDI exporter

        Args:
            tempo: BPM (90-100 typical for 90s R&B)
            time_signature: Tuple of (numerator, denominator)
        """
        self.tempo = tempo
        self.time_signature = time_signature
        self.ticks_per_beat = 480

    def create_midi_file(
        self,
        output_path: str,
        hihat: List[DrumHit] = None,
        kick: List[DrumHit] = None,
        snare: List[DrumHit] = None,
        percussion: List[DrumHit] = None,
        rhodes_chords: List[Chord] = None,
        lead_synth: List[Note] = None
    ) -> str:
        """
        Create MIDI file with all elements on separate tracks

        Args:
            output_path: Path to save MIDI file
            hihat: Hi-hat pattern
            kick: Kick drum pattern
            snare: Snare/clap pattern
            percussion: Percussion pattern
            rhodes_chords: Rhodes chord progression
            lead_synth: Lead synth melody

        Returns:
            Path to created MIDI file
        """
        mid = MidiFile(ticks_per_beat=self.ticks_per_beat)

        # Create meta track
        meta_track = MidiTrack()
        mid.tracks.append(meta_track)

        # Add tempo
        tempo_microseconds = mido.bpm2tempo(self.tempo)
        meta_track.append(MetaMessage('set_tempo', tempo=tempo_microseconds, time=0))

        # Add time signature
        meta_track.append(MetaMessage(
            'time_signature',
            numerator=self.time_signature[0],
            denominator=self.time_signature[1],
            time=0
        ))

        # Track 1: Hi-Hat
        if hihat:
            track = self._create_drum_track(hihat, "Hi-Hat", channel=9)
            mid.tracks.append(track)

        # Track 2: Kick
        if kick:
            track = self._create_drum_track(kick, "Kick", channel=9)
            mid.tracks.append(track)

        # Track 3: Snare/Clap
        if snare:
            track = self._create_drum_track(snare, "Snare", channel=9)
            mid.tracks.append(track)

        # Track 4: Percussion
        if percussion:
            track = self._create_drum_track(percussion, "Percussion", channel=9)
            mid.tracks.append(track)

        # Track 5: Rhodes Piano
        if rhodes_chords:
            track = self._create_chord_track(rhodes_chords, "Rhodes Piano", channel=0)
            mid.tracks.append(track)

        # Track 6: Lead Synth
        if lead_synth:
            track = self._create_melody_track(lead_synth, "Lead Synth", channel=1)
            mid.tracks.append(track)

        # Save file
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        mid.save(output_path)

        return output_path

    def _create_drum_track(self, hits: List[DrumHit], name: str, channel: int) -> MidiTrack:
        """Create a drum track from drum hits"""
        track = MidiTrack()
        track.append(MetaMessage('track_name', name=name, time=0))

        # Set to drum channel
        track.append(Message('program_change', program=0, channel=channel, time=0))

        # Sort hits by time
        sorted_hits = sorted(hits, key=lambda x: x.time)

        current_time = 0.0

        for hit in sorted_hits:
            # Calculate delta time in ticks
            delta_ticks = self._beats_to_ticks(hit.time - current_time)
            if delta_ticks < 0:
                delta_ticks = 0

            # Note on
            track.append(Message(
                'note_on',
                note=hit.note,
                velocity=hit.velocity,
                time=delta_ticks,
                channel=channel
            ))

            # Note off (drums typically very short)
            track.append(Message(
                'note_off',
                note=hit.note,
                velocity=0,
                time=10,  # Very short
                channel=channel
            ))

            current_time = hit.time

        return track

    def _create_chord_track(self, chords: List[Chord], name: str, channel: int) -> MidiTrack:
        """Create a track for chord progression"""
        track = MidiTrack()
        track.append(MetaMessage('track_name', name=name, time=0))

        # Electric Piano (Rhodes)
        track.append(Message('program_change', program=4, channel=channel, time=0))

        current_time = 0.0

        for chord in chords:
            # Calculate delta time for chord start
            delta_ticks = self._beats_to_ticks(chord.start_time - current_time)
            if delta_ticks < 0:
                delta_ticks = 0

            # Note on for all notes in chord
            for i, note in enumerate(chord.notes):
                time_delta = delta_ticks if i == 0 else 0
                track.append(Message(
                    'note_on',
                    note=note,
                    velocity=chord.velocity,
                    time=time_delta,
                    channel=channel
                ))

            current_time = chord.start_time

            # Note off for all notes
            duration_ticks = self._beats_to_ticks(chord.duration)

            for i, note in enumerate(chord.notes):
                time_delta = duration_ticks if i == 0 else 0
                track.append(Message(
                    'note_off',
                    note=note,
                    velocity=0,
                    time=time_delta,
                    channel=channel
                ))

            current_time = chord.start_time + chord.duration

        return track

    def _create_melody_track(self, notes: List[Note], name: str, channel: int) -> MidiTrack:
        """Create a track for melody"""
        track = MidiTrack()
        track.append(MetaMessage('track_name', name=name, time=0))

        # Lead Synth
        track.append(Message('program_change', program=81, channel=channel, time=0))

        current_time = 0.0

        for note in notes:
            # Calculate delta time
            delta_ticks = self._beats_to_ticks(note.start_time - current_time)
            if delta_ticks < 0:
                delta_ticks = 0

            # Note on
            track.append(Message(
                'note_on',
                note=note.pitch,
                velocity=note.velocity,
                time=delta_ticks,
                channel=channel
            ))

            current_time = note.start_time

            # Note off
            duration_ticks = self._beats_to_ticks(note.duration)

            track.append(Message(
                'note_off',
                note=note.pitch,
                velocity=0,
                time=duration_ticks,
                channel=channel
            ))

            current_time = note.start_time + note.duration

        return track

    def _beats_to_ticks(self, beats: float) -> int:
        """Convert beats to MIDI ticks"""
        return int(beats * self.ticks_per_beat)

    def export_individual_tracks(
        self,
        output_dir: str,
        base_name: str,
        hihat: List[DrumHit] = None,
        kick: List[DrumHit] = None,
        snare: List[DrumHit] = None,
        percussion: List[DrumHit] = None,
        rhodes_chords: List[Chord] = None,
        lead_synth: List[Note] = None
    ) -> Dict[str, str]:
        """
        Export each element as a separate MIDI file

        Returns:
            Dictionary mapping track name to file path
        """
        files = {}

        if hihat:
            path = f"{output_dir}/{base_name}_hihat.mid"
            self.create_midi_file(path, hihat=hihat)
            files['hihat'] = path

        if kick:
            path = f"{output_dir}/{base_name}_kick.mid"
            self.create_midi_file(path, kick=kick)
            files['kick'] = path

        if snare:
            path = f"{output_dir}/{base_name}_snare.mid"
            self.create_midi_file(path, snare=snare)
            files['snare'] = path

        if percussion:
            path = f"{output_dir}/{base_name}_percussion.mid"
            self.create_midi_file(path, percussion=percussion)
            files['percussion'] = path

        if rhodes_chords:
            path = f"{output_dir}/{base_name}_rhodes.mid"
            self.create_midi_file(path, rhodes_chords=rhodes_chords)
            files['rhodes'] = path

        if lead_synth:
            path = f"{output_dir}/{base_name}_lead.mid"
            self.create_midi_file(path, lead_synth=lead_synth)
            files['lead'] = path

        return files
