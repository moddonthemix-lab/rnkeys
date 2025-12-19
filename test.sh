#!/bin/bash
# Quick test script for RNKeys

echo "🎵 Testing RNKeys..."
echo ""

# Test imports
echo "1. Testing imports..."
python3 -c "
from src.generator import RNKeysGenerator
from src.drum_generator import DrumPatternGenerator
from src.chord_generator import RhodesChordGenerator
from src.melody_generator import LeadSynthGenerator
from src.midi_exporter import MIDIExporter
print('✓ All imports successful')
"

if [ $? -ne 0 ]; then
    echo "✗ Import failed. Install dependencies:"
    echo "  pip install -r requirements.txt"
    exit 1
fi

# Test generation
echo ""
echo "2. Testing MIDI generation..."
python3 -c "
from src.generator import RNKeysGenerator
import os

gen = RNKeysGenerator(key='C', tempo=95, bars=4)
files = gen.generate_complete_beat(
    output_path='test_beat.mid',
    hihat_complexity='medium',
    kick_style='rnb',
    use_claps=True,
    percussion_type='shaker',
    chord_style='smooth',
    melody_style='smooth',
    melody_scale='major_pentatonic',
    separate_tracks=False
)

if os.path.exists('test_beat.mid'):
    size = os.path.getsize('test_beat.mid')
    print(f'✓ MIDI file created ({size} bytes)')
    os.remove('test_beat.mid')
else:
    print('✗ MIDI file not created')
    exit(1)
" 2>&1 | grep -E "✓|✗"

if [ $? -ne 0 ]; then
    echo "✗ Generation failed"
    exit 1
fi

echo ""
echo "3. Testing web app..."
python3 -c "
from app import app
print('✓ Flask app loads successfully')
"

if [ $? -ne 0 ]; then
    echo "✗ Web app failed to load"
    exit 1
fi

echo ""
echo "🎉 All tests passed!"
echo ""
echo "To run the web app:"
echo "  python app.py"
echo ""
echo "Or use the CLI:"
echo "  python rnkeys.py"
