# RNKeys - 90s R&B MIDI Pattern Generator

> Compete with Timbaland and R. Kelly 🎹🥁🎵

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

Generate authentic **90s R&B MIDI patterns** with separate tracks for hi-hat, kick, snare/clap, percussion, Rhodes piano chord progressions, and lead synth melodies. All the flavor of classic 90s R&B production, ready to drop into your DAW.

**🌐 Web App + CLI Available!**

## Features

### Drum Patterns
- **Hi-Hat**: Closed, open, and pedal combinations with swing
  - Simple, medium, or complex (Timbaland-style) patterns
  - 16th note grooves with rolls and syncopation
- **Kick**: Classic R&B and hip-hop patterns
  - On-beat emphasis (1 and 3)
  - Syncopated variations
- **Snare/Clap**: Authentic backbeat with ghost notes
  - Mix snare and claps for that thick 90s sound
  - Flams and doubles for extra punch
- **Percussion**: Shakers, tambourines, and congas

### Musical Elements
- **Rhodes Piano**: Soulful, jazzy chord progressions
  - Classic progressions (I-V-vi-IV, vi-IV-I-V, ii-V-I, etc.)
  - Smooth, gospel, or minimal styles
  - Major 7ths, minor 7ths, 9th chords, and more
  - Voice-led inversions for smooth transitions

- **Lead Synth**: Vocal-style melodic lines
  - Pentatonic scales (major, minor, blues)
  - Smooth legato or rhythmic variations
  - Call-and-response patterns
  - Slides and bends

## Installation & Usage

### Option 1: Web App (Easiest!)

**Deploy to Railway in 1 click:**

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

1. Click the button above
2. Connect your GitHub
3. Get your live URL in 2 minutes!

**Or run locally:**
```bash
pip install -r requirements.txt
python app.py
```
Then visit `http://localhost:5000` in your browser!

See [DEPLOY.md](DEPLOY.md) for detailed deployment instructions.

### Option 2: CLI (Command Line)

```bash
# Clone the repository
git clone <repository-url>
cd rnkeys

# Install dependencies
pip install -r requirements.txt

# Generate a beat
python rnkeys.py
```

## Quick Start - CLI

### Generate a Complete Beat

```bash
python rnkeys.py
```

This creates `output/rnkeys_beat.mid` with all elements on separate tracks:
- Track 1: Hi-Hat
- Track 2: Kick
- Track 3: Snare/Clap
- Track 4: Percussion
- Track 5: Rhodes Piano
- Track 6: Lead Synth

Load it into your DAW and you're ready to produce!

## Usage Examples

### Basic Commands

```bash
# Default 8-bar beat at 95 BPM in C
python rnkeys.py

# Slow jam in D at 85 BPM
python rnkeys.py -k D -t 85

# Upbeat track at 110 BPM with 16 bars
python rnkeys.py -t 110 -b 16

# Minor key with blues scale
python rnkeys.py -k Am --scale minor_pentatonic
```

### Style Variations

```bash
# Timbaland-style complex hi-hats
python rnkeys.py --hihat complex

# Gospel-style Rhodes chords
python rnkeys.py --chords gospel

# Rhythmic, syncopated melody
python rnkeys.py --melody rhythmic

# Blues scale lead
python rnkeys.py --scale blues
```

### Generate Individual Elements

```bash
# Drums only (hi-hat, kick, snare, percussion)
python rnkeys.py --drums-only

# Rhodes chord progression only
python rnkeys.py --rhodes-only --chords smooth

# Lead synth melody only
python rnkeys.py --melody-only --scale major_pentatonic
```

### Export Separate Track Files

```bash
# Generate main MIDI + individual files for each track
python rnkeys.py --separate
```

This creates:
- `rnkeys_beat.mid` (all tracks)
- `rnkeys_beat_hihat.mid`
- `rnkeys_beat_kick.mid`
- `rnkeys_beat_snare.mid`
- `rnkeys_beat_percussion.mid`
- `rnkeys_beat_rhodes.mid`
- `rnkeys_beat_lead.mid`

## Command-Line Options

```
Options:
  -o, --output PATH               Output MIDI file path
  -k, --key TEXT                  Musical key (C, D, E, F, G, A, B with # or b)
  -t, --tempo INTEGER             Tempo in BPM (80-120 recommended)
  -b, --bars INTEGER              Number of bars to generate
  --swing FLOAT                   Swing amount (0.0-0.3)
  --hihat [simple|medium|complex] Hi-hat complexity
  --kick [rnb|hiphop]            Kick drum style
  --claps/--no-claps             Mix claps with snare
  --percussion [shaker|tambourine|conga]
  --chords [smooth|gospel|minimal] Rhodes chord style
  --melody [smooth|rhythmic|riff] Lead synth melody style
  --scale [major_pentatonic|minor_pentatonic|blues]
  --separate/--no-separate       Export separate track files
  --drums-only                   Generate drums only
  --rhodes-only                  Generate Rhodes only
  --melody-only                  Generate melody only
  --version                      Show version
  --help                         Show this message
```

## Example Workflows

### 1. Slow R&B Ballad

```bash
python rnkeys.py \
  -k Db -t 72 -b 8 \
  --swing 0.15 \
  --hihat simple \
  --chords smooth \
  --melody smooth \
  --scale minor_pentatonic
```

### 2. Upbeat Timbaland-Style Track

```bash
python rnkeys.py \
  -k G -t 105 -b 16 \
  --hihat complex \
  --kick hiphop \
  --chords gospel \
  --melody rhythmic
```

### 3. Minimal Late-Night Vibe

```bash
python rnkeys.py \
  -k Em -t 88 \
  --hihat simple \
  --percussion shaker \
  --chords minimal \
  --melody smooth \
  --scale blues
```

### 4. Build Your Own Beat Piece by Piece

```bash
# Generate drums
python rnkeys.py --drums-only -o output/drums.mid -t 95 -k C

# Generate chords
python rnkeys.py --rhodes-only -o output/chords.mid -t 95 -k C

# Generate melody
python rnkeys.py --melody-only -o output/melody.mid -t 95 -k C

# Import all three into your DAW!
```

## Technical Details

### 90s R&B Production Characteristics

This generator captures authentic 90s R&B elements:

**Rhythmic Features:**
- Swing timing (not perfectly straight)
- Syncopated hi-hat patterns with rolls
- Kick drums on 1 and 3 with occasional syncopation
- Snare/clap on 2 and 4 (the backbeat)
- Ghost notes for humanization
- Layered snare + clap for thickness

**Harmonic Features:**
- Jazzy chord progressions (ii-V-I, I-vi-IV-V)
- Extended chords (7ths, 9ths, 6ths)
- Smooth voice leading and inversions
- Gospel-influenced chord movement

**Melodic Features:**
- Pentatonic and blues scales (easy to sing over)
- Vocal-style phrasing with rests
- Slides and neighbor tones
- Call-and-response patterns

### MIDI Implementation

- **Ticks Per Beat**: 480 (high resolution)
- **Drum Channel**: Channel 9 (GM standard)
- **Rhodes**: Program 4 (Electric Piano)
- **Lead Synth**: Program 81 (Lead Synth)
- **Velocity Variations**: Humanized velocities for natural feel
- **Timing**: Micro-timing variations for groove

## DAW Integration

### Recommended Workflow

1. **Generate MIDI** with RNKeys
2. **Import** into your DAW (Ableton, FL Studio, Logic, etc.)
3. **Assign Sounds**:
   - Load your favorite drum samples
   - Use a Rhodes VST (Neo-Soul Keys, Lounge Lizard, etc.)
   - Add a lead synth (Omnisphere, Serum, etc.)
4. **Customize**:
   - Adjust velocities
   - Add effects (reverb, compression)
   - Layer additional sounds
5. **Produce** your 90s R&B masterpiece!

### Compatible with All DAWs

- Ableton Live
- FL Studio
- Logic Pro
- Pro Tools
- Cubase
- Studio One
- Reaper
- GarageBand
- Any DAW that supports MIDI import

## Project Structure

```
rnkeys/
├── src/
│   ├── __init__.py            # Package init
│   ├── drum_generator.py      # Hi-hat, kick, snare, percussion
│   ├── chord_generator.py     # Rhodes chord progressions
│   ├── melody_generator.py    # Lead synth melodies
│   ├── midi_exporter.py       # MIDI file creation
│   ├── generator.py           # Main orchestrator
│   └── cli.py                 # Command-line interface
├── output/                     # Generated MIDI files
├── requirements.txt            # Dependencies
├── rnkeys.py                  # Entry point
└── README.md                  # This file
```

## Tips for Best Results

1. **Tempo Sweet Spots**:
   - Ballads: 70-85 BPM
   - Mid-tempo R&B: 85-100 BPM
   - Upbeat jams: 100-115 BPM

2. **Key Choices**:
   - C, F, G - Classic and bright
   - Db, Eb, Ab - Smooth and soulful
   - D, A, E - Energetic

3. **Style Combinations**:
   - Smooth + Major Pentatonic = Classic R&B
   - Gospel + Minor Pentatonic = Emotional ballad
   - Rhythmic + Blues = Funky groove

4. **Layering**:
   - Generate multiple variations
   - Layer different patterns
   - Mix and match elements

## Contributing

Want to add more patterns or improve the generator? Contributions welcome!

1. Fork the repository
2. Create your feature branch
3. Make your changes
4. Submit a pull request

Ideas for contributions:
- More drum pattern variations
- Additional chord progressions
- New percussion sounds
- Bass line generator
- Vocal melody generator
- Preset configurations
- More scale options

## License

MIT License - see LICENSE file

## Credits

Inspired by the legendary production of:
- **Timbaland** - Innovative drums and percussion
- **R. Kelly** - Soulful melodies and progressions
- **Teddy Riley** - New Jack Swing pioneers
- **Jimmy Jam & Terry Lewis** - Smooth R&B production

## Support

Found a bug? Want a feature? Open an issue!

---

**Make those 90s R&B hits!** 🎵🔥

Load your MIDI into your DAW, add your vocals, and you're ready to create that timeless R&B sound.
