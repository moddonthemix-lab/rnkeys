"""
RNKeys Web Application
Flask web interface for generating 90s R&B MIDI patterns
"""
from flask import Flask, render_template, request, send_file, jsonify, url_for
from flask_cors import CORS
import os
import tempfile
import uuid
from pathlib import Path
import time
import threading

from src.generator import RNKeysGenerator

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output', 'web')
# Ensure directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

print(f"Output folder: {UPLOAD_FOLDER}")
print(f"Output folder exists: {os.path.exists(UPLOAD_FOLDER)}")

# Cleanup old files periodically
def cleanup_old_files():
    """Remove files older than 1 hour"""
    while True:
        try:
            now = time.time()
            for file_path in Path(UPLOAD_FOLDER).glob('*.mid'):
                if now - file_path.stat().st_mtime > 3600:  # 1 hour
                    file_path.unlink()
        except Exception as e:
            print(f"Cleanup error: {e}")
        time.sleep(600)  # Run every 10 minutes

# Start cleanup thread
cleanup_thread = threading.Thread(target=cleanup_old_files, daemon=True)
cleanup_thread.start()


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    """Generate MIDI patterns based on form input"""
    try:
        # Get form data
        data = request.json if request.is_json else request.form.to_dict()

        key = data.get('key', 'C')
        tempo = int(data.get('tempo', 95))
        bars = int(data.get('bars', 8))
        swing = float(data.get('swing', 0.1))

        hihat = data.get('hihat', 'medium')
        kick = data.get('kick', 'rnb')

        # Handle boolean values (can be bool or string)
        claps_val = data.get('claps', True)
        claps = claps_val if isinstance(claps_val, bool) else str(claps_val).lower() == 'true'

        percussion = data.get('percussion', 'shaker')

        chords = data.get('chords', 'smooth')
        melody = data.get('melody', 'smooth')
        scale = data.get('scale', 'major_pentatonic')

        # Handle boolean values (can be bool or string)
        separate_val = data.get('separate', False)
        separate = separate_val if isinstance(separate_val, bool) else str(separate_val).lower() == 'true'

        mode = data.get('mode', 'complete')  # complete, drums, rhodes, melody

        # Generate unique filename
        file_id = str(uuid.uuid4())[:8]
        output_name = f"rnkeys_{file_id}"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{output_name}.mid")

        # Create generator
        generator = RNKeysGenerator(
            key=key,
            tempo=tempo,
            bars=bars,
            swing=swing
        )

        files = {}

        # Generate based on mode
        if mode == 'drums':
            generator.generate_drums_only(
                output_path=output_path,
                hihat_complexity=hihat,
                kick_style=kick,
                use_claps=claps,
                percussion_type=percussion
            )
            files['complete'] = output_path

        elif mode == 'rhodes':
            generator.generate_rhodes_only(
                output_path=output_path,
                style=chords
            )
            files['complete'] = output_path

        elif mode == 'melody':
            generator.generate_melody_only(
                output_path=output_path,
                style=melody,
                scale=scale
            )
            files['complete'] = output_path

        else:  # complete
            files = generator.generate_complete_beat(
                output_path=output_path,
                hihat_complexity=hihat,
                kick_style=kick,
                use_claps=claps,
                percussion_type=percussion,
                chord_style=chords,
                melody_style=melody,
                melody_scale=scale,
                separate_tracks=separate
            )

        # Convert file paths to download URLs
        download_urls = {}
        for track_type, file_path in files.items():
            filename = os.path.basename(file_path)
            download_urls[track_type] = url_for('download_file', filename=filename, _external=True)

        return jsonify({
            'success': True,
            'files': download_urls,
            'message': 'Beat generated successfully! 🎵'
        })

    except Exception as e:
        print(f"Error generating beat: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/download/<filename>')
def download_file(filename):
    """Download a generated MIDI file"""
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print(f"Download requested: {filename}")
        print(f"Looking for file at: {file_path}")
        print(f"File exists: {os.path.exists(file_path)}")

        if os.path.exists(file_path):
            return send_file(
                file_path,
                as_attachment=True,
                download_name=filename,
                mimetype='audio/midi'
            )
        else:
            # List files in directory for debugging
            try:
                files = os.listdir(app.config['UPLOAD_FOLDER'])
                print(f"Files in directory: {files}")
            except:
                pass
            return jsonify({'error': f'File not found: {filename}'}), 404
    except Exception as e:
        print(f"Download error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'RNKeys'})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
