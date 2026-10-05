# -*- coding: utf-8 -*-
"""
Bilingual Multi-Speaker Drama Director (Hindi & English)
Automatically detects language, extracts character dialogues, injects dramatic Climax Hook,
and assigns appropriate cinema voice profiles.
"""

import os
import re
import json
from typing import Dict, Any, List, Tuple, Optional

# English dialogue attribution patterns
EN_ATTR_REGEX = re.compile(
    r'^(.*?)\b(said|asked|shouted|whispered|screamed|cried|replied|muttered|yelled|demanded|gasped)\b[,:-]?\s*["“\']?(.*?)["”\']?$',
    re.IGNORECASE | re.DOTALL
)

COMMON_EN_HEROES = ["Alex", "Edward", "Ethan", "Lucas", "Liam", "Christian", "Damon", "Noah", "Leo", "Adrian", "Julian", "James"]
COMMON_EN_HEROINES = ["Elena", "Emma", "Bella", "Sophia", "Ava", "Chloe", "Scarlett", "Mia", "Lily", "Aria", "Isabella", "Grace"]

class BilingualDramaDirector:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "")

    def detect_language(self, text: str) -> str:
        """Detects whether text is primarily Hindi (hi) or English (en)."""
        hindi_chars = len(re.findall(r'[\u0900-\u097F]', text))
        total_letters = len(re.findall(r'[a-zA-Z\u0900-\u097F]', text))
        if total_letters > 0 and (hindi_chars / total_letters) > 0.25:
            return "hi"
        return "en"

    def clean_text(self, text: str, lang: str = "hi") -> List[str]:
        raw_paras = [p.strip() for p in text.split('\n\n') if p.strip()]
        clean = []
        junk_en = [r'subscribe', r'leave a comment', r'chapter \d+:', r'read also', r'copyright \d+']
        junk_hi = [r'very sad emotional love story', r'sad love story in hindi', r'कमेंट करके जरूर बताना', r'शेयर करें', r'मूल उद्देश्य']

        junk = junk_hi if lang == "hi" else junk_en

        for p in raw_paras:
            if any(re.search(pat, p, re.IGNORECASE) for pat in junk):
                continue
            p_norm = re.sub(r'[ \t]+', ' ', p).strip()
            if len(p_norm) >= 12:
                clean.append(p_norm)
        return clean

    def generate_climax_hook(self, hero: str, heroine: str, lang: str = "hi") -> List[Dict[str, Any]]:
        """Generates intense opening Climax Hook for Hindi or English stories."""
        if lang == "hi":
            return [
                {
                    "character": "NARRATOR",
                    "mood": "crying",
                    "text": f"बारिश की उस तूफानी रात में... जब {hero} भीगता हुआ उस सूने घर के बंद दरवाजे को पागलों की तरह पीट रहा था, तब उसे नहीं पता था कि उसकी ज़िंदगी, उसकी {heroine}... उसे हमेशा के लिए छोड़कर जा चुकी है!",
                    "sfx_cue": "none",
                    "bgm_cue": "romantic_sad_piano"
                },
                {
                    "character": "HERO",
                    "mood": "crying",
                    "text": f"{heroine}! प्लीज दरवाजा खोलो... तुम मुझे ऐसे छोड़कर नहीं जा सकतीं! बाहर आओ {heroine}... सिर्फ एक बार मेरी बात सुन लो!",
                    "sfx_cue": "none",
                    "bgm_cue": "romantic_sad_piano"
                },
                {
                    "character": "NARRATOR",
                    "mood": "cinematic",
                    "text": f"लेकिन अंदर सिर्फ़ सन्नाटा था। न कोई आवाज़, न कोई जवाब... सब कुछ एक पल में राख हो चुका था! पर यह बर्बादी उस रात नहीं हुई थी... यह रूह कंपा देने वाली दास्तान शुरू हुई थी तीन महीने पहले, जब दोनों की नज़रें पहली बार टकराई थीं...",
                    "sfx_cue": "none",
                    "bgm_cue": "romantic_sad_piano"
                }
            ]
        else:
            return [
                {
                    "character": "NARRATOR",
                    "mood": "crying",
                    "text": f"On that stormy, rain-drenched midnight... as {hero} pounded violently against the heavy locked door of the desolate mansion, he had no idea that his entire world, {heroine}... had vanished forever!",
                    "sfx_cue": "none",
                    "bgm_cue": "romantic_sad_piano"
                },
                {
                    "character": "HERO",
                    "mood": "crying",
                    "text": f"{heroine}! Please, open the door! You can't just leave me like this! Come out... just hear me out once!",
                    "sfx_cue": "none",
                    "bgm_cue": "romantic_sad_piano"
                },
                {
                    "character": "NARRATOR",
                    "mood": "cinematic",
                    "text": f"But from inside, there was only cold, deafening silence. Everything they built had shattered in a single night. Yet this heartbreaking saga did not begin in the storm... it began three months earlier, the day their eyes first locked...",
                    "sfx_cue": "none",
                    "bgm_cue": "romantic_sad_piano"
                }
            ]

    def build_drama_script(self, raw_text: str, title: str = "Audio Drama", add_hook: bool = True) -> Dict[str, Any]:
        lang = self.detect_language(raw_text)
        print(f"  🌐 Detected Story Language: {'HINDI (हिंदी)' if lang == 'hi' else 'ENGLISH (अंग्रेजी)'}")

        if lang == "hi":
            from story_engine.dialogue_parser import DramaScriptBuilder
            builder = DramaScriptBuilder()
            script = builder.build_full_audio_drama_script(raw_text, title=title, add_climax_hook=add_hook)
            script["language"] = "hi"
            return script
        else:
            return self._build_english_drama_script(raw_text, title=title, add_hook=add_hook)

    def _build_english_drama_script(self, raw_text: str, title: str, add_hook: bool) -> Dict[str, Any]:
        clean_paras = self.clean_text(raw_text, lang="en")
        hero = "Christian"
        heroine = "Elena"

        for h in COMMON_EN_HEROES:
            if re.search(r'\b' + h + r'\b', raw_text):
                hero = h
                break
        for f in COMMON_EN_HEROINES:
            if re.search(r'\b' + f + r'\b', raw_text):
                heroine = f
                break

        scenes = []
        if add_hook:
            scenes.extend(self.generate_climax_hook(hero, heroine, lang="en"))

        last_spk = "NARRATOR"
        for p in clean_paras:
            # Check quotes
            if '"' in p or '“' in p:
                parts = re.split(r'([“"][^”"]+[”"])', p)
                for part in parts:
                    part = part.strip()
                    if not part:
                        continue
                    if (part.startswith('"') and part.endswith('"')) or (part.startswith('“') and part.endswith('”')):
                        speech = part[1:-1].strip()
                        char = "HEROINE" if last_spk == "HERO" else "HERO"
                        scenes.append({
                            "character": char,
                            "mood": "cinematic",
                            "text": speech,
                            "sfx_cue": "none",
                            "bgm_cue": "romantic_sad_piano"
                        })
                        last_spk = char
                    else:
                        if len(part) >= 10:
                            scenes.append({
                                "character": "NARRATOR",
                                "mood": "cinematic",
                                "text": part,
                                "sfx_cue": "none",
                                "bgm_cue": "romantic_sad_piano"
                            })
            else:
                scenes.append({
                    "character": "NARRATOR",
                    "mood": "cinematic",
                    "text": p,
                    "sfx_cue": "none",
                    "bgm_cue": "romantic_sad_piano"
                })

        return {
            "title": title,
            "genre": "Bilingual Romance & Hard Drama",
            "language": "en",
            "characters": {
                "HERO": hero,
                "HEROINE": heroine,
                "NARRATOR": "Narrator"
            },
            "total_scenes": len(scenes),
            "scenes": scenes
        }