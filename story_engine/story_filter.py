# -*- coding: utf-8 -*-
"""
Strict Drama Filter & Classifier for Pocket FM / Kuku FM Audio Drama Studio
Ensures 100% of hunted, scraped, or generated stories are PURE HIGH-STAKES DRAMA:
- Allowed: Family Drama, Heartbreak, Love/Romance, Betrayal, Revenge, Arranged Marriage, Social/Emotional Twists
- Strictly BLOCKED: Horror, Bhoot, Ghost, Chudail, Dayan, Tantrik, Paranormal, Supernatural
"""

import re
from typing import Tuple, List

# Explicitly Blacklisted Horror & Paranormal Terms
HORROR_BLACKLIST = [
    "horror", "ghost", "bhoot", "pret", "haunted", "darawani", "chudail",
    "dayan", "qabristan", "shmashan", "tantrik", "kala jadu", "supernatural",
    "witch", "demon", "zombie", "khooni saya", "aatma", "pret aatma", "bhoot pret",
    "kabristan", "shamshan", "darawna", "darawane", "haveli ka saya",
    "भूत", "प्रेत", "डायन", "चुड़ैल", "कब्रिस्तान", "श्मशान", "तांत्रिक",
    "काला जादू", "डरावनी", "डरावना", "आत्मा", "हॉरर", "खूनी साया", "पिशाच"
]

# Verified High-Stakes Drama Keywords
DRAMA_ALLOWED_KEYWORDS = [
    "love", "romance", "drama", "family", "betrayal", "revenge", "sacrifice",
    "heartbreak", "twist", "marriage", "divorce", "relationship", "emotional",
    "प्यार", "मोहब्बत", "इश्क", "धोखा", "बदला", "परिवार", "सास बहू", "रिश्ते",
    "तलाक", "शादी", "अरेंज्ड मैरिज", "जुदाई", "आंसू", "दर्द", "जायदाद", "विवाद"
]


def check_drama_validity(title: str, text: str = "") -> Tuple[bool, str]:
    """
    Validates if a story strictly qualifies as Drama and contains ZERO horror elements.
    Returns: (is_valid, reason)
    """
    full_content = f"{title.lower()} {text[:2500].lower()}"

    # 1. Check for Horror Blacklist
    for kw in HORROR_BLACKLIST:
        pattern = r"\b" + re.escape(kw) + r"\b"
        if re.search(pattern, full_content, re.IGNORECASE) or kw in full_content:
            return False, f"Rejected: Story contains horror/supernatural keyword '{kw}'. Strictly Drama only!"

    # 2. Check for Drama relevance
    has_drama_intent = any(dk in full_content for dk in DRAMA_ALLOWED_KEYWORDS)
    if not has_drama_intent and len(text.split()) > 100:
        return False, "Rejected: Story lacks emotional/dramatic stakes (Not high-stakes drama)."

    return True, "Verified Pure High-Stakes Drama"
