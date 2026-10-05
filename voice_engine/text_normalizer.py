# -*- coding: utf-8 -*-
"""
Hindi Text Normalization for Natural Speech Synthesis
"""

import re

# Common digit to Hindi word mappings
HINDI_DIGITS = {
    '0': 'शून्य', '1': 'एक', '2': 'दो', '3': 'तीन', '4': 'चार',
    '5': 'पांच', '6': 'छह', '7': 'सात', '8': 'आठ', '9': 'नौ',
    '10': 'दस', '20': 'बीस', '50': 'पचास', '100': 'सौ', '1000': 'हज़ार',
    '100000': 'लाख', '10000000': 'करोड़'
}

def normalize_hindi_text(text: str) -> str:
    """
    Cleans and prepares Hindi text for Chatterbox TTS:
    - Removes markdown syntax, asterisks, brackets
    - Cleans paralinguistic tags like [laugh], [sigh] that cause speech artifacts
    - Ensures proper Hindi sentence terminators (।) for natural pauses
    """
    if not text:
        return ""

    # Remove markdown like *italics* or **bold**
    clean = re.sub(r'[*_~`#>]', '', text)

    # Remove square bracket tags like [laugh], [sigh], [breath]
    # (Chatterbox sometimes reads these literally if not handled)
    clean = re.sub(r'\[.*?\]', '', clean)
    clean = re.sub(r'\(.*?\)', '', clean)

    # Replace multiple whitespaces
    clean = re.sub(r'\s+', ' ', clean).strip()

    # Normalize Hindi punctuation
    clean = clean.replace(".", "।").replace("!", "।").replace("?", " ?")
    clean = re.sub(r'।+', '।', clean)

    # Ensure ending pause
    if clean and clean[-1] not in "।?":
        clean += "।"

    return clean
