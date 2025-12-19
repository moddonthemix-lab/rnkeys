// RNKeys Web App JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('generateForm');
    const generateBtn = document.getElementById('generateBtn');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    const error = document.getElementById('error');
    const swingSlider = document.getElementById('swing');
    const swingValue = document.getElementById('swingValue');
    const modeButtons = document.querySelectorAll('.mode-btn');
    const modeInput = document.getElementById('mode');

    // Update swing value display
    swingSlider.addEventListener('input', function() {
        swingValue.textContent = this.value;
    });

    // Mode button handling
    modeButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            modeButtons.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            const mode = this.dataset.mode;
            modeInput.value = mode;

            // Show/hide sections based on mode
            const drumSettings = document.getElementById('drumSettings');
            const musicalSettings = document.getElementById('musicalSettings');

            if (mode === 'drums') {
                drumSettings.style.display = 'block';
                musicalSettings.style.display = 'none';
            } else if (mode === 'rhodes') {
                drumSettings.style.display = 'none';
                musicalSettings.style.display = 'block';
                // Hide melody-specific settings
                document.getElementById('melody').closest('.form-group').style.display = 'none';
                document.getElementById('scale').closest('.form-group').style.display = 'none';
            } else if (mode === 'melody') {
                drumSettings.style.display = 'none';
                musicalSettings.style.display = 'block';
                // Hide chord-specific settings
                document.getElementById('chords').closest('.form-group').style.display = 'none';
            } else {
                drumSettings.style.display = 'block';
                musicalSettings.style.display = 'block';
                // Show all
                document.getElementById('melody').closest('.form-group').style.display = 'flex';
                document.getElementById('scale').closest('.form-group').style.display = 'flex';
                document.getElementById('chords').closest('.form-group').style.display = 'flex';
            }
        });
    });

    // Form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Hide previous results/errors
        results.style.display = 'none';
        error.style.display = 'none';
        loading.style.display = 'block';
        generateBtn.disabled = true;

        // Collect form data
        const formData = {
            key: document.getElementById('key').value,
            tempo: document.getElementById('tempo').value,
            bars: document.getElementById('bars').value,
            swing: document.getElementById('swing').value,
            hihat: document.getElementById('hihat').value,
            kick: document.getElementById('kick').value,
            claps: document.getElementById('claps').checked,
            percussion: document.getElementById('percussion').value,
            chords: document.getElementById('chords').value,
            melody: document.getElementById('melody').value,
            scale: document.getElementById('scale').value,
            separate: document.getElementById('separate').checked,
            mode: document.getElementById('mode').value
        };

        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            loading.style.display = 'none';
            generateBtn.disabled = false;

            if (data.success) {
                // Show download links
                const downloadLinksDiv = document.getElementById('downloadLinks');
                downloadLinksDiv.innerHTML = '';

                // Track name mapping
                const trackNames = {
                    'complete': '🎵 Complete Beat',
                    'hihat': '🎩 Hi-Hat',
                    'kick': '🥾 Kick',
                    'snare': '👏 Snare/Clap',
                    'percussion': '🪘 Percussion',
                    'rhodes': '🎹 Rhodes Piano',
                    'lead': '🎸 Lead Synth'
                };

                for (const [trackType, url] of Object.entries(data.files)) {
                    const link = document.createElement('a');
                    link.href = url;
                    link.className = 'download-link';
                    link.textContent = `Download ${trackNames[trackType] || trackType}`;
                    link.download = '';
                    downloadLinksDiv.appendChild(link);
                }

                results.style.display = 'block';

                // Scroll to results
                results.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            } else {
                throw new Error(data.error || 'Generation failed');
            }
        } catch (err) {
            loading.style.display = 'none';
            generateBtn.disabled = false;

            document.getElementById('errorMessage').textContent = err.message;
            error.style.display = 'block';

            // Scroll to error
            error.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    });
});
