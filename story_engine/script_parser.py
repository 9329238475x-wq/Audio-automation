# -*- coding: utf-8 -*-
"""
Smart Script Parser for 20-Character Radio FM / Pocket FM Audio Drama.
Maps any story character (Hindi names, relationships, professions)
to the optimal voice profile among 20 studio speakers.
"""

import re
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple

from config.settings import MOOD_PRESETS, SAMPLES_DIR

# Smart Hindi & English keywords dictionary
ROLE_MAPPING_RULES = [
    # 1. Child speakers (Highest priority)
    (r"(बच्ची|बिटिया|पिंकी|गुडिया|लड़की|कन्या|छुटकी|child_female|kid_female|little_girl)", "CHILD_FEMALE"),
    (r"(बच्चा|मुन्ना|गोलू|छोटू|बालक|लड़का|child_male|kid_male|little_boy|kid|child)", "CHILD_MALE"),

    # 2. Grandparents
    (r"(दादी|नानी|अम्मा|बुढ़िया|grandmother|grandma|dadi|nani)", "GRANDMOTHER"),
    (r"(दादा|नाना|बाबा|बूढ़ा|वृद्ध|grandfather|grandpa|dada|nana)", "GRANDFATHER"),

    # 3. Mothers & Mother-in-law
    (r"(सास|कठोर माँ|strict_mother|saas)", "MOTHER_STRICT"),
    (r"(माँ|माता|मैया|मां|अम्मी|mother|mom|maa)", "MOTHER"),

    # 4. Fathers & Patriarch
    (r"(मुखिया|ठाकुर|जमींदार|कड़क पिता|सख्त पिता|सख्त|strict_father|patriarch)", "FATHER_STRICT"),
    (r"(पिता|पिताजी|बापू|अब्बा|पापा|father|dad|pitaji)", "FATHER"),

    # 5. Professionals
    (r"(डॉक्टर|दरोगा|इंस्पेक्टर|हवलदार|वकील|जज|officer|doctor|cop|inspector|lawyer)", "COP_DOCTOR"),

    # 6. Relatives (Sister, Bhabhi/Aunt)
    (r"(बहन|दीदी|बहना|छोटी|sister|didi)", "SISTER"),
    (r"(भाभी|चाची|ताई|मौसी|मामी|bhabhi|chachi|aunt)", "BHABHI"),

    # 7. Antagonists (Villain, Rival, Vamp)
    (r"(सौतन|वैम्प|डायन|षड्यंत्रकारी|vamp|sautan)", "VAMP"),
    (r"(खलनायक|गुंडा|बदमाश|दुश्मन|villain|rival|enemy|gunda)", "VILLAIN"),

    # 8. Servants & Helpers
    (r"(नौकर|ड्राइवर|माली|रसोइया|सेवक|servant|driver|helper|peon)", "SERVANT_MALE"),

    # 9. Heroine (Bold vs Romantic)
    (r"(सशक्त|गुस्सैल नायिका|heroine_bold|bold_girl)", "HEROINE_BOLD"),
    (r"(नायिका|सुमन|निर्मला|आरुषि|सिमरन|काव्या|प्रिया|heroine|female_lead|wife|lover_female)", "HEROINE"),

    # 10. Hero (Angry vs Romantic)
    (r"(गुस्सैल नायक|क्रोधित|hero_angry|angry_male)", "HERO_ANGRY"),
    (r"(नायक|कबीर|समीर|रोहन|अमर|तोताराम|hero|male_lead|husband|lover_male)", "HERO"),

    # 11. Friends
    (r"(दोस्त|यार|मित्र|सखा|friend|buddy|pal)", "FRIEND_MALE"),

    # 12. Narrator
    (r"(सूत्रधार|वर्णनकर्ता|narrator|storyteller|narrator_male)", "NARRATOR")
]

class ScriptParser:
    def __init__(self, voices_config_path: Path):
        self.voices_config = {}
        if voices_config_path.exists():
            with open(voices_config_path, "r", encoding="utf-8") as f:
                raw = json.load(f)
                self.voices_config = raw.get("genres", {}).get("desi_romance_drama", {}).get("characters", {})

    def resolve_character(self, raw_char: str) -> str:
        """
        Intelligently resolves any raw character name or title
        to one of the 20 studio character keys.
        """
        raw_upper = raw_char.upper().strip()

        # Direct match in config
        if raw_upper in self.voices_config:
            return raw_upper

        # Exact alias handling
        alias_map = {
            "NARRATION": "NARRATOR",
            "STORYTELLER": "NARRATOR",
            "MALE_LEAD": "HERO",
            "FEMALE_LEAD": "HEROINE",
            "GIRL": "HEROINE",
            "BOY": "HERO",
            "MAN": "HERO",
            "WOMAN": "HEROINE",
            "KID": "CHILD_MALE",
            "CHILD": "CHILD_MALE",
            "CHILD_BOY": "CHILD_MALE",
            "CHILD_GIRL": "CHILD_FEMALE",
            "KID_BOY": "CHILD_MALE",
            "KID_GIRL": "CHILD_FEMALE",
            "BABY": "CHILD_MALE",
            "RIVAL": "VILLAIN",
            "DAD": "FATHER",
            "MOM": "MOTHER",
            "DADI": "GRANDMOTHER",
            "DADA": "GRANDFATHER"
        }
        if raw_upper in alias_map:
            return alias_map[raw_upper]

        # Rule-based matching against Hindi/English regex patterns
        raw_lower = raw_char.lower()
        for pattern, mapped_char in ROLE_MAPPING_RULES:
            if re.search(pattern, raw_lower):
                return mapped_char

        # Smart fallback based on common feminine markers
        if any(raw_lower.endswith(suf) for suf in ["ी", "ा", "देवी", "bai", "rani", "female", "girl"]):
            return "HEROINE"

        return "NARRATOR"

    def parse_script(self, script_path: Path) -> List[Dict[str, Any]]:
        """
        Parses script JSON into a normalized list of segment tasks for voice synthesis.
        """
        with open(script_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        scenes = data.get("scenes", [])
        tasks = []

        for idx, scene in enumerate(scenes):
            raw_char = scene.get("character", "NARRATOR")
            char_key = self.resolve_character(raw_char)
            char_info = self.voices_config.get(char_key, self.voices_config.get("NARRATOR", {}))

            # Voice reference sample
            ref_sample_name = char_info.get("reference_sample", "01_narrator_male.wav")
            ref_sample_path = SAMPLES_DIR / ref_sample_name

            # Fallback to alias if specific WAV is missing
            if not ref_sample_path.exists():
                fallback_path = SAMPLES_DIR / "narrator.wav"
                if fallback_path.exists():
                    ref_sample_path = fallback_path

            # Mood & delivery parameters
            mood = scene.get("mood", char_info.get("default_mood", "neutral")).lower()
            mood_params = MOOD_PRESETS.get(mood, MOOD_PRESETS["neutral"])

            task = {
                "index": idx + 1,
                "character": char_key,
                "original_character": raw_char,
                "role_name": char_info.get("role", char_key),
                "gender": char_info.get("gender", "male"),
                "age_group": char_info.get("age_group", "adult"),
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
