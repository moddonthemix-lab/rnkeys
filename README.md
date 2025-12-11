# RNKeys - Song to MIDI Converter

Convert any song into playable MIDI files with automatic chord detection and melody extraction. Upload a song and get MIDI keys that match the chords, progressions, and melody!

## Features

- **Automatic Chord Detection**: Analyzes audio to detect chord progressions
- **Melody Extraction**: Extracts the main melody line and converts it to MIDI notes
- **Key Detection**: Automatically detects the musical key and mode
- **Tempo Detection**: Identifies the BPM of your song
- **Multiple Output Formats**:
  - Full MIDI (chords + melody)
  - Chords-only MIDI
  - Melody-only MIDI
- **Easy CLI Interface**: Simple command-line tool for quick conversions

## Installation

### Requirements

- Python 3.8 or higher
- FFmpeg (for audio file support)

### Setup

1. Clone this repository:
```bash
git clone <repository-url>
cd rnkeys
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Installing FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html)

## Usage

### Basic Usage

Convert any audio file to MIDI:

```bash
python rnkeys.py your_song.mp3
```

This will create three MIDI files in the `output/` directory:
- `your_song_full.mid` - Complete version with chords and melody
- `your_song_chords.mid` - Chord progression only
- `your_song_melody.mid` - Melody line only

### Advanced Options

**Specify custom output directory:**
```bash
python rnkeys.py song.mp3 -o my_midis/
```

**Custom output filename:**
```bash
python rnkeys.py song.mp3 -n mysong
```

**Skip chord detection:**
```bash
python rnkeys.py song.mp3 --no-chords
```

**Skip melody extraction:**
```bash
python rnkeys.py song.mp3 --no-melody
```

**Adjust chord segment length:**
```bash
python rnkeys.py song.mp3 --chord-length 4.0
```

**Show help:**
```bash
python rnkeys.py --help
```

### Supported Audio Formats

- MP3
- WAV
- FLAC
- OGG
- M4A
- And more (any format supported by FFmpeg)

## How It Works

1. **Audio Loading**: Loads and preprocesses the audio file
2. **Key & Tempo Detection**: Analyzes the audio to determine key signature and BPM
3. **Chord Detection**: Uses chromagram analysis to identify chord progressions
4. **Melody Extraction**: Employs pitch tracking and Spotify's basic-pitch model to extract melody
5. **MIDI Generation**: Converts detected musical elements into MIDI format

## Technical Details

### Chord Detection

The chord detection algorithm uses:
- Constant-Q Transform (CQT) chromagram
- Template matching with major, minor, diminished, augmented, and 7th chords
- Confidence scoring to filter out uncertain detections
- Automatic merging of consecutive identical chords

### Melody Extraction

Two methods are available:
1. **Basic-Pitch** (primary): Spotify's neural network model for accurate audio-to-MIDI conversion
2. **Librosa** (fallback): Pitch tracking using piptrack for simpler melody extraction

## Example Output

```
============================================================
RNKeys - Song to MIDI Converter
============================================================
Input file: examples/song.mp3

[1/5] Loading and analyzing audio...
Audio loaded: 180.50 seconds, sample rate: 22050 Hz
Detected tempo: 120.0 BPM
Detected key: C major

[2/5] Detecting chord progressions...
Detected 42 chord segments

Chord Progression:
    0.00s -   2.00s: C      (confidence: 0.85)
    2.00s -   4.00s: Am     (confidence: 0.78)
    4.00s -   6.00s: F      (confidence: 0.82)
    6.00s -   8.00s: G      (confidence: 0.80)
    ...

[3/5] Extracting melody...
  Extracted 245 melody notes

[4/5] Generating MIDI files...
  Created: output/song_full.mid
  Created: output/song_chords.mid
  Created: output/song_melody.mid

[5/5] Conversion complete!
============================================================
Summary:
  Duration: 180.50 seconds
  Tempo: 120.0 BPM
  Key: C major
  Chords detected: 42
  Melody notes: 245

Output files:
  full: output/song_full.mid
  chords: output/song_chords.mid
  melody: output/song_melody.mid
============================================================
```

## Use Cases

- **Music Production**: Extract chords and melody from reference tracks
- **Learning**: Analyze songs to understand chord progressions
- **Cover Songs**: Get MIDI notes to play along with any song
- **Remixing**: Use extracted MIDI in your DAW
- **Music Theory**: Study progressions and melodies from your favorite songs

## Troubleshooting

**Issue: "No module named 'basic_pitch'"**
- Solution: Install with `pip install basic-pitch`

**Issue: "FFmpeg not found"**
- Solution: Install FFmpeg (see Installation section)

**Issue: Poor chord detection accuracy**
- Solution: Try adjusting `--chord-length` parameter (2.0-4.0 seconds works best)
- Clean, well-mixed audio works better than lo-fi or heavily distorted tracks

**Issue: Melody extraction missing notes**
- Solution: The basic-pitch model works best on monophonic melodies. Complex polyphonic audio may not extract perfectly.

## Project Structure

```
rnkeys/
├── src/
│   ├── __init__.py           # Package initialization
│   ├── audio_processor.py    # Audio loading and analysis
│   ├── chord_detector.py     # Chord detection logic
│   ├── melody_extractor.py   # Melody extraction
│   ├── midi_generator.py     # MIDI file generation
│   ├── converter.py          # Main conversion orchestrator
│   └── cli.py               # Command-line interface
├── output/                   # Generated MIDI files (created automatically)
├── examples/                 # Example audio files
├── requirements.txt          # Python dependencies
├── rnkeys.py                # Main entry point
└── README.md                # This file
```

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## License

MIT License

## Acknowledgments

- [librosa](https://librosa.org/) - Audio analysis library
- [basic-pitch](https://github.com/spotify/basic-pitch) - Spotify's audio-to-MIDI model
- [mido](https://mido.readthedocs.io/) - MIDI file handling
- [music21](https://web.mit.edu/music21/) - Music theory toolkit

## Roadmap

Future enhancements:
- [ ] Web interface for drag-and-drop conversion
- [ ] Better chord recognition (sus chords, extended chords)
- [ ] Rhythm detection and quantization
- [ ] Multiple instrument track separation
- [ ] Real-time audio input support
- [ ] Export to MusicXML format
- [ ] Cloud deployment option

---

Made with ♪ by the RNKeys team
