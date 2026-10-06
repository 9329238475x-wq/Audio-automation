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

# Verify GPU
assert torch.cuda.is_available(), "GPU must be enabled on Kaggle!"
print(f"🚀 Kaggle GPU Detected: {torch.cuda.get_device_name(0)}")

# Import Chatterbox Multilingual
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

print("Loading Chatterbox Multilingual V3...")
tts_model = ChatterboxMultilingualTTS.from_pretrained(device="cuda", t3_model="v3")
print("Chatterbox V3 Loaded on GPU!")

def enhance_audio_dsp(audio: np.ndarray, sr: int = 24000) -> np.ndarray:
    """Pure Loud Peak Normalization to -0.5 dB (0.95 amplitude) with ZERO artificial effects."""
    peak = np.max(np.abs(audio))
    if peak > 1e-4:
        audio = (audio / peak) * 0.95
    return audio.astype(np.float32)

print("Kaggle Audio DSP ready (Pure Loud Dry Vocal).")
