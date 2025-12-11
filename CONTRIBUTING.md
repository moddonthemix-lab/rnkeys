# Contributing to RNKeys

Thank you for your interest in contributing to RNKeys! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/rnkeys.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit your changes: `git commit -m "Add your descriptive commit message"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Code Style

- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and concise
- Comment complex logic

## Testing

Before submitting a PR:

1. Test with various audio formats (MP3, WAV, FLAC)
2. Test with different genres and styles
3. Verify all command-line options work
4. Check that generated MIDI files are valid

## Areas for Contribution

### High Priority

- Improved chord recognition algorithms
- Better melody extraction accuracy
- Performance optimizations
- Unit tests and integration tests
- Documentation improvements

### Feature Ideas

- Web interface (Flask/FastAPI)
- Batch processing
- Real-time audio input
- Bass line extraction
- Drum pattern detection
- Support for more chord types (sus, add9, etc.)
- MusicXML export
- GUI application

### Bug Fixes

Check the Issues page for known bugs and issues.

## Commit Message Guidelines

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests when relevant

## Pull Request Process

1. Update README.md with details of changes if needed
2. Update requirements.txt if you added dependencies
3. Ensure your code follows the style guidelines
4. Write clear description of changes in PR
5. Link related issues in PR description

## Questions?

Feel free to open an issue for:
- Questions about the codebase
- Feature discussions
- Bug reports
- General feedback

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to RNKeys! 🎵
