# -*- coding: utf-8 -*-
"""
Viral Metadata Generator:
- 3 High-CTR Click-Worthy Titles (Curiosity gap, emotional punch, emojis)
- Full YouTube Description (Emotional quote hook, synopsis, 20-character cast breakdown, chapter timestamps)
- High-Volume Viral Hashtags (#HindiKahaniya, #PocketFM, #AudioStory...)
- Top 20 SEO Search Tags
"""

import os
import json
import requests
from pathlib import Path
from typing import Optional, Dict, Any

class ViralMetadataGenerator:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")

    def generate_youtube_kit(
        self,
        story_title: str,
        story_text: str = "",
        character_breakdown: Optional[Dict[str, int]] = None,
        duration_str: str = "3.5 Hours",
        output_dir: Optional[Path] = None
    ) -> Dict[str, Any]:
        """
        Generates complete YouTube Publishing Kit saved as TXT and returned as dict.
        """
        if not output_dir:
            output_dir = Path("C:/Audio-automation/output/metadata")
        output_dir.mkdir(parents=True, exist_ok=True)

        safe_name = "".join(c for c in story_title if c.isalnum() or c in (" ", "_", "-")).rstrip().replace(" ", "_")
        target_path = output_dir / f"youtube_kit_{safe_name}.txt"

        print(f"\n[ViralMetadataGenerator] 📈 Generating High-CTR Viral YouTube Package for: '{story_title}'...")

        data = self._call_gemini_seo(story_title, story_text, duration_str)

        # Build formatted package
        cast_text = ""
        if character_breakdown:
            cast_lines = [f"  • {char}: {count} scene(s)" for char, count in character_breakdown.items()]
            cast_text = "\n" + "\n".join(cast_lines)
        else:
            cast_text = "  • Full 20-Speaker Multi-Cast Audio Drama (Hero, Heroine, Kids, Parents, Elders, Rivals)"

        titles_text = "\n".join([f"Option {i}: {t}" for i, t in enumerate(data.get("viral_titles", []), 1)])
        hashtags_str = " ".join(data.get("viral_hashtags", []))
        tags_str = ", ".join(data.get("viral_tags", []))

        kit_content = f"""================================================================================
📺 YOUTUBE VIRAL PUBLISHING KIT (POCKET FM / KUKU FM STYLE)
Story: {story_title} | Duration: {duration_str}
================================================================================

🔥 3 HIGH-CTR CLICK-WORTHY TITLES (Choose the best one):
--------------------------------------------------------------------------------
{titles_text}

📝 VIRAL YOUTUBE DESCRIPTION (Copy-paste directly):
--------------------------------------------------------------------------------
{data.get('viral_description', '')}

🎭 VOICE CAST & CHARACTERS:
{cast_text}

🎧 AUDIO PRODUCTION NOTE:
  Recorded & Mastered in 24kHz Pure Cinema Sound with Real Rain Ambience and Grand Piano.
  Please use Headphones for the best immersive 8D experience.

🏷️ VIRAL HASHTAGS:
{hashtags_str}

🔑 TOP 20 YOUTUBE SEARCH TAGS (Copy into Video Tags box):
--------------------------------------------------------------------------------
{tags_str}

================================================================================
"""
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(kit_content)

        print(f"  [ViralMetadataGenerator] 💾 Saved YouTube Publishing Kit -> {target_path.name}")
        data["file_path"] = str(target_path)
        return data

    def _call_gemini_seo(self, title: str, text: str, duration: str) -> Dict[str, Any]:
        """Calls Gemini API to craft high-retention viral YouTube elements."""
        default_data = {
            "viral_titles": [
                f"💔 उस रात उसने क्या छुपाया था? | {title} | Heart Touching Hindi Love Story",
                f"😭 काश वो एक बार मुड़कर देख लेती... | {title} | Pocket FM Style Audio Drama",
                f"🔥 20 आवाज़ों में महा ड्रामा | {title} | Hindi Audiobook Full Story"
            ],
            "viral_description": f"सुनिए '{title}' की एक ऐसी दर्दभरी और रूह कंपा देने वाली प्रेम कहानी जो आपके दिल को छू जाएगी। जब सच्चाई सामने आती है, तो पैरों तले ज़मीन खिसक जाती है...\n\n🎧 कृपया हेडफ़ोन (Headphones) का उपयोग करें।",
            "viral_hashtags": ["#HindiKahaniya", "#AudioStory", "#PocketFM", "#KukuFM", "#LoveStory", "#HeartTouchingStory", "#HindiAudiobook", "#EmotionalStory", "#HindiStories"],
            "viral_tags": ["hindi love story", "hindi kahaniya", "pocket fm story", "kuku fm stories", "audio story hindi", "heart touching love story", "sad love story hindi", "hindi audio book", "hindi drama"]
        }
        if not self.api_key:
            return default_data

        prompt = f"""You are the #1 YouTube Growth Expert for Pocket FM & Kuku FM Hindi Audio Stories.
Given:
Title: {title}
Estimated Duration: {duration}
Snippet: {text[:800] if text else title}

Generate a JSON object with:
1. "viral_titles": List of 3 irresistible, high-CTR YouTube titles in Hindi/Hinglish with emojis. (Include curiosity hooks, emotional shock, and keywords like Pocket FM / Love Story).
2. "viral_description": Compelling YouTube description (first 3 lines must be a heart-wrenching emotional dialogue quote that stops the scroll, followed by a dramatic synopsis that creates unbearable curiosity to listen to the end, headphone warning, and copyright disclaimer).
3. "viral_hashtags": List of 12 top viral Hindi YouTube hashtags (e.g. #HindiKahaniya, #PocketFM, #AudioStory, #LoveStory...).
4. "viral_tags": List of 20 high-ranking YouTube SEO search tags.

Output ONLY valid JSON."""

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-lite-latest:generateContent?key={self.api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json", "temperature": 0.7}
        }
        try:
            res = requests.post(url, json=payload, timeout=20)
            if res.status_code == 200:
                raw_json = res.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
                parsed = json.loads(raw_json)
                if isinstance(parsed, dict) and "viral_titles" in parsed:
                    return parsed
        except Exception as e:
            print(f"  [ViralMetadataGenerator] Gemini SEO call warning: {e}")

        return default_data
