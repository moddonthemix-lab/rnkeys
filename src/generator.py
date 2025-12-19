"""
Main RNKeys Generator - Orchestrates all pattern generation
"""
from typing import Dict, Optional
from pathlib import Path

from .drum_generator import DrumPatternGenerator
from .chord_generator import RhodesChordGenerator
from .melody_generator import LeadSynthGenerator
from .midi_exporter import MIDIExporter


class RNKeysGenerator:
    """Main 90s R&B pattern generator"""

    def __init__(
        self,
        key: str = 'C',
        tempo: int = 95,
        bars: int = 8,
        swing: float = 0.1
    ):
        """
        Initialize RNKeys generator

        Args:
            key: Musical key (C, D, E, F, G, A, B with optional # or b)
            tempo: BPM (80-120 typical for 90s R&B)
            bars: Number of bars to generate
            swing: Amount of swing (0.0-0.3)
        """
        self.key = key
        self.tempo = tempo
        self.bars = bars
        self.swing = swing

        # Initialize generators
        self.drum_gen = DrumPatternGenerator(bars=bars, swing=swing)
        self.chord_gen = RhodesChordGenerator(key=key, bars=bars)
        self.melody_gen = LeadSynthGenerator(key=key, bars=bars)
        self.exporter = MIDIExporter(tempo=tempo)

    def generate_complete_beat(
        self,
        output_path: str,
        hihat_complexity: str = "medium",
        kick_style: str = "rnb",
        use_claps: bool = True,
        percussion_type: str = "shaker",
        chord_style: str = "smooth",
        melody_style: str = "smooth",
        melody_scale: str = "major_pentatonic",
        separate_tracks: bool = False
    ) -> Dict[str, str]:
        """
        Generate a complete 90s R&B beat with all elements

        Args:
            output_path: Path for output MIDI file
            hihat_complexity: "simple", "medium", "complex"
            kick_style: "rnb" or "hiphop"
            use_claps: Mix claps with snare
            percussion_type: "shaker", "tambourine", "conga"
            chord_style: "smooth", "gospel", "minimal"
            melody_style: "smooth", "rhythmic", "riff"
            melody_scale: "major_pentatonic", "minor_pentatonic", "blues"
            separate_tracks: If True, also export individual track files

        Returns:
            Dictionary with file paths
        """
        print("=" * 60)
        print("RNKeys - 90s R&B MIDI Generator")
        print("=" * 60)
        print(f"Key: {self.key}")
        print(f"Tempo: {self.tempo} BPM")
        print(f"Bars: {self.bars}")
        print(f"Swing: {self.swing}")
        print()

        # Generate patterns
        print("[1/7] Generating hi-hat pattern...")
        hihat = self.drum_gen.generate_hihat_pattern(complexity=hihat_complexity)
        print(f"  Generated {len(hihat)} hi-hat hits")

        print("[2/7] Generating kick pattern...")
        kick = self.drum_gen.generate_kick_pattern(style=kick_style)
        print(f"  Generated {len(kick)} kick hits")

        print("[3/7] Generating snare pattern...")
        snare = self.drum_gen.generate_snare_pattern(use_claps=use_claps)
        print(f"  Generated {len(snare)} snare/clap hits")

        print("[4/7] Generating percussion...")
        percussion = self.drum_gen.generate_percussion(perc_type=percussion_type)
        print(f"  Generated {len(percussion)} {percussion_type} hits")

        print("[5/7] Generating Rhodes chord progression...")
        rhodes = self.chord_gen.generate_progression(style=chord_style)
        print(f"  Generated {len(rhodes)} chords")

        print("[6/7] Generating lead synth melody...")
        lead = self.melody_gen.generate_melody(style=melody_style, scale=melody_scale)
        print(f"  Generated {len(lead)} melody notes")

        print("[7/7] Exporting MIDI files...")

        # Create main MIDI file with all tracks
        main_file = self.exporter.create_midi_file(
            output_path=output_path,
            hihat=hihat,
            kick=kick,
            snare=snare,
            percussion=percussion,
            rhodes_chords=rhodes,
            lead_synth=lead
        )

        files = {'complete': main_file}
        print(f"  Created: {main_file}")

        # Optionally export individual tracks
        if separate_tracks:
            output_dir = str(Path(output_path).parent)
            base_name = Path(output_path).stem

            individual_files = self.exporter.export_individual_tracks(
                output_dir=output_dir,
                base_name=base_name,
                hihat=hihat,
                kick=kick,
                snare=snare,
                percussion=percussion,
                rhodes_chords=rhodes,
                lead_synth=lead
            )

            files.update(individual_files)

            for track_name, file_path in individual_files.items():
                print(f"  Created: {file_path}")

        print()
        print("=" * 60)
        print("✓ Beat generation complete!")
        print("=" * 60)
        print()
        print("Pattern Details:")
        print(f"  Hi-hats: {len(hihat)} hits ({hihat_complexity} complexity)")
        print(f"  Kick: {len(kick)} hits ({kick_style} style)")
        print(f"  Snare: {len(snare)} hits ({'with claps' if use_claps else 'snare only'})")
        print(f"  Percussion: {len(percussion)} {percussion_type} hits")
        print(f"  Rhodes: {len(rhodes)} chords ({chord_style} style)")
        print(f"  Lead: {len(lead)} notes ({melody_style} style, {melody_scale})")
        print()
        print("Output files:")
        for file_type, file_path in files.items():
            print(f"  {file_type}: {file_path}")
        print("=" * 60)

        return files

    def generate_drums_only(self, output_path: str, **kwargs) -> str:
        """Generate drums only (hi-hat, kick, snare, percussion)"""
        hihat = self.drum_gen.generate_hihat_pattern(
            complexity=kwargs.get('hihat_complexity', 'medium')
        )
        kick = self.drum_gen.generate_kick_pattern(
            style=kwargs.get('kick_style', 'rnb')
        )
        snare = self.drum_gen.generate_snare_pattern(
            use_claps=kwargs.get('use_claps', True)
        )
        percussion = self.drum_gen.generate_percussion(
            perc_type=kwargs.get('percussion_type', 'shaker')
        )

        return self.exporter.create_midi_file(
            output_path=output_path,
            hihat=hihat,
            kick=kick,
            snare=snare,
            percussion=percussion
        )

    def generate_rhodes_only(self, output_path: str, style: str = "smooth") -> str:
        """Generate Rhodes chord progression only"""
        rhodes = self.chord_gen.generate_progression(style=style)

        return self.exporter.create_midi_file(
            output_path=output_path,
            rhodes_chords=rhodes
        )

    def generate_melody_only(
        self,
        output_path: str,
        style: str = "smooth",
        scale: str = "major_pentatonic"
    ) -> str:
        """Generate lead synth melody only"""
        lead = self.melody_gen.generate_melody(style=style, scale=scale)

        return self.exporter.create_midi_file(
            output_path=output_path,
            lead_synth=lead
        )
