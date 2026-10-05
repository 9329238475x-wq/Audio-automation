# -*- coding: utf-8 -*-
"""
Self-contained Kaggle Pipeline Runner for Chatterbox V3 GPU Audio Generation.
"""

import os
import sys
import gc
import json
import torch
import soundfile as sf
import numpy as np
from pathlib import Path
from scipy import signal

# Verify GPU
assert torch.cuda.is_available(), "GPU must be enabled on Kaggle!"
print(f"🚀 Kaggle GPU Detected: {torch.cuda.get_device_name(0)}")

# Import Chatterbox Multilingual
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

print("Loading Chatterbox Multilingual V3...")
tts_model = ChatterboxMultilingualTTS.from_pretrained(device="cuda", t3_model="v3")
print("✅ Chatterbox V3 Loaded on GPU!")

def enhance_audio_dsp(audio: np.ndarray, sr: int = 24000) -> np.ndarray:
    """Step 11 Cinema Quality DSP: Presence EQ + Compressor + Loudness Normalize"""
    # 1. Peaking EQ 3kHz
    center_freq = 3000.0
    bandwidth = 2000.0
    boost_db = 4.5
    w0 = 2 * np.pi * center_freq / sr
    alpha = np.sin(w0) / (2.0 * (bandwidth / sr))
    A = 10.0 ** (boost_db / 40.0)
    b = np.array([1.0 + alpha * A, -2.0 * np.cos(w0), 1.0 - alpha * A])
    a = np.array([1.0 + alpha / A, -2.0 * np.cos(w0), 1.0 - alpha / A])
    b = b / a[0]
    a = a / a[0]
    try:
        audio = signal.filtfilt(b, a, audio)
    except Exception:
        audio = signal.lfilter(b, a, audio)

    # 2. Dynamic Compressor
    rms = np.sqrt(np.mean(audio**2))
    rms_db = 20 * np.log10(max(rms, 1e-10))
    gain_db = -23.0 - rms_db
    audio = audio * (10.0 ** (gain_db / 20.0))

    # 3. Soft Limiting
    peak = np.max(np.abs(audio))
    if peak > 0.95:
        audio = audio * (0.94 / peak)
    return audio.astype(np.float32)

print("Kaggle Audio DSP ready.")
