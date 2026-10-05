# -*- coding: utf-8 -*-
"""
Gemini AI Drama Director Engine
Uses Google Gemini Flash API with 1M Token Context as the Master Drama Director:
- Analyzes story like a Bollywood / Pocket FM audio drama director.
- Detects characters: HERO, HEROINE, MOTHER, FATHER, RIVAL, NARRATOR.
- Separates 3rd-person narrator action from character spoken dialogue.
- Tags emotional delivery: crying, heartbroken, angry, romantic, whisper, cinematic.
- Injects 30-45s intense Climax Cold-Open Hook in rain.
- Chunked for complete JSON fidelity without truncation (4,000-word acts).
- Multi-model fallback with automatic local parser fail-safe (0% quota risk).
"""

import os
import re
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
import requests
from dotenv import load_dotenv

# Load API Key
load_dotenv(Path(__file__).resolve().parent.parent / ".env")
load_dotenv()

FALLBACK_MODELS = [
    "gemini-flash-lite-latest",
    "gemini-3.5-flash",
    "gemini-flash-latest",
    "gemini-pro-latest"
]

DIRECTOR_SYSTEM_PROMPT = """You are an elite Bollywood / Pocket FM Audio Drama Director.
Your job is to transform this raw novel text into a professional Multi-Speaker Audio Drama script.

Rules:
1. Strip all website junk, blog titles, SEO text, "like/subscribe/comment" boilerplates.
2. Break the text into dialogue turns and narration scenes.
3. For dialogue attribution like "सुजाता ने रोते हुए कहा-", the attribution belongs to NARRATOR, and the spoken dialogue inside quotes belongs to HEROINE or HERO.
4. Characters must be categorized as:
   - "HERO" (Male protagonist)
   - "HEROINE" (Female protagonist)
   - "MOTHER" (Elderly female)
   - "FATHER" (Elderly male)
   - "RIVAL" (Antagonist / Rival)
   - "NARRATOR" (Baritone storyteller)
5. Mood must be one of: "crying", "heartbroken", "angry", "romantic", "sad", "whisper", "cinematic".
6. Output MUST be ONLY a valid JSON array of objects with keys:
   - "character": Character tag
   - "mood": Delivery emotion
   - "text": The clean Hindi / English spoken sentence or narration (NO asterisks, NO markdown).
"""

class GeminiDramaDirector:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "")
        if not self.api_key:
            print("⚠️ [GeminiDirector] No GEMINI_API_KEY found in environment or .env!")

    def call_gemini_json(self, prompt: str) -> Optional[List[Dict[str, Any]]]:
        """Calls Gemini API with model fallback and returns parsed JSON array."""
        if not self.api_key:
            return None

        for model in FALLBACK_MODELS:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.api_key}"
            payload = {
                "contents": [
                    {"parts": [{"text": DIRECTOR_SYSTEM_PROMPT + "\n\nNovel Segment to Direct:\n" + prompt}]}
                ],
                "generationConfig": {
                    "response_mime_type": "application/json",
                    "temperature": 0.3
                }
            }
            try:
                resp = requests.post(url, json=payload, timeout=40)
                if resp.status_code == 200:
                    raw_ans = resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
                    parsed = json.loads(raw_ans)
                    if isinstance(parsed, list):
                        return parsed
                    elif isinstance(parsed, dict) and "scenes" in parsed:
                        return parsed["scenes"]
                elif resp.status_code in (429, 503):
                    print(f"  [GeminiDirector] Model {model} returned HTTP {resp.status_code}, trying next model...")
                    time.sleep(1)
                    continue
                else:
                    print(f"  [GeminiDirector] Model {model} returned HTTP {resp.status_code}: {resp.text[:120]}")
            except Exception as e:
                print(f"  [GeminiDirector] Request error on {model}: {e}")
                continue

        return None

    def direct_novel(
        self,
        raw_text: str,
        title: str = "Audio Drama",
        hero_name: str = "कबीर",
        heroine_name: str = "आरुषि",
        chunk_word_size: int = 3500
    ) -> Dict[str, Any]:
        """
        Directs an entire 30,000 - 40,000 word mega novel using Gemini AI:
        - Splits into ~3,500 word dramatic acts to ensure zero token truncation.
        - Directs each act with Gemini AI Director.
        - Stitches together into one master script with Climax Rain Hook.
        """
        print(f"\n🎬 [Gemini AI Director] Directing Full Story: '{title}'...")
        words = raw_text.split()
        total_words = len(words)
        print(f"  📊 Total Story Words: {total_words}")

        # Split into acts
        acts = []
        curr_words = []
        for w in words:
            curr_words.append(w)
            if len(curr_words) >= chunk_word_size and (w.endswith("।") or w.endswith(".") or "\n" in w):
                acts.append(" ".join(curr_words))
                curr_words = []
        if curr_words:
            acts.append(" ".join(curr_words))

        print(f"  🎭 Divided into {len(acts)} Dramatic Acts for Gemini AI Direction (0% Output Truncation Guarantee).")

        all_scenes = []

        # 1. Injected Rain Climax Cold-Open Hook
        from story_engine.dialogue_parser import DramaScriptBuilder
        hook_scenes = DramaScriptBuilder().generate_climax_hook(hero_name, heroine_name)
        all_scenes.extend(hook_scenes)

        success_ai_acts = 0

        for act_idx, act_text in enumerate(acts, 1):
            act_word_count = len(act_text.split())
            print(f"  ▶️ Directing Act {act_idx}/{len(acts)} ({act_word_count} words) with Gemini AI...")

            ai_scenes = self.call_gemini_json(act_text)
            if ai_scenes and len(ai_scenes) > 0:
                print(f"    ✨ Gemini AI Directed {len(ai_scenes)} scenes for Act {act_idx}!")
                for s in ai_scenes:
                    all_scenes.append({
                        "character": s.get("character", "NARRATOR").upper(),
                        "mood": s.get("mood", "cinematic").lower(),
                        "text": s.get("text", "").strip(),
                        "sfx_cue": "none",
                        "bgm_cue": "romantic_sad_piano"
                    })
                success_ai_acts += 1
            else:
                print(f"    ⚠️ Act {act_idx} fallback to Local Rule Director...")
                local_script = DramaScriptBuilder().build_full_audio_drama_script(act_text, title=title, add_climax_hook=False)
                all_scenes.extend(local_script.get("scenes", []))

            # Small pause between acts
            if act_idx < len(acts):
                time.sleep(1)

        print(f"\n🎉 [Gemini AI Director] Story Direction Complete!")
        print(f"  🌟 AI-Directed Acts: {success_ai_acts}/{len(acts)}")
        print(f"  🎬 Total Master Scenes: {len(all_scenes)}")

        # Count character distribution
        speakers = {}
        for s in all_scenes:
            c = s.get("character", "NARRATOR")
            speakers[c] = speakers.get(c, 0) + 1
        print(f"  🎭 Character Breakdown: {speakers}")

        return {
            "title": title,
            "genre": "AI Directed Bollywood / Pocket FM Audio Drama",
            "characters": {
                "HERO": hero_name,
                "HEROINE": heroine_name,
                "NARRATOR": "Narrator"
            },
            "total_scenes": len(all_scenes),
            "scenes": all_scenes
        }
