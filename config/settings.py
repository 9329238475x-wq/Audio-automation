# -*- coding: utf-8 -*-
"""
Studio & Production Settings
Dynamic Cross-Platform Configuration: Works seamlessly on both Windows and Kaggle Linux.
"""
import os
import sys
from pathlib import Path

# Project root: Auto-detects running directory (Works on Kaggle /kaggle/working/ as well as Local PC)
ROOT_DIR = Path(__file__).resolve().parent.parent

ASSETS_DIR = ROOT_DIR / "assets"
CONFIG_DIR = ROOT_DIR / "config"
INPUT_STORIES_DIR = ROOT_DIR / "input_stories"
OUTPUT_DIR = ROOT_DIR / "output"
SCRIPTS_DIR = OUTPUT_DIR / "scripts"
AUDIO_CHUNKS_DIR = OUTPUT_DIR / "audio_chunks"
FINAL_MASTERS_DIR = OUTPUT_DIR / "masters"
BGM_DIR = ASSETS_DIR / "bgm"
SFX_DIR = ASSETS_DIR / "sfx"
SAMPLES_DIR = ROOT_DIR / "voice_samples"

# Ensure runtime directories exist
for d in [INPUT_STORIES_DIR, OUTPUT_DIR, SCRIPTS_DIR, AUDIO_CHUNKS_DIR, FINAL_MASTERS_DIR, SAMPLES_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Audio Standards
SAMPLE_RATE = 24000
AUDIO_FORMAT = "wav"
SPEECH_PAUSE_MS = 380

# Chatterbox V3 Neural Model Configuration (MAIN ENGINE)
DEFAULT_TTS_ENGINE = os.environ.get("TTS_ENGINE", "chatterbox")
CHATTERBOX_MODEL = "chatterbox-v3-mtl"
CHATTERBOX_MTL_VERSION = "multilingual_v3"
TTS_LANGUAGE = "hi"

# Mood presets for emotional nuance in voice synthesis
MOOD_PRESETS = {
    "neutral": {"exaggeration": 0.50, "cfg_weight": 0.25},
    "romantic": {"exaggeration": 0.60, "cfg_weight": 0.28},
    "sad": {"exaggeration": 0.65, "cfg_weight": 0.30},
    "heartbroken": {"exaggeration": 0.70, "cfg_weight": 0.32},
    "crying": {"exaggeration": 0.75, "cfg_weight": 0.35},
    "angry": {"exaggeration": 0.80, "cfg_weight": 0.38},
    "whisper": {"exaggeration": 0.40, "cfg_weight": 0.20},
    "cinematic": {"exaggeration": 0.55, "cfg_weight": 0.27}
}

# Channel Branding
CHANNEL_NAME = os.environ.get("CHANNEL_NAME", "DESI AUDIO STORIES")
