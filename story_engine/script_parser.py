# -*- coding: utf-8 -*-
"""
Script Parser: Validates and prepares scenes for voice synthesis and studio mixing.
"""

import json
from pathlib import Path
from typing import List, Dict, Any

from config.settings import MOOD_PRESETS, SAMPLES_DIR

class ScriptParser:
    def __init__(self, voices_config_path: Path):
        self.voices_config = {}
        if voices_config_path.exists():
            with open(voices_config_path, "r", encoding="utf-8") as f:
                raw = json.load(f)
                self.voices_config = raw.get("genres", {}).get("desi_romance_drama", {}).get("characters", {})

    def parse_script(self, script_path: Path) -> List[Dict[str, Any]]:
        """
        Parses script JSON into a normalized list of segment tasks for voice synthesis.
        """
        with open(script_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        scenes = data.get("scenes", [])
        tasks = []

        for idx, scene in enumerate(scenes):
            char_key = scene.get("character", "NARRATOR").upper()
            char_info = self.voices_config.get(char_key, {})

            # Voice reference sample
            ref_sample_name = char_info.get("reference_sample", "narrator.wav")
            ref_sample_path = SAMPLES_DIR / ref_sample_name

            # Mood & Chatterbox parameters
            mood = scene.get("mood", char_info.get("default_mood", "neutral")).lower()
            mood_params = MOOD_PRESETS.get(mood, MOOD_PRESETS["neutral"])

            task = {
                "index": idx + 1,
                "character": char_key,
                "role_name": char_info.get("role", char_key),
                "gender": char_info.get("gender", "male"),
                "text": scene.get("text", "").strip(),
                "mood": mood,
                "exaggeration": mood_params["exaggeration"],
                "cfg_weight": mood_params["cfg_weight"],
                "reference_sample": str(ref_sample_path) if ref_sample_path.exists() else None,
                "sfx_cue": scene.get("sfx_cue"),
                "bgm_cue": scene.get("bgm_cue"),
            }
            tasks.append(task)

        return tasks
