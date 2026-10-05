import re
# -*- coding: utf-8 -*-
"""
Edge TTS Fast Testing Engine
Enables rapid prototyping & listening to full story dialogue flow, pacing, and BGM mixing locally.
Provides distinct character voices (Narrator vs Hero vs Heroine) with cinema acoustic profiles.
"""

import os
import asyncio
import subprocess
import edge_tts
from pathlib import Path
from typing import Optional, Dict, Any

from voice_engine.text_normalizer import normalize_hindi_text
from voice_engine.audio_enhancer import enhance_audio
from config.settings import SAMPLE_RATE

# Distinct Voice Profiles for Edge TTS Testing Mode
# English Character Profiles for Bilingual Multi-Speaker Audio Drama
EDGE_ENGLISH_PROFILES = {
    "NARRATOR": {
        "voice": "en-US-BrianNeural",
        "base_pitch": "-4Hz",
        "base_rate": "-4%"
    },
    "HERO": {
        "voice": "en-US-GuyNeural",
        "base_pitch": "+3Hz",
        "base_rate": "+2%"
    },
    "HEROINE": {
        "voice": "en-US-JennyNeural",
        "base_pitch": "-3Hz",
        "base_rate": "-4%"
    },
    "MOTHER": {
        "voice": "en-US-JennyNeural",
        "base_pitch": "-6Hz",
        "base_rate": "-6%"
    },
    "RIVAL": {
        "voice": "en-US-ChristopherNeural",
        "base_pitch": "-4Hz",
        "base_rate": "-2%"
    }
}

EDGE_CHARACTER_PROFILES = {
    # Narrator: Mature, deep, serious storyteller baritone
    "NARRATOR": {
        "voice": "hi-IN-MadhurNeural",
        "base_pitch": "-14Hz",
        "base_rate": "-7%"
    },
    # Hero (Kabir): Young, emotional male tenor (distinct from narrator)
    "HERO": {
        "voice": "hi-IN-MadhurNeural",
        "base_pitch": "+6Hz",
        "base_rate": "+3%"
    },
    # Heroine (Aarushi): Warm, velvety, emotional young female (lowered pitch to eliminate screechiness)
    "HEROINE": {
        "voice": "hi-IN-SwaraNeural",
        "base_pitch": "-5Hz",
        "base_rate": "-6%"
    },
    # Mother: Warm, gentle elderly female
    "MOTHER": {
        "voice": "hi-IN-SwaraNeural",
        "base_pitch": "-8Hz",
        "base_rate": "-8%"
    },
    # Rival: Harsh, confrontational male
    "RIVAL": {
        "voice": "hi-IN-MadhurNeural",
        "base_pitch": "-8Hz",
        "base_rate": "-5%"
    }
}

class EdgeTTSVoiceEngine:
    def __init__(self):
        print("[VoiceEngine] ⚡ Edge TTS Engine Initialized (Testing Mode: Distinct Character Voices)")

    def synthesize_segment(
        self,
        text: str,
        output_path: Path,
        character: str = "NARRATOR",
        mood: str = "romantic",
        auto_enhance: bool = True,
        **kwargs
    ) -> Path:
        """
        Synthesizes spoken audio for a segment using Edge TTS with distinct character acoustic profiles.
        """
        clean_text = normalize_hindi_text(text)
        if not clean_text:
            raise ValueError("Input text is empty after normalization.")

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        raw_mp3 = output_path.with_suffix(".temp.mp3")
        raw_wav = output_path.with_suffix(".raw.wav")

        char_key = character.upper()
        is_english = len(re.findall(r'[a-zA-Z]', clean_text)) > len(re.findall(r'[ऀ-ॿ]', clean_text))
        if is_english:
            profile = EDGE_ENGLISH_PROFILES.get(char_key, EDGE_ENGLISH_PROFILES["NARRATOR"])
        else:
            profile = EDGE_CHARACTER_PROFILES.get(char_key, EDGE_CHARACTER_PROFILES["NARRATOR"])
        voice = profile["voice"]
        pitch = profile["base_pitch"]
        rate = profile["base_rate"]

        # Dynamic mood adjustments without losing character persona
        if char_key == "HERO":
            if mood in ("sad", "heartbroken", "crying"):
                rate = "-4%"
                pitch = "+3Hz"
        elif char_key == "HEROINE":
            if mood in ("crying", "heartbroken"):
                rate = "-7%"
                pitch = "-6Hz"   # Tearful, intimate, velvety (NO piercing high frequencies)
            elif mood == "whisper":
                rate = "-10%"
                pitch = "-7Hz"
        elif char_key == "NARRATOR":
            if mood == "romantic":
                rate = "-5%"

        print(f"  [VoiceEngine:EdgeTTS] [{char_key}] Mood: {mood} | Voice: {voice} (Pitch: {pitch}, Rate: {rate})")
        print(f"    Text: \"{clean_text[:50]}...\"")

        # Run async edge_tts
        async def _speak():
            for attempt in range(8):
                try:
                    comm = edge_tts.Communicate(clean_text, voice=voice, rate=rate, pitch=pitch)
                    await comm.save(str(raw_mp3))
                    return
                except Exception as e:
                    if attempt < 7:
                        wait_t = 3 * (attempt + 1)
                        print(f"    [EdgeTTS Warning] Net/DNS retry {attempt+1}/8 in {wait_t}s: {e}", flush=True)
                        await asyncio.sleep(wait_t)
                    else:
                        raise e

        # Skip if already synthesized
        if output_path.exists() and output_path.stat().st_size > 2000:
            return output_path

        asyncio.run(_speak())

        # Convert to 24000Hz 16-bit PCM WAV via FFmpeg
        cmd = [
            "ffmpeg", "-y", "-i", str(raw_mp3),
            "-ar", str(SAMPLE_RATE), "-ac", "1",
            "-c:a", "pcm_s16le", str(raw_wav)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        if raw_mp3.exists():
            try:
                raw_mp3.unlink()
            except Exception:
                pass

        # Apply Cinema Quality Audio Enhancement tailored for character acoustics
        if auto_enhance:
            enhance_audio(raw_wav, output_path, sr=SAMPLE_RATE, character=char_key)
            if raw_wav.exists():
                try:
                    raw_wav.unlink()
                except Exception:
                    pass
        else:
            if raw_wav.exists():
                raw_wav.rename(output_path)

        return output_path
