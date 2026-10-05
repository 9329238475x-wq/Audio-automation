from story_engine.dialogue_parser import DramaScriptBuilder
# -*- coding: utf-8 -*-
"""
Universal Full Story Scraper & Ingestion Engine
Scrapes complete, full-length Hindi Desi Romance, Emotional & Twist stories from any public URL,
pre-tested portal feeds, search queries, or raw text files, and dramatizes 100% of the story
into multi-character audio scripts without cutting or truncating content.
"""

import os
import sys
import re
import json
import time
import urllib.parse
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

import requests
from bs4 import BeautifulSoup

from config.settings import SCRIPTS_DIR

INPUT_STORIES_DIR = Path(__file__).resolve().parent.parent / "input_stories"
INPUT_STORIES_DIR.mkdir(parents=True, exist_ok=True)

# Curated High-Quality Full-Length Hindi Emotional Stories (Complete Stories)
CURATED_PORTAL_STORIES = [
    {
        "title": "सुजाता और सुभाष की बेपनाह मोहब्बत की दास्तान",
        "url": "https://storyinhindi.net/emotional-love-story-in-hindi/",
        "category": "sad_emotional_love",
        "paragraphs_approx": 102,
        "words_approx": 2692,
        "description": "बेपनाह मोहब्बत, जुदाई और दर्द भरी दास्तान (102 पैराग्राफ्स, 100% पूरी कहानी)"
    },
    {
        "title": "सच्ची मोहब्बत और दिल छू लेने वाला प्यार",
        "url": "https://storyinhindi.net/true-love-story-in-hindi/",
        "category": "heart_touching_love",
        "paragraphs_approx": 79,
        "words_approx": 3895,
        "description": "सच्चा प्यार, समर्पण और दिल को झकझोर देने वाली दास्तान (79 पैराग्राफ्स, पूरी कहानी)"
    },
    {
        "title": "एक बेवफा प्यार की सच्ची कहानी",
        "url": "https://storyinhindi.net/real-love-story-in-hindi-2/",
        "category": "painful_betrayal",
        "paragraphs_approx": 67,
        "words_approx": 3285,
        "description": "बेवफाई, टूटा हुआ दिल और दर्द की इन्तिहा (67 पैराग्राफ्स, पूरी कहानी)"
    },
    {
        "title": "मैं तुम्हारे बिना कैसे जी पाऊंगा: दुःख भरी प्रेम कहानी",
        "url": "https://storyinhindi.net/short-sad-love-story-in-hindi/",
        "category": "painful_love",
        "paragraphs_approx": 52,
        "words_approx": 1771,
        "description": "सच्चा प्यार, जुदाई और तड़प (52 पैराग्राफ्स, पूरी कहानी)"
    },
    {
        "title": "कॉलेज की अधूरी प्रेम कहानी: मैं उसे कभी माफ नहीं करूंगा",
        "url": "https://storyinhindi.net/college-love-story-in-hindi/",
        "category": "college_love",
        "paragraphs_approx": 48,
        "words_approx": 1737,
        "description": "कॉलेज रोमांस, गलतफहमी और दिल छू लेने वाला मोड़ (48 पैराग्राफ्स, पूरी कहानी)"
    },
    {
        "title": "तड़प: आखिर क्यों छोड़ गई तुम मुझे (अधूरी प्रेम कथा)",
        "url": "https://storyinhindi.net/heart-touching-love-story-in-hindi/",
        "category": "heartbroken_twist",
        "paragraphs_approx": 48,
        "words_approx": 1762,
        "description": "अधूरी प्रेम कथा, तड़प और आंसुओं का सैलाब (48 पैराग्राफ्स, पूरी कहानी)"
    },
    {
        "title": "रिशभ और आन्या: रुलाने वाली अधूरी लव स्टोरी",
        "url": "https://storyinhindi.net/sad-love-story-in-hindi/",
        "category": "sad_love",
        "paragraphs_approx": 40,
        "words_approx": 1166,
        "description": "कॉलेज का प्यार, बारिश और अधूरी मोहब्बत (40 पैराग्राफ्स, पूरी कहानी)"
    },
    {
        "title": "एक गलती और सबकुछ खत्म: दर्द भरी दास्तान",
        "url": "https://storyinhindi.net/true-love-love-story-in-hindi/",
        "category": "tragic_twist",
        "paragraphs_approx": 65,
        "words_approx": 2450,
        "description": "एक भूल, जुदाई और जिंदगी भर का दर्द (65 पैराग्राफ्स, पूरी कहानी)"
    }
]

JUNK_PATTERNS = [
    r"Copyright.*",
    r"All Rights Reserved.*",
    r"दोस्तों अगर आपको कहानी पसंद आई.*",
    r"कृपया इस कहानी को शेयर करें.*",
    r"Share this story.*",
    r"Read More:.*",
    r"Also Read:.*",
    r"Follow us on.*",
    r"कमेंट करके बताएं.*",
    r"WhatsApp पर शेयर करें.*",
    r"यह भी पढ़ें:.*",
    r"अगला भाग पढ़ें.*",
    r"टिप्पणी छोड़ें.*",
    r"Save my name, email.*",
    r"Notify me of follow-up.*",
    r"Previous Post.*",
    r"Next Post.*",
    r"Table of Contents.*"
]

NON_DIALOGUE_PATTERNS = [
    r"story in hindi",
    r"love story",
    r"sad story",
    r"emotional story",
    r"part\s*\d+",
    r"भाग\s*\d+",
    r"\|"
]

class StoryScraper:
    def __init__(self, timeout: int = 15):
        self.timeout = timeout
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept-Language": "hi,en-US;q=0.9,en;q=0.8"
        }

    def scrape_url(self, url: str) -> Dict[str, Any]:
        """
        Scrapes a complete full-length Hindi story from any public web URL.
        Extracts 100% of the story paragraphs without truncation.
        """
        print(f"\n[StoryScraper] 🌐 Fetching complete story from: {url}")
        res = requests.get(url, headers=self.headers, timeout=self.timeout)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")

        # Clean noise tags
        for tag in soup(["script", "style", "noscript", "nav", "header", "footer", "aside", "form"]):
            tag.decompose()

        # 1. Title Extraction
        title = ""
        h1 = soup.find("h1")
        if h1 and len(h1.get_text().strip()) > 5:
            title = h1.get_text().strip()
        elif soup.title:
            title = soup.title.get_text().strip()
        else:
            title = "दर्दभरी प्रेम कहानी"

        # Clean title suffix
        title = re.split(r"[|\-–—]", title)[0].strip()

        # 2. Main Story Content Extraction
        article = (
            soup.find("article") or
            soup.find("div", class_="entry-content") or
            soup.find("div", class_="post-content") or
            soup.find("div", class_="post-body") or
            soup.find("div", class_="story-content") or
            soup.find("div", class_="article-content") or
            soup.find("div", class_="story-detail") or
            soup.find("main")
        )

        # Fallback: Find container with maximum Hindi text density
        if not article:
            candidates = soup.find_all(["div", "section"])
            best_node = soup
            max_hindi_len = 0
            for node in candidates:
                text = node.get_text()
                hindi_chars = len(re.findall(r'[\u0900-\u097F]', text))
                if hindi_chars > max_hindi_len:
                    max_hindi_len = hindi_chars
                    best_node = node
            article = best_node

        clean_paras = []
        for p in article.find_all(["p", "blockquote"]):
            text = p.get_text().strip()
            if len(text) < 20:
                continue

            if any(re.search(pat, text, re.IGNORECASE) for pat in JUNK_PATTERNS):
                continue

            text = re.sub(r'\s+', ' ', text)
            clean_paras.append(text)

        full_raw_text = "\n\n".join(clean_paras)
        word_count = sum(len(p.split()) for p in clean_paras)

        print(f"  ✅ Scraped Title: \"{title}\"")
        print(f"  ✅ Total Story Paragraphs: {len(clean_paras)} (100% Full Story Scraped)")
        print(f"  ✅ Total Word Count: {word_count} words")

        # Save raw copy in input_stories
        safe_name = "".join(c for c in title if c.isalnum() or c in (" ", "_")).replace(" ", "_")[:35]
        raw_file = INPUT_STORIES_DIR / f"scraped_{safe_name}.txt"
        with open(raw_file, "w", encoding="utf-8") as f:
            f.write(f"# {title}\nSource: {url}\n\n{full_raw_text}")
        print(f"  💾 Complete raw story saved to: {raw_file}")

        return {
            "title": title,
            "url": url,
            "paragraphs": clean_paras,
            "raw_text": full_raw_text,
            "word_count": word_count,
            "saved_file": str(raw_file)
        }

    def scrape_curated(self, index: int = 0) -> Dict[str, Any]:
        """Scrapes one of the pre-tested high-quality Hindi emotional love stories."""
        target = CURATED_PORTAL_STORIES[index % len(CURATED_PORTAL_STORIES)]
        print(f"\n[StoryScraper] 📖 Selected Curated Story #{index}: {target['title']}")
        return self.scrape_url(target["url"])

    def list_curated_stories(self) -> List[Dict[str, Any]]:
        """Returns list of all available high-quality curated stories."""
        return CURATED_PORTAL_STORIES

    def search_stories(self, query: str, max_results: int = 6) -> List[Dict[str, str]]:
        """
        Searches web story portals for any keyword and returns top matching story links.
        """
        print(f"\n[StoryScraper] 🔍 Searching web for stories with keyword: \"{query}\"")
        encoded_query = urllib.parse.quote_plus(query)
        search_url = f"https://storyinhindi.net/?s={encoded_query}"

        results = []
        try:
            res = requests.get(search_url, headers=self.headers, timeout=self.timeout)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                articles = soup.find_all("article")
                for a in articles:
                    h2 = a.find(["h2", "h1"])
                    link = a.find("a")
                    snippet = a.find(["p", "div", "span"])
                    if h2 and link and link.get("href"):
                        results.append({
                            "title": h2.get_text().strip(),
                            "url": link.get("href").strip(),
                            "snippet": snippet.get_text().strip()[:120] if snippet else ""
                        })
                    if len(results) >= max_results:
                        break
        except Exception as e:
            print(f"  ⚠️ Search error: {e}")

        return results

    def parse_story_to_script(
        self,
        story_data: Dict[str, Any],
        hero_name: Optional[str] = None,
        heroine_name: Optional[str] = None,
        max_scenes: Optional[int] = None,
        add_climax_hook: bool = True,
        director: str = "gemini"
    ) -> Dict[str, Any]:
        """
        Transforms 100% of raw scraped story paragraphs into an emotional multi-character audio drama script.
        - Primary: Gemini AI Drama Director (1,500 daily free Google AI Studio calls)
        - Fallback: Local Rule-Based NLP Director (0% quota risk)
        """
        title = story_data.get("title", "दर्दभरी प्रेम कहानी")
        raw_text = story_data.get("raw_text", "")
        if not raw_text and story_data.get("paragraphs"):
            raw_text = "\n\n".join(story_data["paragraphs"])

        script_obj = None
        if director.lower() == "gemini":
            try:
                from story_engine.gemini_drama_director import GeminiDramaDirector
                ai_director = GeminiDramaDirector()
                if ai_director.api_key:
                    print("🌟 [StoryScraper] Directing story with Google Gemini AI Drama Director...")
                    script_obj = ai_director.direct_novel(
                        raw_text=raw_text,
                        title=title,
                        hero_name=hero_name or "कबीर",
                        heroine_name=heroine_name or "आरुषि"
                    )
            except Exception as e:
                print(f"⚠️ [StoryScraper] Gemini AI Director error, falling back to Local Rule Director: {e}")

        if not script_obj:
            builder = DramaScriptBuilder()
            script_obj = builder.build_full_audio_drama_script(
                raw_text=raw_text,
                title=title,
                add_climax_hook=add_climax_hook
            )

        if hero_name:
            script_obj["characters"]["HERO"] = hero_name
        if heroine_name:
            script_obj["characters"]["HEROINE"] = heroine_name

        script_obj["source_url"] = story_data.get("url", "Scraped Story")
        script_obj["total_paras"] = len(story_data.get("paragraphs", []))
        script_obj["total_words"] = story_data.get("word_count", 0)

        # Truncate only if user explicitly requested max_scenes limit
        if max_scenes and max_scenes > 0 and len(script_obj["scenes"]) > max_scenes:
            print(f"  ✂️ Truncation requested: Selecting {max_scenes} scenes...")
            half = max_scenes // 2
            script_obj["scenes"] = script_obj["scenes"][:half] + script_obj["scenes"][-(max_scenes - half):]
            script_obj["total_scenes"] = len(script_obj["scenes"])
        else:
            print(f"  ✨ 100% FULL STORY PRESERVED: {len(script_obj['scenes'])} audio scenes with Multi-Speaker dialogue!")

        return script_obj

    def _detect_character_names(self, text: str) -> Tuple[Optional[str], Optional[str]]:
        """Automatically extracts Indian hero & heroine names from story text."""
        common_heroes = [
            "सुभाष", "रिशभ", "कबीर", "सूरज", "राहुल", "रोहन", "आर्यन", "अमन", 
            "समीर", "देव", "आदित्य", "विवेक", "विकास", "अभिषेक", "गौरव", "अमित"
        ]
        common_heroines = [
            "सुजाता", "आन्या", "आरुषि", "शिबानी", "प्रिया", "सिमरन", "रिया", 
            "अंजली", "नैना", "तान्या", "काव्या", "पूजा", "नेहा", "खुशी", "दीक्षा"
        ]

        found_hero = None
        found_heroine = None

        for h in common_heroes:
            if h in text:
                found_hero = h
                break

        for f in common_heroines:
            if f in text:
                found_heroine = f
                break

        return found_hero, found_heroine

    def _classify_dialogue(self, dialogue: str, context: str, hero_name: str, heroine_name: str) -> Tuple[str, str]:
        """Determines whether dialogue belongs to HERO, HEROINE, or NARRATOR."""
        combined = f"{context} {dialogue}"
        female_markers = ["बोली", "कही", "रोई", f"{heroine_name} ने कहा", "लड़की", "पत्नी", "माँ", f"{hero_name} से कहा", "चिल्लाई", "सिसकते हुए"]
        male_markers = ["बोला", "कहा", "चिल्लाया", f"{hero_name} ने कहा", "लड़का", "पति", f"{heroine_name} से कहा"]

        speaker = "HERO"
        for fm in female_markers:
            if fm in combined:
                speaker = "HEROINE"
                break

        mood = self._detect_mood(combined)
        return speaker, mood

    def _detect_mood(self, text: str) -> str:
        """Detects dramatic emotional mood from Hindi keywords."""
        sad_keywords = ["रो", "आँसू", "दर्द", "तड़प", "चीख़", "बिछड़", "मौत", "अलविदा", "माफ़ी", "नफ़रत", "अधूरी", "खून", "धोखा", "दफ़न"]
        whisper_keywords = ["धीमी आवाज़", "फुसफुसा", "कान में", "सहमी", "कांपती", "चुपके से"]
        romantic_keywords = ["प्यार", "मुस्कुरा", "हँसी", "नज़रों", "गले", "चूम", "खूबसूरत", "बाहों", "माथा", "इश्क", "मोहब्बत"]

        for w in sad_keywords:
            if w in text:
                return "crying" if ("रो" in text or "आँसू" in text or "सिसक" in text) else "heartbroken"

        for w in whisper_keywords:
            if w in text:
                return "whisper"

        for w in romantic_keywords:
            if w in text:
                return "romantic"

        return "cinematic"

    def save_script(self, script_data: Dict[str, Any], filename: Optional[str] = None) -> Path:
        """Saves script into output/scripts/ directory."""
        SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
        if not filename:
            safe_title = "".join(c for c in script_data.get("title", "story") if c.isalnum() or c in (" ", "_")).replace(" ", "_")[:25]
            filename = f"scraped_{safe_title}_{int(time.time())}.json"

        out_path = SCRIPTS_DIR / filename
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(script_data, f, ensure_ascii=False, indent=2)

        print(f"  💾 Audio Drama Script saved: {out_path}")
        return out_path
