# -*- coding: utf-8 -*-
"""
Story Generator for Desi Love, Romance & Emotional Twist Drama
"""

import os
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional

from story_engine.romance_prompts import SYSTEM_PROMPT, SAMPLE_ROMANCE_STORY
from config.settings import SCRIPTS_DIR

class StoryGenerator:
    def __init__(self, api_key: Optional[str] = None, provider: str = "gemini"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.provider = provider.lower()

    def generate_story(
        self,
        topic: str = "आखिरी ख़त और वो बारिश की रात",
        duration_minutes: int = 5,
        hero_name: str = "कबीर",
        heroine_name: str = "आरुषि",
        twist_theme: str = "Secret Sacrifice for lover's family",
        output_filename: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a complete audio drama script with dialogue, emotions, SFX, and BGM cues.
        """
        print(f"\n[StoryGenerator] Generating '{topic}' ({duration_minutes} min)...")
        print(f"  Hero: {hero_name} | Heroine: {heroine_name} | Twist: {twist_theme}")

        story_data = None

        # 1. Try AI Generation if API key is present
        if self.api_key:
            try:
                story_data = self._generate_with_ai(topic, duration_minutes, hero_name, heroine_name, twist_theme)
            except Exception as e:
                print(f"  [StoryGenerator] AI generation warning: {e}. Falling back to curated master story.")

        # 2. Fallback to Curated Production Story
        if not story_data:
            story_data = self._get_curated_story(topic, hero_name, heroine_name)

        # 3. Save to output/scripts/
        SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
        if not output_filename:
            timestamp = int(time.time())
            safe_title = "".join(c for c in topic if c.isalnum() or c in (" ", "_", "-")).rstrip().replace(" ", "_")
            output_filename = f"script_{safe_title}_{timestamp}.json"

        output_path = SCRIPTS_DIR / output_filename
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(story_data, f, ensure_ascii=False, indent=2)

        print(f"  [StoryGenerator] Script saved successfully: {output_path}")
        print(f"  Total Scenes / Segments: {len(story_data.get('scenes', []))}")
        return story_data

    def _generate_with_ai(
        self, topic: str, duration_minutes: int, hero_name: str, heroine_name: str, twist_theme: str
    ) -> Dict[str, Any]:
        """Calls Gemini or OpenAI to create a brand new script."""
        import requests

        user_prompt = f"""
Write a complete, emotional audio drama script in Hindi for the topic: '{topic}'.
Estimated audio length: {duration_minutes} minutes.
Characters: Hero ({hero_name}), Heroine ({heroine_name}), Narrator (कथावाचक).
Twist Theme: {twist_theme}.

Return ONLY a valid JSON object matching this schema:
{{
  "title": "{topic}",
  "genre": "Desi Romance & Emotional Twist Drama",
  "synopsis": "Short emotional synopsis",
  "bgm_theme": "romantic_sad_piano",
  "scenes": [
    {{
      "character": "NARRATOR or HERO or HEROINE",
      "mood": "romantic or sad or emotional or crying or whisper or angry or cinematic",
      "text": "Dialogue or narration in heart-touching Hindi",
      "sfx_cue": "rain or heartbeat or paper_rustle or door_slam",
      "bgm_cue": "sad_piano or emotional_strings or violin_solo"
    }}
  ]
}}
"""
        # Example using Gemini REST API directly without heavy external SDK
        gemini_key = os.getenv("GEMINI_API_KEY", self.api_key)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
        payload = {
            "contents": [{
                "parts": [
                    {"text": SYSTEM_PROMPT},
                    {"text": user_prompt}
                ]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "responseMimeType": "application/json"
            }
        }
        res = requests.post(url, json=payload, timeout=30)
        res.raise_for_status()
        res_json = res.json()
        raw_text = res_json['candidates'][0]['content']['parts'][0]['text']
        return json.loads(raw_text)

    def _get_curated_story(self, topic: str, hero_name: str, heroine_name: str) -> Dict[str, Any]:
        """Returns the curated master romance story with updated character names."""
        import copy
        story = copy.deepcopy(SAMPLE_ROMANCE_STORY)
        story["title"] = topic

        # Replace default names if custom names given
        if hero_name != "कबीर" or heroine_name != "आरुषि":
            for scene in story["scenes"]:
                scene["text"] = scene["text"].replace("कबीर", hero_name).replace("आरुषि", heroine_name)
        return story
