# -*- coding: utf-8 -*-
"""
Story Scraper & Kavana Hard Drama Studio CLI
Specialized in high-stakes, explosive Kavana / Pocket FM style Hard Drama:
  1. Kavana Top-Charting Hard Dramas (Cold CEO, She Hates Me, Mafia Queen, Arrange Marriage, etc.)
  2. Full Web Story Scraping (100% complete story preserved without truncation)
  3. Web Search for Hard Drama & Romance Stories
  4. Local .txt Story Ingestion & Direct Text Paste
  5. Studio Audio Drama Production Pipeline
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import os
import json
import time
import argparse
from pathlib import Path

from story_engine.story_scraper import StoryScraper, CURATED_PORTAL_STORIES
from story_engine.advanced_scraper import AdvancedStoryScraper
from story_engine.kavana_hard_drama import KAVANA_HARD_DRAMA_STORIES, get_kavana_story_by_id
from pipeline import run_audio_story_pipeline
from config.settings import SCRIPTS_DIR

def save_hard_drama_script(story: dict) -> Path:
    SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    safe_title = "".join(c for c in story.get("title", "hard_drama") if c.isalnum() or c in (" ", "_")).replace(" ", "_")[:25]
    filename = f"kavana_{safe_title}_{int(time.time())}.json"
    out_path = SCRIPTS_DIR / filename
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(story, f, ensure_ascii=False, indent=2)
    return out_path

def interactive_menu(scraper: StoryScraper):
    print("\n" + "=" * 74)
    print(" 🌟 KAVANA & MULTI-SPEAKER MEGA AUDIO NOVEL STUDIO (3-4 HOURS) 🌟")
    print("=" * 74)
    print(" [1] 💎 30k-40k Words MEGA NOVELS (3 to 4 Hours Audio: Hindi Nirmala / English Sherlock)")
    print(" [2] 🌐 Scrape Web Novel (Pratilipi / Wattpad - Up to 30 Episodes/Chapters)")
    print(" [3] 📂 Load Any Local Story (.txt file from input_stories/)")
    print(" [4] 👑 Kavana Top Hard Dramas (She Hates Me, Cold CEO, Mafia Queen, etc.)")
    print(" [5] 🔍 Search Stories on Web")
    print(" [6] ✍️  Paste Story Text Directly")
    print(" [0] ❌ Exit")
    print("=" * 74)

    choice = input("Enter choice (1-6, default: 1): ").strip() or "1"
    story_data = None
    custom_script_path = None
    title = ""
    hero = "कबीर"
    heroine = "आरुषि"

    if choice == "1":
        mega_novels = [
            {
                "file": "2_Nirmala_Part1_34k_Words_Hindi_4Hours.txt",
                "title": "निर्मला (भाग 1) - मुंशी प्रेमचंद",
                "lang": "Hindi",
                "approx_hours": "3.8 Hours",
                "words": "34,113 शब्द",
                "desc": "दर्दभरी पारिवारिक भावनात्मक ड्रामा कहानी (Part 1)"
            },
            {
                "file": "3_Nirmala_Part2_34k_Words_Hindi_4Hours.txt",
                "title": "निर्मला (भाग 2) - मुंशी प्रेमचंद",
                "lang": "Hindi",
                "approx_hours": "3.8 Hours",
                "words": "34,140 शब्द",
                "desc": "दर्दभरी पारिवारिक भावनात्मक ड्रामा कहानी (Part 2 Climax)"
            },
            {
                "file": "1_Nirmala_Complete_Novel_68k_Hindi.txt",
                "title": "निर्मला (सम्पूर्ण उपन्यास) - मुंशी प्रेमचंद",
                "lang": "Hindi",
                "approx_hours": "7.6 Hours",
                "words": "68,253 शब्द",
                "desc": "सम्पूर्ण महा-उपन्यास (Full Continuous Drama)"
            },
            {
                "file": "4_Sherlock_Holmes_Hound_Baskervilles_English_59k_4Hours.txt",
                "title": "The Hound of the Baskervilles - Sherlock Holmes",
                "lang": "English",
                "approx_hours": "4.5 Hours",
                "words": "58,240 words",
                "desc": "Classic English Detective Mystery Drama"
            }
        ]
        print("\n--- 🌟 30k-40k Words MEGA NOVELS (3-4 HOURS AUDIO) ---")
        for i, n in enumerate(mega_novels):
            print(f" [{i}] {n['title']} ({n['lang']})")
            print(f"     अवधि: ~{n['approx_hours']} | शब्द: {n['words']}")
            print(f"     विवरण: {n['desc']}\n")
        idx_str = input(f"उपन्यास का नंबर चुनें (0-{len(mega_novels)-1}, default: 0): ").strip() or "0"
        try:
            sel_idx = int(idx_str)
        except ValueError:
            sel_idx = 0
        sel_novel = mega_novels[sel_idx % len(mega_novels)]
        fpath = Path(__file__).resolve().parent.parent / "input_stories" / sel_novel["file"]
        with open(fpath, "r", encoding="utf-8") as f:
            raw_text = f.read()
        paras = [p.strip() for p in raw_text.split("\n\n") if len(p.strip()) > 20]
        story_data = {
            "title": sel_novel["title"],
            "paragraphs": paras,
            "raw_text": raw_text,
            "word_count": sum(len(p.split()) for p in paras),
            "url": str(fpath)
        }
    elif choice == "2":
        url = input("\nवेबसाइट का कहानी लिंक (URL) डालें: ").strip()
        if not url:
            print("❌ कोई URL नहीं दिया गया!")
            return
        story_data = AdvancedStoryScraper().scrape(url)

    elif choice == "3":
        query = input("\nसर्च कीवर्ड लिखें (उदा: Cold CEO, Mafia, नफ़रत, अरेंज मैरिज): ").strip()
        if not query:
            query = "Cold CEO love story in hindi"
        results = scraper.search_stories(query, max_results=6)
        if not results:
            print("❌ कोई कहानी नहीं मिली!")
            return
        print(f"\n--- '{query}' के लिए कहानियाँ मिलीं ---")
        for i, r in enumerate(results):
            print(f" [{i}] {r['title']}")
            print(f"     URL: {r['url']}")
        sel = input(f"\nकहानी नंबर चुनें (0-{len(results)-1}, default: 0): ").strip() or "0"
        try:
            sel_idx = int(sel)
        except ValueError:
            sel_idx = 0
        target_url = results[sel_idx]["url"]
        story_data = AdvancedStoryScraper().scrape(target_url)

    elif choice == "4":
        print("\n--- चुनी हुई प्रसिद्ध फुल कहानियाँ ---")
        for i, s in enumerate(CURATED_PORTAL_STORIES):
            print(f" [{i}] {s['title']}")
            print(f"     विवरण: {s['description']} (~{s.get('words_approx', 0)} शब्द)")
        idx_str = input(f"\nकहानी का नंबर चुनें (0-{len(CURATED_PORTAL_STORIES)-1}, default: 0): ").strip() or "0"
        try:
            story_idx = int(idx_str)
        except ValueError:
            story_idx = 0
        story_data = scraper.scrape_curated(story_idx)

    elif choice == "5":
        input_dir = Path(__file__).resolve().parent.parent / "input_stories"
        files = list(input_dir.glob("*.txt"))
        if not files:
            print(f"❌ {input_dir} में कोई .txt फ़ाइल नहीं है!")
            return
        print("\n--- उपलब्ध कहानी फ़ाइलें ---")
        for i, f in enumerate(files):
            print(f" [{i}] {f.name}")
        sel = input(f"फ़ाइल नंबर चुनें (0-{len(files)-1}): ").strip() or "0"
        try:
            sel_f = files[int(sel)]
        except Exception:
            sel_f = files[0]
        with open(sel_f, "r", encoding="utf-8") as f:
            raw_text = f.read()
        paras = [p.strip() for p in raw_text.split("\n\n") if len(p.strip()) > 20]
        title = sel_f.stem.replace("scraped_", "").replace("_", " ")
        story_data = {
            "title": title,
            "paragraphs": paras,
            "raw_text": raw_text,
            "word_count": sum(len(p.split()) for p in paras),
            "url": str(sel_f)
        }

    elif choice == "6":
        print("\nअपनी पूरी कहानी यहाँ पेस्ट करें (समाप्त करने के लिए नई लाइन पर END लिखकर Enter दबाएं):")
        lines = []
        while True:
            try:
                line = input()
                if line.strip() == "END":
                    break
                lines.append(line)
            except EOFError:
                break
        raw_text = "\n".join(lines).strip()
        if not raw_text:
            print("❌ खाली टेक्स्ट!")
            return
        title_in = input("कहानी का शीर्षक (Title) दें: ").strip() or "हार्ड ड्रामा लव स्टोरी"
        paras = [p.strip() for p in raw_text.split("\n\n") if len(p.strip()) > 20]
        story_data = {
            "title": title_in,
            "paragraphs": paras,
            "raw_text": raw_text,
            "word_count": sum(len(p.split()) for p in paras),
            "url": "User Provided Text"
        }

    else:
        print("अलविदा!")
        return

    # If story was scraped, dramatize it 100%
    if story_data:
        print("\n--- DRAMATIZING 100% COMPLETE STORY INTO AUDIO DRAMA SCRIPT ---")
        dir_choice = input("\n🎬 Drama Director चुनें:\n  1) 🌟 Google Gemini AI Director (Recommended - Uses your 1,500 free daily calls!)\n  2) ⚡ Local Rule Director (0 API calls)\nचुनें (1/2, default: 1): ").strip() or "1"
        director_mode = "local" if dir_choice == "2" else "gemini"
        script = scraper.parse_story_to_script(story_data, max_scenes=None, director=director_mode)
        custom_script_path = scraper.save_script(script)
        title = script["title"]
        hero = script["characters"]["HERO"]
        heroine = script["characters"]["HEROINE"]

    print("\n" + "=" * 74)
    print(" 🎉 HARD DRAMA SCRIPT READY FOR PRODUCTION!")
    print(f"  Title:       {title}")
    print(f"  Script JSON: {custom_script_path}")
    print("=" * 74)

    # Prompt to run audio pipeline
    run_now = input("\nक्या आप अभी इसका स्टूडियो ऑडियो ड्रामा बनाना चाहते हैं? (Y/n): ").strip().lower()
    if run_now in ("", "y", "yes"):
        eng_choice = input("वॉइस इंजन: 1) 🎙️ Chatterbox V3 (Production Neural)  2) Edge TTS (default: 1): ").strip()
        engine = "edge" if eng_choice == "2" else "chatterbox"
        print(f"\n🚀 Launching Studio Audio Production Pipeline ({engine.upper()})...")
        run_audio_story_pipeline(
            topic=title,
            hero_name=hero,
            heroine_name=heroine,
            custom_script_path=str(custom_script_path),
            output_prefix="hard_drama",
            engine=engine
        )
    else:
        print(f"\n💡 कभी भी ऑडियो बनाने के लिए यह कमांड चलाएं:")
        print(f"  python pipeline.py --script \"{custom_script_path}\" --engine edge")


def main():
    parser = argparse.ArgumentParser(description="Kavana Hard Drama & Full Story Scraper Studio")
    parser.add_argument("--kavana", type=str, default=None, help="Kavana Story ID or Index (0 to 5, cold_ceo, she_hates_me, arrange_marriage, mafia_queen, after_death, still_yours)")
    parser.add_argument("--url", type=str, default=None, help="Direct web URL of full story to scrape")
    parser.add_argument("--index", type=int, default=None, help="Index of curated story (0 to 7)")
    parser.add_argument("--search", type=str, default=None, help="Search stories on web by keyword")
    parser.add_argument("--director", type=str, default="gemini", choices=["gemini", "local"], help="Drama Director Engine: 'gemini' (AI Director, 1500 daily free calls) or 'local' (Rule NLP)")
    parser.add_argument("--list", action="store_true", help="List all available stories")
    parser.add_argument("--file", type=str, default=None, help="Local story text file in input_stories/")
    parser.add_argument("--text", type=str, default=None, help="Direct story text string")
    parser.add_argument("--max-scenes", type=int, default=None, help="Optional: max scenes limit (Default: None = 100%% FULL STORY)")
    parser.add_argument("--run", action="store_true", help="Automatically run audio production after scraping")
    parser.add_argument("--engine", type=str, default="chatterbox", choices=["edge", "chatterbox"], help="TTS Engine: edge or chatterbox")
    parser.add_argument("--hero", type=str, default=None, help="Custom Hero Name")
    parser.add_argument("--heroine", type=str, default=None, help="Custom Heroine Name")
    parser.add_argument("--interactive", action="store_true", help="Launch interactive menu")

    args = parser.parse_args()
    scraper = StoryScraper()

    # 1. List all stories
    if args.list:
        print("\n" + "=" * 74)
        print(" 🔥 KAVANA TOP HARD DRAMA STORIES:")
        print("=" * 74)
        for i, s in enumerate(KAVANA_HARD_DRAMA_STORIES):
            print(f"  [{i}] ID: {s['id']}")
            print(f"      Title: {s['title']}")
            print(f"      Genre: {s['genre']}")
            print(f"      Synopsis: {s['synopsis']}\n")

        print("=" * 74)
        print(" 📚 CURATED FULL WEB STORIES (100% COMPLETE):")
        print("=" * 74)
        for i, s in enumerate(CURATED_PORTAL_STORIES):
            print(f"  [{i}] {s['title']}")
            print(f"      विवरण: {s['description']} (~{s.get('words_approx', 0)} शब्द)")
            print(f"      URL: {s['url']}\n")

        print("हार्ड ड्रामा ऑडियो सीधे बनाने के लिए रन करें:")
        print("  python scrape_story.py --kavana cold_ceo --run")
        print("  python scrape_story.py --kavana she_hates_me --run")
        print("  python scrape_story.py --index 0 --run")
        return

    # If no args or interactive
    if (len(sys.argv) == 1) or args.interactive:
        interactive_menu(scraper)
        return

    # 2. Kavana Hard Drama selection
    if args.kavana:
        kavana_id = args.kavana.strip()
        try:
            k_idx = int(kavana_id)
            story = KAVANA_HARD_DRAMA_STORIES[k_idx % len(KAVANA_HARD_DRAMA_STORIES)]
        except ValueError:
            story = get_kavana_story_by_id(kavana_id)

        script_path = save_hard_drama_script(story)
        print("\n" + "=" * 74)
        print(" 🔥 KAVANA HARD DRAMA LOADED SUCCESSFULLY!")
        print(f"  Title:        {story['title']}")
        print(f"  Genre:        {story['genre']}")
        print(f"  Characters:   Hero: {story['characters']['HERO']} | Heroine: {story['characters']['HEROINE']}")
        print(f"  Total Scenes: {len(story['scenes'])}")
        print(f"  Script JSON:  {script_path}")
        print("=" * 74)

        if args.run:
            print(f"\n🚀 Launching Studio Audio Production ({args.engine.upper()})...")
            run_audio_story_pipeline(
                topic=story["title"],
                hero_name=story["characters"]["HERO"],
                heroine_name=story["characters"]["HEROINE"],
                custom_script_path=str(script_path),
                output_prefix="hard_drama",
                engine=args.engine
            )
        else:
            print(f"\n💡 To produce audio: python pipeline.py --script \"{script_path}\" --engine {args.engine}")
        return

    # 3. Search web stories
    if args.search:
        results = scraper.search_stories(args.search, max_results=6)
        if not results:
            print(f"❌ No stories found for keyword: {args.search}")
            return
        print(f"\n--- SEARCH RESULTS FOR '{args.search}' ---")
        for i, r in enumerate(results):
            print(f"  [{i}] {r['title']}")
            print(f"      URL: {r['url']}")
            print(f"      Snippet: {r['snippet']}\n")
        print("To scrape any of these search results, run:")
        print(f"  python scrape_story.py --url \"{results[0]['url']}\" --run")
        return

    # 4. Scrape Source
    story_data = None
    if args.url:
        story_data = AdvancedStoryScraper().scrape(args.url)
    elif args.index is not None:
        story_data = scraper.scrape_curated(args.index)
    elif args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            file_path = Path(__file__).resolve().parent.parent / "input_stories" / args.file
        if not file_path.exists():
            print(f"❌ File not found: {args.file}")
            sys.exit(1)
        with open(file_path, "r", encoding="utf-8") as f:
            raw_text = f.read()
        paras = [p.strip() for p in raw_text.split("\n\n") if len(p.strip()) > 20]
        title = file_path.stem.replace("scraped_", "").replace("_", " ")
        story_data = {
            "title": title,
            "paragraphs": paras,
            "raw_text": raw_text,
            "word_count": sum(len(p.split()) for p in paras),
            "url": str(file_path)
        }
    elif args.text:
        raw_text = args.text
        paras = [p.strip() for p in raw_text.split("\n\n") if len(p.strip()) > 20]
        story_data = {
            "title": "हार्ड ड्रामा लव स्टोरी",
            "paragraphs": paras,
            "raw_text": raw_text,
            "word_count": sum(len(p.split()) for p in paras),
            "url": "Command Line Text"
        }
    else:
        print("[StoryScraper] Defaulting to Curated Story [0]...")
        story_data = scraper.scrape_curated(0)

    # 5. Dramatize into script (100% full story preserved)
    print("\n--- DRAMATIZING 100% COMPLETE STORY INTO AUDIO DRAMA SCRIPT ---")
    script = scraper.parse_story_to_script(
        story_data,
        hero_name=args.hero,
        heroine_name=args.heroine,
        max_scenes=args.max_scenes,
        director=args.director
    )
    script_path = scraper.save_script(script)

    print("\n" + "=" * 74)
    print(" 🎉 100% COMPLETE STORY SCRAPED & DRAMATIZED SUCCESSFULLY!")
    print(f"  Title:        {script['title']}")
    print(f"  Total Paras:  {story_data.get('paragraphs', []) and len(story_data['paragraphs'])}")
    print(f"  Total Words:  {story_data['word_count']}")
    print(f"  Total Scenes: {len(script['scenes'])} (100%% FULL STORY PRESERVED)")
    print(f"  Script JSON:  {script_path}")
    print("=" * 74)

    if args.run:
        print(f"\n🚀 Launching Studio Audio Production Pipeline ({args.engine.upper()})...")
        run_audio_story_pipeline(
            topic=script["title"],
            hero_name=script["characters"]["HERO"],
            heroine_name=script["characters"]["HEROINE"],
            custom_script_path=str(script_path),
            output_prefix="hard_drama",
            engine=args.engine
        )
    else:
        print("\n💡 To produce audio drama: python pipeline.py --script " + repr(str(script_path)) + f" --engine {args.engine}")

if __name__ == "__main__":
    main()
