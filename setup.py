"""
Setup script for RNKeys
"""
from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="rnkeys",
    version="0.1.0",
    description="Convert audio files to MIDI with automatic chord and melody detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="RNKeys Team",
    python_requires=">=3.8",
    packages=find_packages(),
    install_requires=[
        "librosa>=0.10.0",
        "soundfile>=0.12.0",
        "numpy>=1.24.0",
        "scipy>=1.10.0",
        "mido>=1.3.0",
        "music21>=9.1.0",
        "basic-pitch>=0.2.5",
        "pychord>=0.5.3",
        "click>=8.1.0",
        "rich>=13.0.0",
        "tqdm>=4.65.0",
    ],
    entry_points={
        "console_scripts": [
            "rnkeys=src.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
        "Topic :: Multimedia :: Sound/Audio :: MIDI",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="audio midi music chord melody converter",
)
