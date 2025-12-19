"""
90s R&B Drum Pattern Generator
Generates authentic hi-hat, kick, snare/clap patterns
"""
import random
import numpy as np
from typing import List, Tuple, Dict
from dataclasses import dataclass


@dataclass
class DrumHit:
    """Represents a single drum hit"""
    time: float  # Time in beats
    velocity: int  # MIDI velocity (0-127)
    note: int  # MIDI note number


class DrumPatternGenerator:
    """Generates 90s R&B style drum patterns"""

    # MIDI note mappings (General MIDI Drum Map)
    KICK = 36
    SNARE = 38
    CLAP = 39
    CLOSED_HH = 42
    OPEN_HH = 46
    PEDAL_HH = 44
    CRASH = 49
    RIDE = 51

    def __init__(self, bars: int = 4, swing: float = 0.1):
        """
        Initialize drum pattern generator

        Args:
            bars: Number of bars to generate (4 beats per bar)
            swing: Amount of swing (0.0 = straight, 0.1 = slight swing, 0.3 = heavy swing)
        """
        self.bars = bars
        self.swing = swing
        self.beats = bars * 4

    def generate_hihat_pattern(self, complexity: str = "medium") -> List[DrumHit]:
        """
        Generate hi-hat pattern (closed, open, pedal)

        Args:
            complexity: "simple", "medium", "complex" (Timbaland style)

        Returns:
            List of hi-hat hits
        """
        hits = []

        if complexity == "simple":
            # Straight 8ths or 16ths
            for bar in range(self.bars):
                for beat in range(4):
                    time = bar * 4 + beat
                    # 8th notes
                    hits.append(DrumHit(time, random.randint(80, 100), self.CLOSED_HH))
                    hits.append(DrumHit(time + 0.5, random.randint(60, 80), self.CLOSED_HH))

        elif complexity == "medium":
            # 16th notes with variations
            for bar in range(self.bars):
                for beat in range(4):
                    time = bar * 4 + beat
                    # 16th notes
                    for sixteenth in range(4):
                        t = time + sixteenth * 0.25
                        t = self._apply_swing(t)

                        # Vary velocity for groove
                        if sixteenth == 0:
                            vel = random.randint(90, 110)
                        elif sixteenth == 2:
                            vel = random.randint(70, 90)
                        else:
                            vel = random.randint(50, 70)

                        # Occasional open hi-hat
                        if random.random() < 0.1:
                            hits.append(DrumHit(t, vel, self.OPEN_HH))
                        else:
                            hits.append(DrumHit(t, vel, self.CLOSED_HH))

        else:  # complex - Timbaland style
            # Syncopated 16ths with rolls and triplets
            for bar in range(self.bars):
                for beat in range(4):
                    time = bar * 4 + beat

                    # Add main 16th pattern
                    pattern = [True, False, True, True] if random.random() > 0.5 else [True, True, False, True]

                    for i, should_hit in enumerate(pattern):
                        if should_hit:
                            t = time + i * 0.25
                            t = self._apply_swing(t)
                            vel = random.randint(60, 100)

                            # Mix closed and open
                            if i == 3 and random.random() < 0.3:
                                hits.append(DrumHit(t, vel, self.OPEN_HH))
                            else:
                                hits.append(DrumHit(t, vel, self.CLOSED_HH))

                    # Add occasional rolls
                    if random.random() < 0.15:
                        roll_start = time + 0.75
                        for r in range(4):
                            hits.append(DrumHit(
                                roll_start + r * 0.0625,
                                random.randint(70, 90),
                                self.CLOSED_HH
                            ))

        return sorted(hits, key=lambda x: x.time)

    def generate_kick_pattern(self, style: str = "rnb") -> List[DrumHit]:
        """
        Generate kick drum pattern

        Args:
            style: "rnb" (on 1 and 3 with variations) or "hiphop" (more syncopated)

        Returns:
            List of kick hits
        """
        hits = []

        for bar in range(self.bars):
            for beat in range(4):
                time = bar * 4 + beat

                if style == "rnb":
                    # Kick on 1 and 3 (main beats)
                    if beat == 0 or beat == 2:
                        hits.append(DrumHit(time, random.randint(110, 127), self.KICK))

                        # Occasional extra kick
                        if random.random() < 0.3:
                            hits.append(DrumHit(
                                time + 0.75,
                                random.randint(80, 100),
                                self.KICK
                            ))
                    # Syncopated kick
                    elif random.random() < 0.2:
                        hits.append(DrumHit(
                            time + random.choice([0.25, 0.5, 0.75]),
                            random.randint(90, 110),
                            self.KICK
                        ))
                else:  # hiphop style
                    if beat == 0:
                        hits.append(DrumHit(time, random.randint(110, 127), self.KICK))
                    elif beat == 2:
                        # Sometimes skip beat 3
                        if random.random() > 0.2:
                            hits.append(DrumHit(time, random.randint(100, 120), self.KICK))
                    elif random.random() < 0.3:
                        # Syncopation
                        hits.append(DrumHit(
                            time + random.choice([0.5, 0.75]),
                            random.randint(90, 110),
                            self.KICK
                        ))

        return sorted(hits, key=lambda x: x.time)

    def generate_snare_pattern(self, use_claps: bool = False) -> List[DrumHit]:
        """
        Generate snare/clap pattern

        Args:
            use_claps: If True, mix in claps for that 90s flavor

        Returns:
            List of snare/clap hits
        """
        hits = []
        snare_note = self.CLAP if use_claps else self.SNARE

        for bar in range(self.bars):
            for beat in range(4):
                time = bar * 4 + beat

                # Main snare on 2 and 4 (backbeat)
                if beat == 1 or beat == 3:
                    hits.append(DrumHit(time, random.randint(100, 120), snare_note))

                    # Layer snare + clap for that thick sound
                    if use_claps and random.random() > 0.5:
                        other_note = self.SNARE if snare_note == self.CLAP else self.CLAP
                        hits.append(DrumHit(time, random.randint(90, 110), other_note))

                # Ghost notes
                elif random.random() < 0.15:
                    hits.append(DrumHit(
                        time + random.choice([0.25, 0.5, 0.75]),
                        random.randint(30, 50),
                        self.SNARE
                    ))

                # Occasional flam (double hit for thickness)
                if (beat == 1 or beat == 3) and random.random() < 0.3:
                    hits.append(DrumHit(time - 0.03125, random.randint(60, 80), snare_note))

        return sorted(hits, key=lambda x: x.time)

    def generate_percussion(self, perc_type: str = "shaker") -> List[DrumHit]:
        """
        Generate percussion patterns (shaker, tambourine, conga)

        Args:
            perc_type: "shaker", "tambourine", "conga"

        Returns:
            List of percussion hits
        """
        hits = []

        # MIDI note mappings for percussion
        perc_notes = {
            "shaker": 70,  # Maracas
            "tambourine": 54,  # Tambourine
            "conga": 62,  # High Conga
        }

        note = perc_notes.get(perc_type, 70)

        if perc_type == "shaker":
            # Steady 8th or 16th notes
            for bar in range(self.bars):
                for beat in range(4):
                    time = bar * 4 + beat
                    for eighth in range(2):
                        t = time + eighth * 0.5
                        t = self._apply_swing(t)
                        vel = random.randint(40, 60)
                        hits.append(DrumHit(t, vel, note))

        elif perc_type == "tambourine":
            # Accent on 2 and 4 like snare
            for bar in range(self.bars):
                for beat in range(4):
                    time = bar * 4 + beat
                    if beat == 1 or beat == 3:
                        hits.append(DrumHit(time, random.randint(70, 90), note))
                    elif random.random() < 0.3:
                        hits.append(DrumHit(time, random.randint(40, 60), note))

        else:  # conga
            # Syncopated conga hits
            for bar in range(self.bars):
                for beat in range(4):
                    time = bar * 4 + beat
                    if random.random() < 0.4:
                        t = time + random.choice([0, 0.25, 0.5, 0.75])
                        vel = random.randint(60, 90)
                        hits.append(DrumHit(t, vel, note))

        return sorted(hits, key=lambda x: x.time)

    def _apply_swing(self, time: float) -> float:
        """Apply swing to timing"""
        if self.swing == 0:
            return time

        # Check if this is an off-beat (not on the beat)
        beat_position = time % 1
        if 0.2 < beat_position < 0.8:
            # Apply swing to off-beats
            return time + self.swing * 0.1

        return time
