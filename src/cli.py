#!/usr/bin/env python3
"""
RNKeys CLI - Generate 90s R&B MIDI patterns
"""
import click
from rich.console import Console
from pathlib import Path

from .generator import RNKeysGenerator
from . import __version__


console = Console()


@click.command()
@click.option(
    '-o', '--output',
    default='output/rnkeys_beat.mid',
    help='Output MIDI file path'
)
@click.option(
    '-k', '--key',
    default='C',
    help='Musical key (C, D, E, F, G, A, B with optional # or b)'
)
@click.option(
    '-t', '--tempo',
    default=95,
    type=int,
    help='Tempo in BPM (80-120 recommended for 90s R&B)'
)
@click.option(
    '-b', '--bars',
    default=8,
    type=int,
    help='Number of bars to generate'
)
@click.option(
    '--swing',
    default=0.1,
    type=float,
    help='Swing amount (0.0-0.3)'
)
@click.option(
    '--hihat',
    default='medium',
    type=click.Choice(['simple', 'medium', 'complex']),
    help='Hi-hat complexity'
)
@click.option(
    '--kick',
    default='rnb',
    type=click.Choice(['rnb', 'hiphop']),
    help='Kick drum style'
)
@click.option(
    '--claps/--no-claps',
    default=True,
    help='Mix claps with snare'
)
@click.option(
    '--percussion',
    default='shaker',
    type=click.Choice(['shaker', 'tambourine', 'conga']),
    help='Percussion type'
)
@click.option(
    '--chords',
    default='smooth',
    type=click.Choice(['smooth', 'gospel', 'minimal']),
    help='Rhodes chord style'
)
@click.option(
    '--melody',
    default='smooth',
    type=click.Choice(['smooth', 'rhythmic', 'riff']),
    help='Lead synth melody style'
)
@click.option(
    '--scale',
    default='major_pentatonic',
    type=click.Choice(['major_pentatonic', 'minor_pentatonic', 'blues']),
    help='Melody scale'
)
@click.option(
    '--separate/--no-separate',
    default=False,
    help='Export separate MIDI files for each track'
)
@click.option(
    '--drums-only',
    is_flag=True,
    help='Generate drums only (no chords or melody)'
)
@click.option(
    '--rhodes-only',
    is_flag=True,
    help='Generate Rhodes chords only'
)
@click.option(
    '--melody-only',
    is_flag=True,
    help='Generate lead melody only'
)
@click.option(
    '--version',
    is_flag=True,
    help='Show version'
)
def main(
    output, key, tempo, bars, swing, hihat, kick, claps, percussion,
    chords, melody, scale, separate, drums_only, rhodes_only, melody_only, version
):
    """
    RNKeys - 90s R&B MIDI Pattern Generator

    \b
    Generate authentic 90s R&B drum patterns, Rhodes progressions, and lead synths.
    Compete with Timbaland and R. Kelly!

    \b
    Examples:
        # Generate a complete beat
        rnkeys

        # Slow jam in D minor
        rnkeys -k D -t 85 --scale minor_pentatonic --chords smooth

        # Upbeat jam with complex hi-hats
        rnkeys -t 110 --hihat complex --melody rhythmic

        # Drums only (no melody/chords)
        rnkeys --drums-only

        # Export all tracks separately
        rnkeys --separate

        # Gospel-style Rhodes in F
        rnkeys -k F --rhodes-only --chords gospel
    """

    if version:
        console.print(f"RNKeys version {__version__}")
        return

    try:
        # Create generator
        generator = RNKeysGenerator(
            key=key,
            tempo=tempo,
            bars=bars,
            swing=swing
        )

        # Generate based on mode
        if drums_only:
            console.print("[cyan]Generating drums only...[/cyan]\n")
            generator.generate_drums_only(
                output_path=output,
                hihat_complexity=hihat,
                kick_style=kick,
                use_claps=claps,
                percussion_type=percussion
            )
        elif rhodes_only:
            console.print("[cyan]Generating Rhodes chords only...[/cyan]\n")
            generator.generate_rhodes_only(
                output_path=output,
                style=chords
            )
        elif melody_only:
            console.print("[cyan]Generating lead melody only...[/cyan]\n")
            generator.generate_melody_only(
                output_path=output,
                style=melody,
                scale=scale
            )
        else:
            # Complete beat
            generator.generate_complete_beat(
                output_path=output,
                hihat_complexity=hihat,
                kick_style=kick,
                use_claps=claps,
                percussion_type=percussion,
                chord_style=chords,
                melody_style=melody,
                melody_scale=scale,
                separate_tracks=separate
            )

        console.print("\n[green]✓ MIDI generation successful![/green]")
        console.print(f"\nLoad these MIDI files into your DAW and add that 90s R&B flavor! 🎹🥁🎵")

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        import traceback
        traceback.print_exc()
        exit(1)


if __name__ == '__main__':
    main()
