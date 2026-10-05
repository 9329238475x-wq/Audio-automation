# -*- coding: utf-8 -*-
"""
SFX Manager: Handles foley, environmental ambience, and emotional sound effects.
"""

import os
import numpy as np
import soundfile as sf
from pathlib import Path
from typing import Optional

from config.settings import SFX_DIR, SAMPLE_RATE

class SFXManager:
    def __init__(self, sfx_dir: Path = SFX_DIR):
        self.sfx_dir = Path(sfx_dir)
        self.sfx_dir.mkdir(parents=True, exist_ok=True)

    def get_or_create_sfx(self, sfx_cue: str, max_duration_s: float = 4.0) -> Optional[np.ndarray]:
        """
        Loads matching SFX from assets/sfx/ or synthesizes procedural sound effect.
        """
        if not sfx_cue or sfx_cue == "none":
            return None

        # 1. Check custom assets
        for ext in (".wav", ".mp3"):
            potential_file = self.sfx_dir / f"{sfx_cue}{ext}"
            if potential_file.exists():
                try:
                    data, sr = sf.read(str(potential_file), dtype='float32')
                    if len(data.shape) > 1:
                        data = data.mean(axis=1)
                    return data
                except Exception:
                    pass

        # 2. Procedural Foley Synthesis
        return self._synthesize_procedural_sfx(sfx_cue, max_duration_s)

    def _synthesize_procedural_sfx(self, cue: str, dur_s: float) -> np.ndarray:
        samples = int(SAMPLE_RATE * dur_s)
        t = np.linspace(0, dur_s, samples, endpoint=False)

        if "rain" in cue:
            # Pink noise filtered for rain sound
            noise = np.random.normal(0, 0.08, samples)
            # Low rumble
            rumble = 0.05 * np.sin(2 * np.pi * 55 * t) * np.exp(-t * 0.5)
            return (noise + rumble).astype(np.float32)

        elif "heartbeat" in cue:
            # Double thump pulse
            audio = np.zeros(samples, dtype=np.float32)
            for cycle in range(int(dur_s * 1.5)):
                t_sub = t - (cycle * 0.7)
                mask1 = (t_sub >= 0) & (t_sub < 0.15)
                mask2 = (t_sub >= 0.2) & (t_sub < 0.35)
                audio[mask1] += 0.25 * np.sin(2 * np.pi * 60 * t_sub[mask1]) * np.exp(-t_sub[mask1] * 20)
                audio[mask2] += 0.18 * np.sin(2 * np.pi * 55 * (t_sub[mask2] - 0.2)) * np.exp(-(t_sub[mask2] - 0.2) * 20)
            return audio

        elif "paper" in cue:
            # Paper rustle: high-frequency bursts of noise
            noise = np.random.normal(0, 0.12, samples)
            burst = np.sin(2 * np.pi * 4 * t) ** 4
            return (noise * burst * np.exp(-t * 1.5)).astype(np.float32)

        else:
            # Gentle cinematic whoosh
            env = np.sin(np.pi * (t / dur_s)) ** 2
            noise = np.random.normal(0, 0.04, samples)
            return (noise * env).astype(np.float32)
