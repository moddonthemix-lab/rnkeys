# Examples

Place your audio files in this directory to test the converter.

## Quick Test

1. Add an audio file (e.g., `song.mp3`, `track.wav`) to this directory
2. Run the converter:

```bash
cd ..
python rnkeys.py examples/your_song.mp3
```

3. Check the `output/` directory for the generated MIDI files

## Example Commands

```bash
# Basic conversion
python rnkeys.py examples/song.mp3

# Custom output directory
python rnkeys.py examples/song.mp3 -o examples/midi_output/

# Only extract chords
python rnkeys.py examples/song.mp3 --no-melody

# Only extract melody
python rnkeys.py examples/song.mp3 --no-chords

# Longer chord segments for slower songs
python rnkeys.py examples/ballad.mp3 --chord-length 4.0
```

## Recommended Test Files

For best results, try with:
- Clear, well-mixed audio
- Songs with distinct chord progressions
- Tracks with prominent melody lines
- Various genres (pop, rock, jazz, classical)

## Note

Example audio files are not included in this repository due to copyright.
Please use your own audio files for testing.
