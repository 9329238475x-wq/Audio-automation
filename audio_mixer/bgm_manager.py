# -*- coding: utf-8 -*-
"""
BGM & Atmosphere Manager:
- Long-Sustained (5.5s) Acoustic Grand Piano Chords
  (Each chord holds steady for 4-6 seconds with no rapid level changes)
- Direct untouched authentic Deep-Rain (from c:\Audio-automation\assets\bgm\Deep-Rain.mp3)
- Pure direct audio with volume trim (0.35) and ONLY 5% subtle room reverb as requested
"""

import os
import subprocess
import numpy as np
import soundfile as sf
from scipy import signal
from pathlib import Path
from typing import Optional

from config.settings import BGM_DIR, SAMPLE_RATE, ASSETS_DIR

def apply_reverb(audio: np.ndarray, sr: int = 24000, wet: float = 0.05, decay: float = 0.30) -> np.ndarray:
    """Applies subtle 5% natural room reverb using feedback comb and all-pass filters."""
    from scipy.signal import lfilter
    delays_ms = [29.7, 37.1, 41.1, 43.7]
    comb_outputs = np.zeros_like(audio)

    for d_ms in delays_ms:
        delay_samples = int(d_ms * sr / 1000)
        b = np.zeros(delay_samples + 1)
        b[0] = 1.0
        a = np.zeros(delay_samples + 1)
        a[0] = 1.0
        a[-1] = -decay
        comb_outputs += lfilter(b, a, audio)

    comb_outputs *= 0.25

    for ap_ms in [5.1, 1.7]:
        ap_samples = int(ap_ms * sr / 1000)
        g = 0.5
        b_ap = np.zeros(ap_samples + 1)
        b_ap[0] = -g
        b_ap[-1] = 1.0
        a_ap = np.zeros(ap_samples + 1)
        a_ap[0] = 1.0
        a_ap[-1] = -g
        comb_outputs = lfilter(b_ap, a_ap, comb_outputs)

    return ((1.0 - wet) * audio + wet * comb_outputs).astype(np.float32)

class BGMManager:
    def __init__(self, bgm_dir: Path = BGM_DIR):
        self.bgm_dir = Path(bgm_dir)
        self.bgm_dir.mkdir(parents=True, exist_ok=True)

        # Deep-Rain paths (check bgm subfolder and assets root)
        self.deep_rain_wav = ASSETS_DIR / "bgm" / "Deep-Rain_24k.wav"
        if not self.deep_rain_wav.exists():
            self.deep_rain_wav = ASSETS_DIR / "Deep-Rain_24k.wav"

        self.deep_rain_mp3 = ASSETS_DIR / "bgm" / "Deep-Rain.mp3"
        if not self.deep_rain_mp3.exists():
            self.deep_rain_mp3 = ASSETS_DIR / "Deep-Rain.mp3"

    def get_or_create_bgm(self, mood_cue: str, duration_seconds: float) -> np.ndarray:
        """
        Loads the timtimata hua piano (twinkling/high melody),
        with clean sub-bass (high-pass 120Hz) so it is not jyada deep, normalized with 5% reverb.
        """
        total_samples = int(duration_seconds * SAMPLE_RATE)
        sparkle_file = ASSETS_DIR / "bgm" / "timtimata_piano_leveled_24k.wav"
        if not sparkle_file.exists():
            sparkle_file = ASSETS_DIR / "bgm" / "romantic_sad_piano_24k.wav"

        if sparkle_file.exists():
            with sf.SoundFile(str(sparkle_file)) as f:
                file_samples = len(f)
                if file_samples >= total_samples:
                    raw_data = f.read(total_samples, dtype='float32')
                else:
                    raw = f.read(dtype='float32')
                    loops = (total_samples // file_samples) + 1
                    raw_data = np.tile(raw, loops)[:total_samples]

            if len(raw_data.shape) > 1:
                raw_data = raw_data.mean(axis=1)

            sos = signal.butter(2, 120, btype='highpass', fs=SAMPLE_RATE, output='sos')
            raw_data = signal.sosfilt(sos, raw_data).astype(np.float32)

            peak = np.max(np.abs(raw_data))
            if peak > 1e-4:
                raw_data = raw_data * (0.85 / peak)

            fade_len = int(SAMPLE_RATE * 2.0)
            if len(raw_data) > fade_len * 2:
                raw_data[:fade_len] *= np.linspace(0.0, 1.0, fade_len)
                raw_data[-fade_len:] *= np.linspace(1.0, 0.0, fade_len)

            print(f"  ✨ Using timtimata hua sparkling piano ({duration_seconds:.1}s, 5% reverb)")
            return apply_reverb(raw_data, SAMPLE_RATE, wet=0.05)

        raw_pad = self._generate_sustained_acoustic_piano(duration_seconds)
        return apply_reverb(raw_pad, SAMPLE_RATE, wet=0.05)

    def generate_continuous_rain_ambience(self, duration_seconds: float, volume_factor: float = 0.35) -> np.ndarray:
        """
        Loads the user's authentic Deep-Rain DIRECTLY without ANY editing or filtering.
        Volume trim set to 0.35 so rain creates a realistic rainfall atmosphere without drowning the piano.
        """
        total_samples = int(duration_seconds * SAMPLE_RATE)

        # Convert once if 24k wav doesn't exist
        if not self.deep_rain_wav.exists() and self.deep_rain_mp3.exists():
            print("  Converting Deep-Rain.mp3 directly to 24000Hz WAV...")
            cmd = [
                "ffmpeg", "-y", "-i", str(self.deep_rain_mp3),
                "-ar", str(SAMPLE_RATE), "-ac", "1",
                "-c:a", "pcm_s16le", str(self.deep_rain_wav)
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        if self.deep_rain_wav.exists():
            with sf.SoundFile(str(self.deep_rain_wav)) as f:
                file_samples = len(f)
                if file_samples >= total_samples:
                    raw_data = f.read(total_samples, dtype='float32')
                else:
                    raw = f.read(dtype='float32')
                    loops = (total_samples // file_samples) + 1
                    raw_data = np.tile(raw, loops)[:total_samples]

            if len(raw_data.shape) > 1:
                raw_data = raw_data.mean(axis=1)

            # Direct untouched audio: volume trim (0.35) + only 5% reverb
            direct_rain = raw_data * volume_factor
            print(f"  ✅ Using direct untouched Deep-Rain audio ({duration_seconds:.1f}s, vol={volume_factor:.2f}, 5% reverb)")
            return apply_reverb(direct_rain, SAMPLE_RATE, wet=0.05)

        return np.zeros(total_samples, dtype=np.float32)

    def _generate_sustained_acoustic_piano(self, duration_seconds: float) -> np.ndarray:
        """
        Generates warm, cinematic acoustic grand piano chords where each chord
        sustains smoothly for 5.5 seconds (3 to 6 seconds) without rapid jumping or level changes.
        """
        sr = SAMPLE_RATE
        n_samples = int(duration_seconds * sr)
        out = np.zeros(n_samples, dtype=np.float32)

        # Heart-touching cinematic Desi romance chord progression (Am9 -> Fmaj7 -> Cmaj9 -> Em7)
        chords = [
            [110.0, 164.81, 220.0, 261.63, 329.63, 392.0],  # Am9 (Deep emotional sadness)
            [87.31, 130.81, 174.61, 220.0, 261.63, 329.63], # Fmaj7 (Longing / heartbreak)
            [65.41, 98.0, 130.81, 164.81, 196.0, 246.94],   # Cmaj9 (Nostalgia / memories)
            [82.41, 123.47, 164.81, 196.0, 246.94, 293.66], # Em7 (Melancholy resolution)
        ]

        chord_len = 5.5   # Holds steady for 5.5 seconds (3-6s range as requested)
        crossfade = 2.0   # 2.0s seamless gentle overlap (no abrupt drops)
        step = chord_len - crossfade

        t_chord = np.linspace(0, chord_len, int(chord_len * sr), endpoint=False)

        # Smooth, sustained acoustic envelope:
        # 0.4s gentle felt strike -> steady sustained singing tone -> 1.8s warm dissolve
        env = np.ones_like(t_chord)
        att_s = int(0.4 * sr)
        rel_s = int(1.8 * sr)
        env[:att_s] = 0.5 * (1 - np.cos(np.pi * np.linspace(0, 1, att_s)))
        env[-rel_s:] = 0.5 * (1 + np.cos(np.pi * np.linspace(0, 1, rel_s)))

        pos = 0.0
        idx = 0
        while pos < duration_seconds:
            chord = chords[idx % len(chords)]
            chord_sig = np.zeros_like(t_chord)
            for f in chord:
                # Acoustic piano harmonic dispersion
                chord_sig += 0.45 * np.sin(2 * np.pi * f * t_chord)
                chord_sig += 0.24 * np.sin(2 * np.pi * (2 * f) * t_chord)
                chord_sig += 0.12 * np.sin(2 * np.pi * (3 * f) * t_chord)
                chord_sig += 0.05 * np.sin(2 * np.pi * (4 * f) * t_chord)
                chord_sig += 0.02 * np.sin(2 * np.pi * (5 * f) * t_chord)

            chord_sig = chord_sig * env
            start_i = int(pos * sr)
            end_i = min(n_samples, start_i + len(chord_sig))
            valid_len = end_i - start_i
            out[start_i:end_i] += chord_sig[:valid_len]
            pos += step
            idx += 1

        # Acoustic Soundboard resonance filter: lowpass at 2600Hz removes harsh buzz, leaving velvety wooden tone
        sos = signal.butter(2, 2600, btype='lowpass', fs=sr, output='sos')
        out = signal.sosfilt(sos, out).astype(np.float32)

        # Soundboard body warmth boost at 220Hz
        w0 = 2 * np.pi * 220.0 / sr
        alpha = np.sin(w0) / (2.0 * 1.2)
        A = 10.0 ** (3.0 / 40.0)
        b = np.array([1.0 + alpha * A, -2.0 * np.cos(w0), 1.0 - alpha * A])
        a = np.array([1.0 + alpha / A, -2.0 * np.cos(w0), 1.0 - alpha / A])
        out = signal.lfilter(b / a[0], a / a[0], out).astype(np.float32)

        # Normalize peak to 0.85
        peak = np.max(np.abs(out))
        if peak > 1e-4:
            out = out * (0.85 / peak)

        print(f"  🎹 Generated sustained cinematic acoustic piano ({duration_seconds:.1f}s, 5.5s chord holds, smooth 2s transitions)")
        return out
