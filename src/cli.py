#!/usr/bin/env python3
"""
Command-line interface for RNKeys Song to MIDI Converter
"""
import click
import sys
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .converter import SongToMIDIConverter


console = Console()


@click.command()
@click.argument('audio_file', type=click.Path(exists=True))
@click.option(
    '-o', '--output',
    default='output',
    help='Output directory for MIDI files (default: output/)'
)
@click.option(
    '-n', '--name',
    default=None,
    help='Output filename (without extension). Defaults to input filename.'
)
@click.option(
    '--no-chords',
    is_flag=True,
    help='Skip chord detection'
)
@click.option(
    '--no-melody',
    is_flag=True,
    help='Skip melody extraction'
)
@click.option(
    '--chord-length',
    default=2.0,
    type=float,
    help='Length of chord segments in seconds (default: 2.0)'
)
@click.option(
    '--version',
    is_flag=True,
    help='Show version information'
)
def main(audio_file, output, name, no_chords, no_melody, chord_length, version):
    """
    RNKeys - Convert audio files to MIDI with chord progressions and melody

    \b
    Usage:
        rnkeys song.mp3
        rnkeys song.wav -o my_output/ -n my_song
        rnkeys song.mp3 --no-chords
        rnkeys song.mp3 --chord-length 4.0

    \b
    Supported formats: MP3, WAV, FLAC, OGG, M4A
    """

    if version:
        from . import __version__
        console.print(f"RNKeys version {__version__}")
        return

    # Validate inputs
    if no_chords and no_melody:
        console.print("[red]Error: Cannot disable both chords and melody![/red]")
        sys.exit(1)

    try:
        # Create converter
        converter = SongToMIDIConverter(output_dir=output)

        # Run conversion
        results = converter.convert(
            audio_file=audio_file,
            output_name=name,
            include_chords=not no_chords,
            include_melody=not no_melody,
            chord_segment_length=chord_length
        )

        console.print("\n[green]✓ Conversion successful![/green]")

    except FileNotFoundError as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error during conversion: {e}[/red]")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
