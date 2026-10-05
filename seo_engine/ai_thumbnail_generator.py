# -*- coding: utf-8 -*-
"""
AI Thumbnail & Poster Generator for Pocket FM / Kuku FM Audio Stories.
1. Analyzes the story with Google Gemini to identify the emotional climax hook.
2. Crafts a world-class, high-CTR cinematic prompt (chiaroscuro, volumetric lighting, glowing bokeh, emotional eye contact, 8k, textless).
3. Generates uncompressed 16:9 (1920x1080) artwork using Flux AI.
4. Auto-crops watermarks, saves as thumbnail, and passes to video renderer.
"""

import os
import json
import urllib.parse
import requests
from pathlib import Path
from typing import Optional, Dict, Any
from PIL import Image

class AIThumbnailGenerator:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")

    def generate_story_thumbnail(
        self,
        story_title: str,
        story_text: str = "",
        output_dir: Optional[Path] = None,
        custom_prompt: Optional[str] = None
    ) -> Path:
        """
        Automatically generates a high-CTR, glowing, textless 16:9 cinematic poster.
        """
        if not output_dir:
            output_dir = Path("C:/Audio-automation/output/thumbnails")
        output_dir.mkdir(parents=True, exist_ok=True)

        safe_name = "".join(c for c in story_title if c.isalnum() or c in (" ", "_", "-")).rstrip().replace(" ", "_")
        target_path = output_dir / f"thumbnail_{safe_name}.jpg"

        print(f"\n[AIThumbnailGenerator] 🎨 Crafting High-CTR Glowing Thumbnail for: '{story_title}'...")

        # 1. Get Climax Visual Prompt using Gemini
        if not custom_prompt:
            visual_prompt = self._craft_gemini_prompt(story_title, story_text)
        else:
            visual_prompt = custom_prompt

        print(f"  [AIThumbnailGenerator] Visual Concept: {visual_prompt[:120]}...")

        # 2. Generate Image via Flux AI
        success = self._fetch_flux_image(visual_prompt, target_path)

        if not success or not target_path.exists():
            print("  [AIThumbnailGenerator] Fallback to atmospheric cinematic canvas...")
            self._generate_fallback_canvas(story_title, target_path)

        print(f"  [AIThumbnailGenerator] 🚀 Master 16:9 Thumbnail Ready: {target_path.name}")
        return target_path

    def _craft_gemini_prompt(self, story_title: str, story_text: str) -> str:
        """Uses Gemini to identify the emotional climax and design a high-CTR visual."""
        default_prompt = (
            f"Cinematic Bollywood emotional drama thumbnail for '{story_title}', "
            "heartbroken Indian young man in heavy rain at night, glowing amber streetlamp, "
            "volumetric moonlight, intense emotional expression, photorealistic, 8k, Unreal Engine 5, textless, masterpiece"
        )
        if not self.api_key:
            return default_prompt

        summary_snip = story_text[:1200] if story_text else story_title
        sys_prompt = (
            "You are an award-winning YouTube Thumbnail Art Director for Pocket FM & Kuku FM. "
            "Analyze this story synopsis and write a ONE-SENTENCE visual description for an image-generation AI (Flux/Midjourney). "
            "Rules for MAX CLICK-THROUGH RATE (CTR): "
            "1. Focus on one intense, high-tension moment (e.g. passionate tearful eye contact in pouring rain, glowing lantern at midnight, shock, heartbreak). "
            "2. Lighting: Glowing volumetric lighting, high contrast chiaroscuro, warm amber bokeh vs deep midnight blue, rim light. "
            "3. NO TEXT, NO WORDS, NO LETTERS, NO TYPOGRAPHY. Pure cinematic imagery. "
            "4. Include keywords: photorealistic, 8k, Unreal Engine 5, cinematic Bollywood audio drama, masterpiece. "
            "Output ONLY the prompt text in English."
        )

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-lite-latest:generateContent?key={self.api_key}"
        payload = {
            "contents": [{
                "parts": [{"text": sys_prompt + f"\n\nStory Context:\nTitle: {story_title}\nSnippet: {summary_snip}"}]
            }],
            "generationConfig": {"temperature": 0.5, "maxOutputTokens": 150}
        }
        try:
            res = requests.post(url, json=payload, timeout=15)
            if res.status_code == 200:
                raw_ans = res.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
                if len(raw_ans) > 20:
                    return raw_ans.replace('"', '').replace('\n', ' ')
        except Exception as e:
            print(f"  [AIThumbnailGenerator] Gemini prompt generation note: {e}")

        return default_prompt

    def _fetch_flux_image(self, prompt: str, target_path: Path) -> bool:
        """Fetches 16:9 image from Flux AI engine and cleans watermark."""
        encoded = urllib.parse.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded}?width=1280&height=720&model=flux&nologo=true&seed=42"

        try:
            res = requests.get(url, timeout=35)
            if res.status_code == 200 and len(res.content) > 10000:
                temp_raw = target_path.with_name(f"{target_path.stem}_raw.jpg")
                with open(temp_raw, "wb") as f:
                    f.write(res.content)

                # Open with PIL, crop bottom 26px to remove any logo/watermark, scale to 1920x1080
                img = Image.open(temp_raw).convert("RGB")
                w, h = img.size
                cropped = img.crop((0, 0, w, h - 26))
                final_poster = cropped.resize((1920, 1080), Image.Resampling.LANCZOS)
                final_poster.save(str(target_path), quality=96)

                if temp_raw.exists():
                    try:
                        temp_raw.unlink()
                    except Exception:
                        pass
                return True
        except Exception as e:
            print(f"  [AIThumbnailGenerator] Flux image download error: {e}")

        return False

    def _generate_fallback_canvas(self, title: str, target_path: Path):
        """Generates clean atmospheric 1920x1080 gradient if internet fails."""
        img = Image.new("RGB", (1920, 1080), (14, 18, 30))
        img.save(str(target_path), quality=95)
