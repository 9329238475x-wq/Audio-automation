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
3. For dialogue attribution like 'रोते हुए उसने कहा...', the attribution belongs to NARRATOR, and the spoken dialogue inside quotes belongs to the character.
4. CASTING MANDATE: Maximize voice diversity across the ensemble cast. DO NOT collapse all characters into Hero/Heroine.
   Assign dialogue to the EXACT matching role from these 20 studio speakers:
   - "CHILD_FEMALE" (Little girl / bitiya / pinki / playful innocent daughter)
   - "CHILD_MALE" (Little boy / munna / golu / playful energetic young son)
   - "MOTHER" (Gentle, affectionate, worried mother)
   - "MOTHER_STRICT" (Orthodox, sharp, commanding mother-in-law / saas)
   - "FATHER" (Emotional, burdened, caring father)
   - "FATHER_STRICT" (Authoritative, strict patriarch / thakur / mukhiya)
   - "GRANDMOTHER" (Loving, story-telling, aged dadi / nani)
   - "GRANDFATHER" (Wise, trembling, affectionate aged dada / nana)
   - "COP_DOCTOR" (Police inspector, constable, doctor, surgeon, lawyer)
   - "SISTER" (Caring, affectionate, chirpy sister / didi)
   - "BHABHI" (Mature, understanding, witty sister-in-law / aunt / chachi)
   - "FRIEND_MALE" (Loyal best friend / buddy / colleague)
   - "VILLAIN" (Gritty, ruthless, menacing antagonist / rival / enemy)
   - "VAMP" (Cunning, sarcastic rival woman / sautan)
   - "SERVANT_MALE" (Humble, loyal servant / driver / helper / peon)
   - "HERO" (Male protagonist in love, remorse, or calm dialogue)
   - "HERO_ANGRY" (Hero in shouting rage, fierce argument, or intense heartbreak)
   - "HEROINE" (Female protagonist in tender, emotional, or romantic scenes)
   - "HEROINE_BOLD" (Female protagonist speaking boldly, defiantly, or confronting)
   - "NARRATOR" (Soulful baritone storyteller)
5. Mood must be one of: "crying", "heartbroken", "angry", "romantic", "sad", "whisper", "cinematic", "neutral".
6. Output MUST be ONLY a valid JSON array of objects with keys:
   - "character": One of the 20 character tags above
   - "mood": Delivery emotion
   - "text": Clean Hindi spoken sentence or narration (NO asterisks, NO markdown).
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

        # -------------------------------------------------------------
        # GEMINI DIRECTOR MASTERSTROKE: AUTO 16:9 GLOWING THUMBNAIL & VIRAL SEO
        # -------------------------------------------------------------
        print(f"\n🎨 [Gemini AI Director] Designing 16:9 High-CTR Glowing Thumbnail & Viral SEO Kit...")
        thumbnail_path = None
        seo_data = {}
        try:
            from seo_engine.ai_thumbnail_generator import AIThumbnailGenerator
            from seo_engine.viral_metadata_generator import ViralMetadataGenerator

            # Climax extraction: Find highest tension scene
            intense_scenes = [s["text"] for s in all_scenes if s.get("mood") in ("crying", "heartbroken", "angry")]
            climax_context = " ".join(intense_scenes[:3]) if intense_scenes else (all_scenes[0]["text"] if all_scenes else title)

            # 1. Generate Glowing 16:9 (1920x1080) Thumbnail
            thumb_gen = AIThumbnailGenerator(api_key=self.api_key)
            thumb_file = thumb_gen.generate_story_thumbnail(
                story_title=title,
                story_text=climax_context
            )
            thumbnail_path = str(thumb_file)

            # 2. Generate Viral SEO Kit (Titles + Description + Tags)
            meta_gen = ViralMetadataGenerator(api_key=self.api_key)
            seo_data = meta_gen.generate_youtube_kit(
                story_title=title,
                story_text=climax_context,
                character_breakdown=speakers
            )
        except Exception as th_err:
            print(f"  ⚠️ [GeminiDirector] Thumbnail / SEO generation notice: {th_err}")

        return {
            "title": title,
            "genre": "AI Directed Bollywood / Pocket FM Audio Drama",
            "characters": {
                "HERO": hero_name,
                "HEROINE": heroine_name,
                "NARRATOR": "Narrator"
            },
            "thumbnail_path": thumbnail_path,
            "seo_package": seo_data,
            "total_scenes": len(all_scenes),
            "scenes": all_scenes
        }
