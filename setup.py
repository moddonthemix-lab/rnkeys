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
    version="1.0.0",
    description="90s R&B MIDI Pattern Generator - Compete with Timbaland and R. Kelly",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="RNKeys Team",
    python_requires=">=3.8",
    packages=find_packages(),
    install_requires=[
        "mido>=1.3.0",
        "music21>=9.1.0",
        "numpy>=1.24.0",
        "click>=8.1.0",
        "rich>=13.0.0",
        "pyyaml>=6.0",
    ],
    entry_points={
        "console_scripts": [
            "rnkeys=src.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Sound/Audio :: MIDI",
        "Topic :: Artistic Software",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="midi music rnb r&b 90s drum pattern generator rhodes synth timbaland production",
)
