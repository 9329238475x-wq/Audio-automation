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

# Ensure runtime directories exist
for d in [INPUT_STORIES_DIR, OUTPUT_DIR, SCRIPTS_DIR, AUDIO_CHUNKS_DIR, FINAL_MASTERS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Audio Standards
SAMPLE_RATE = 24000
AUDIO_FORMAT = "wav"
SPEECH_PAUSE_MS = 380

# Default Engine: 'edge' (Fast, 100% Free & Unlimited) or 'chatterbox' (Neural GPU)
DEFAULT_TTS_ENGINE = os.environ.get("TTS_ENGINE", "edge")
