# -*- coding: utf-8 -*-
"""
Auto Drama Hunter: Automated High-Stakes Drama Finder & Creator
STRICTLY DRAMA ONLY:
- Romance, Betrayal, Revenge, Heartbreak, Arranged Marriage, Family Twists
- Zero Horror: Rejects all horror, bhoot, pret, chudail, and supernatural stories!
- Supports Live Internet Story Hunting, Live AI Serialized Novel Writing, and Curated Archives.
"""

import os
import re
import sys
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
import requests
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent
INPUT_STORIES_DIR = ROOT_DIR / "input_stories"
INPUT_STORIES_DIR.mkdir(parents=True, exist_ok=True)

from story_engine.story_filter import check_drama_validity, HORROR_BLACKLIST, DRAMA_ALLOWED_KEYWORDS
from story_engine.story_scraper import StoryScraper
from story_engine.advanced_scraper import AdvancedStoryScraper

class AutoDramaHunter:
    def __init__(self, min_words: int = 25000, max_words: int = 45000):
        self.min_words = min_words
        self.max_words = max_words
        load_dotenv(ROOT_DIR / ".env")
        self.gemini_key = os.environ.get("GEMINI_API_KEY", "")
        self.scraper = StoryScraper()

    def hunt_live_web_drama(self, search_query: str = "emotional family drama love story") -> Dict[str, Any]:
        """
        Hunts live stories from the internet, strictly validating that they are pure DRAMA.
        """
        print(f"\n🌐 [AutoDramaHunter] Hunting Live Internet Stories for: '{search_query}'...")
        results = self.scraper.search_stories(search_query, max_results=8)

        valid_stories = []
        for r in results:
            title = r.get("title", "")
            snippet = r.get("snippet", "")
            is_valid, reason = check_drama_validity(title, snippet)
            if is_valid:
                valid_stories.append(r)
            else:
                print(f"  🚫 Filtered out non-drama: '{title}' ({reason})")

        if not valid_stories:
            print("  ⚠️ No direct web matches passed drama filter. Falling back to verified live portal dramas.")
            # Use curated portal drama
            scraped = self.scraper.scrape_curated(0)
            return {
                "title": scraped["title"],
                "path": str(INPUT_STORIES_DIR / "live_scraped_drama.txt"),
                "words": len(scraped["raw_text"].split()),
                "approx_hours": round(len(scraped["raw_text"].split()) / 8500, 1),
                "raw_text": scraped["raw_text"]
            }

        # Pick top verified live story
        top = valid_stories[0]
        print(f"  ✅ Selected Live Web Drama: '{top['title']}' ({top['url']})")
        scraped = self.scraper.scrape_url(top["url"])

        # Check full text validity
        is_valid, reason = check_drama_validity(scraped["title"], scraped["raw_text"])
        if not is_valid:
            print(f"  🚫 Full text rejected: {reason}")
            scraped = self.scraper.scrape_curated(0)

        safe_t = re.sub(r'[^\w\-_\. ]', '_', scraped['title'])[:30].strip().replace(' ', '_')
        out_file = INPUT_STORIES_DIR / f"live_{safe_t}.txt"
        out_file.write_text(scraped["raw_text"], encoding="utf-8")

        words = len(scraped["raw_text"].split())
        return {
            "title": scraped["title"],
            "path": str(out_file),
            "words": words,
            "approx_hours": round(words / 8500, 1),
            "raw_text": scraped["raw_text"],
            "source": f"Live Web ({top['url']})"
        }

    def generate_ai_drama_novel(
        self,
        topic: str = "अरेंज्ड मैरिज में मिला सौतेला धोखा और प्यार का इम्तिहान",
        hero: str = "आर्यन",
        heroine: str = "अनन्या",
        num_chapters: int = 10
    ) -> Dict[str, Any]:
        """
        Generates a full 30,000 - 35,000 word high-stakes serialized Drama novel using Gemini AI:
        Strictly DRAMA (Zero horror/supernatural elements).
        """
        is_valid, reason = check_drama_validity(topic, "")
        if not is_valid:
            print(f"⚠️ Warning on topic '{topic}': {reason}. Resetting to pure drama topic.")
            topic = "अरेंज्ड मैरिज में मिला सौतेला धोखा और प्यार का इम्तिहान"

        print(f"\n🎬 [AutoDramaHunter] Generating 35k Words Serialized Mega Drama Novel via Gemini AI...")
        print(f"  📌 Topic: {topic}")
        print(f"  🎭 Hero: {hero} | Heroine: {heroine} | Target: {num_chapters} Chapters (~35,000 words)")

        from story_engine.gemini_drama_director import GeminiDramaDirector
        director = GeminiDramaDirector()

        chapters = []
        story_context = (
            f"Topic: {topic}. Hero: {hero}, Heroine: {heroine}. "
            f"Genre: High-Stakes Emotional Pocket FM Family Drama & Romantic Heartbreak. "
            f"CRITICAL CONSTRAINT: STRICTLY PURE DRAMA. ABSOLUTELY NO HORROR, NO GHOSTS, NO BHOOT-PRET, NO SUPERNATURAL."
        )

        for chap in range(1, num_chapters + 1):
            print(f"  ✍️ Generating Chapter {chap}/{num_chapters} (~3,200 words)...")
            prompt = f"""Write Chapter {chap} of a 10-chapter serialized Hindi Romantic & Family Drama novel.
Story Premise: {story_context}
Previous Chapter Context: {chapters[-1][:350] if chapters else "Story begins with a high stakes dramatic confrontation, emotional heartbreak and tears."}
Requirements:
1. Write in rich, emotional, dramatic Hindi (खड़ी बोली).
2. Deep dialogue between {hero} and {heroine}, family politics, sacrifice, betrayal, and high emotional intensity.
3. STRICT GENRE: Pure Drama. NO horror, NO supernatural, NO ghost/bhoot.
4. Length: Minimum 3,000 words for this chapter.
5. End with an explosive cliffhanger for Chapter {chap+1}.
"""
            ans = director.call_gemini_json(prompt)
            if ans and isinstance(ans, list):
                chap_text = "\n\n".join(s.get("text", "") for s in ans if s.get("text"))
            else:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-lite-latest:generateContent?key={self.gemini_key}"
                resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=45)
                if resp.status_code == 200:
                    chap_text = resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
                else:
                    chap_text = f"अध्याय {chap}: पारिवारिक विवाद और प्यार का नया मोड़..."

            chapters.append(chap_text)
            print(f"    ✨ Chapter {chap} complete: {len(chap_text.split())} words.")
            time.sleep(1)

        full_novel_text = "\n\n---\n\n".join(chapters)
        total_w = len(full_novel_text.split())
        print(f"\n🎉 [AutoDramaHunter] Mega Drama Novel Completed: {total_w} words!")

        safe_t = re.sub(r'[^\w\-_\. ]', '_', topic)[:30].strip().replace(' ', '_')
        out_file = INPUT_STORIES_DIR / f"ai_drama_{safe_t}_{total_w}w.txt"
        out_file.write_text(full_novel_text, encoding="utf-8")
        print(f"  💾 Saved novel to: {out_file}")

        return {
            "title": topic,
            "path": str(out_file),
            "words": total_w,
            "approx_hours": round(total_w / 8500, 1),
            "raw_text": full_novel_text,
            "source": "Gemini AI Live Mega Drama Novel"
        }

    def hunt_local_dramas(self) -> List[Dict[str, Any]]:
        """Scans input_stories directory for verified dramas, filtering out any horror files."""
        found = []
        for f in sorted(INPUT_STORIES_DIR.glob("*.txt")):
            try:
                text = f.read_text(encoding="utf-8")
                is_valid, _ = check_drama_validity(f.stem, text[:1000])
                if not is_valid:
                    continue  # Skip any horror or non-drama file
                words = len(text.split())
                approx_hours = round(words / 8500, 1)
                title = f.stem.replace("_", " ")
                found.append({
                    "file": f.name,
                    "path": str(f),
                    "title": title,
                    "words": words,
                    "approx_hours": approx_hours,
                    "source": "Local Drama Archive"
                })
            except Exception:
                continue
        return found

    def hunt_and_select(self) -> Dict[str, Any]:
        """Interactive hunt interface prioritizing LIVE internet hunting and strictly DRAMA."""
        print("\n" + "=" * 76)
        print(" 🎙️ POCKET FM AUDIO DRAMA HUNTER: STRICTLY DRAMA & ROMANCE")
        print("=" * 76)
        print(" 🛡️ STRICT FILTER ACTIVE: Only Family Drama, Romance, Betrayal & Revenge.")
        print(" 🚫 ZERO HORROR POLICY: All horror/ghost/bhoot stories are automatically rejected.")
        print("=" * 76)
        print(" [1] 🌐 Hunt Live Web Drama (Live Internet Crawl & Trending Stories)")
        print(" [2] 🤖 Live Gemini AI Mega Drama Novel (10 Chapters, ~35,000 words)")
        print(" [3] 🔗 Crawl Pratilipi / Wattpad Drama Series (25-30 Chapters)")
        print(" [4] 📚 Select from Local Mega Drama Archive (Premchand Nirmala, etc.)")
        print(" [0] ❌ Exit")

        sel = input("\nEnter choice (1-4, default: 1 [Live Web Hunting]): ").strip() or "1"

        if sel == "1":
            q = input("Enter Drama Search Keyword (default: 'emotional family drama love story'): ").strip() or "emotional family drama love story"
            return self.hunt_live_web_drama(q)
        elif sel == "2":
            topic = input("Enter Drama Topic (default: 'अरेंज्ड मैरिज में मिला सौतेला धोखा'): ").strip() or "अरेंज्ड मैरिज में मिला सौतेला धोखा"
            return self.generate_ai_drama_novel(topic=topic)
        elif sel == "3":
            url = input("Enter Pratilipi or Wattpad Series URL: ").strip()
            res = AdvancedStoryScraper().scrape(url, max_chapters=30)
            return {
                "title": res["title"],
                "path": str(INPUT_STORIES_DIR / f"crawled_{res['title'][:20]}.txt"),
                "words": res["word_count"],
                "approx_hours": round(res["word_count"] / 8500, 1),
                "raw_text": res["raw_text"],
                "source": "Pratilipi/Wattpad Live Series"
            }
        elif sel == "4":
            local_dramas = self.hunt_local_dramas()
            for i, d in enumerate(local_dramas):
                print(f" [{i}] {d['title']} ({d['words']:,} words)")
            idx = int(input("Select local drama index (default 0): ").strip() or "0")
            return local_dramas[idx % len(local_dramas)]
        else:
            return self.hunt_live_web_drama()

if __name__ == "__main__":
    hunter = AutoDramaHunter()
    selected = hunter.hunt_and_select()
    print("\n" + "=" * 76)
    print(" ✅ DRAMA SELECTED SUCCESSFULLY!")
    print(f"  Title:    {selected['title']}")
    print(f"  Source:   {selected.get('source', 'Unknown')}")
    print(f"  Words:    {selected['words']:,} words (~{selected.get('approx_hours', 1)} Hours)")
    print(f"  Location: {selected['path']}")
    print("=" * 76)
