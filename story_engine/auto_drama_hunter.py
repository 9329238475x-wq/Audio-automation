# -*- coding: utf-8 -*-
"""
Auto Drama Hunter: Autonomous Live Web Scraper & Heartbreak Romance Story Hunter
Strictly hunts Modern Romance, Broken Heart, Betrayal & Emotional Love Dramas:
- 100% Live Web Hunting: Discovers, crawls and scrapes brand new stories from the internet every run.
- Zero Stale Re-runs: Automatically tracks produced URLs & Titles in config/produced_stories.json so no story is ever repeated.
- Pocket FM & Radio Drama Genre: Pure modern romantic heartbreak, separation, tears, betrayal and emotional love.
"""

import os
import re
import sys
import json
import time
import datetime
import urllib.parse
from pathlib import Path
from typing import Dict, Any, List, Optional
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Force UTF-8 on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
INPUT_STORIES_DIR = ROOT_DIR / 'input_stories'
INPUT_STORIES_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_DIR = ROOT_DIR / 'config'
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
SCRIPTS_DIR = ROOT_DIR / 'output' / 'scripts'
SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
PRODUCED_DB_PATH = CONFIG_DIR / 'produced_stories.json'

ROMANCE_SEARCH_QUERIES = [
    'bewafa pyar ki kahani',
    'dard bhari prem kahani',
    'broken heart sad love story',
    'sachi mohabbat aur dhokha',
    'emotional heartbreak story hindi',
    'rula dene wali prem kahani',
    'adhuri mohabbat ki dastan'
]

class AutoDramaHunter:
    def __init__(self, min_words: int = 1000, max_words: int = 50000):
        self.min_words = min_words
        self.max_words = max_words
        load_dotenv(ROOT_DIR / '.env')
        self.gemini_key = os.environ.get('GEMINI_API_KEY', '')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept-Language': 'hi,en-US;q=0.9,en;q=0.8'
        }

    def _load_produced_db(self) -> Dict[str, Any]:
        if not PRODUCED_DB_PATH.exists():
            default_db = {
                'produced_stories': [],
                'current_in_progress': None,
                'last_updated': datetime.datetime.utcnow().isoformat() + 'Z'
            }
            PRODUCED_DB_PATH.write_text(json.dumps(default_db, indent=2, ensure_ascii=False), encoding='utf-8')
            return default_db
        try:
            return json.loads(PRODUCED_DB_PATH.read_text(encoding='utf-8'))
        except Exception:
            return {'produced_stories': [], 'current_in_progress': None}

    def _save_produced_db(self, db: Dict[str, Any]):
        db['last_updated'] = datetime.datetime.utcnow().isoformat() + 'Z'
        PRODUCED_DB_PATH.write_text(json.dumps(db, indent=2, ensure_ascii=False), encoding='utf-8')

    def is_story_produced(self, identifier: str) -> bool:
        """Checks if a story URL, title, or filename has already been completed."""
        if not identifier:
            return False
        db = self._load_produced_db()
        norm_id = identifier.lower().strip()
        for s in db.get('produced_stories', []):
            if s.get('status') == 'completed':
                if s.get('url') and s.get('url').lower().strip() == norm_id:
                    return True
                if s.get('title') and s.get('title').lower().strip() in norm_id:
                    return True
                if s.get('file_name') and s.get('file_name').lower().strip() == norm_id:
                    return True
                if s.get('story_id') and s.get('story_id').lower().strip() == norm_id:
                    return True
        return False

    def hunt_live_web_dramas(self) -> List[Dict[str, str]]:
        """
        Actively crawls live story portals and searches for trending Hindi Romance,
        Broken Heart, and Emotional Love stories.
        """
        print('🌐 [AutoDramaHunter] Scanning Live Web for Trending Hindi Romance & Broken Heart Stories...')
        found = []

        # 1. Scrape Live Emotional Stories Category
        try:
            cat_url = 'https://storyinhindi.net/category/emotional-stories-in-hindi/'
            r = requests.get(cat_url, headers=self.headers, timeout=12)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                for h2 in soup.find_all(['h2', 'h1', 'h3']):
                    a = h2.find('a')
                    if a and a.get('href'):
                        u = a.get('href').strip()
                        t = a.get_text().strip()
                        if u.startswith('http') and not any(s['url'] == u for s in found):
                            found.append({'title': t, 'url': u, 'source': 'Category Feed'})
        except Exception as e:
            print(f'  ⚠️ Category crawl notice: {e}')

        # 2. Search Live Portals for High-Impact Heartbreak & Romance Queries
        for q in ROMANCE_SEARCH_QUERIES:
            try:
                q_enc = urllib.parse.quote_plus(q)
                search_url = f'https://storyinhindi.net/?s={q_enc}'
                sr = requests.get(search_url, headers=self.headers, timeout=10)
                if sr.status_code == 200:
                    ssoup = BeautifulSoup(sr.text, 'html.parser')
                    for art in ssoup.find_all('article'):
                        link = art.find('a')
                        head = art.find(['h2', 'h1', 'h3'])
                        if link and head and link.get('href'):
                            u = link.get('href').strip()
                            t = head.get_text().strip()
                            if u.startswith('http') and not any(s['url'] == u for s in found):
                                found.append({'title': t, 'url': u, 'source': f'Search: {q}'})
            except Exception:
                pass

        print(f'  ✨ Discovered {len(found)} live romance & heartbreak candidate stories on the internet.')
        return found

    def get_next_autopilot_drama(self, channel_name: str = 'Garib YT') -> Dict[str, Any]:
        """
        100% Autonomous Story Hunter for Set-and-Forget Autopilot:
        1. Actively scans and hunts live Hindi Romance & Broken Heart stories on the web.
        2. Filters out any previously produced story using persistent database.
        3. Scrapes the complete full-length text live from the web URL.
        4. Parses full text with DramaScriptBuilder (0% skipped lines, pure dry loud voice).
        5. Saves script and returns complete metadata.
        """
        print('=' * 76)
        print(' 🎯 [AutoDramaHunter] LIVE WEB HUNTING: FRESH ROMANCE & BROKEN HEART STORY')
        print('=' * 76)

        db = self._load_produced_db()
        selected_story = None
        selected_title = ''
        selected_raw_text = ''
        selected_url = ''

        # 1. Scan live web stories
        live_candidates = self.hunt_live_web_dramas()

        from story_engine.story_scraper import StoryScraper
        scraper = StoryScraper()

        for c in live_candidates:
            u = c['url']
            t = c['title']
            if not self.is_story_produced(u) and not self.is_story_produced(t):
                print(f'\n  🔎 Inspecting unproduced live story: "{t}"')
                print(f'     URL: {u}')
                try:
                    scraped = scraper.scrape_url(u)
                    if scraped and len(scraped.get('paragraphs', [])) >= 5 and scraped.get('word_count', 0) >= 400:
                        selected_url = u
                        selected_title = scraped['title']
                        selected_raw_text = scraped['raw_text']
                        print(f'  ✅ Successfully scraped live story: {len(scraped.get("paragraphs", []))} paragraphs ({scraped.get("word_count")} words)')
                        break
                    else:
                        print('     ⚠️ Scraped text was too short. Trying next live candidate...')
                except Exception as scrape_err:
                    print(f'     ⚠️ Scraping notice: {scrape_err}. Trying next...')

        # 2. If web search stories are exhausted, crawl serialized Pratilipi / Wattpad series or generate AI Novel
        if not selected_raw_text:
            print('  🌐 Live single stories exhausted! Crawling serialized live Hindi drama series...')
            try:
                from story_engine.advanced_scraper import AdvancedStoryScraper
                adv_scraper = AdvancedStoryScraper()
                pratilipi_test_url = 'https://hindi.pratilipi.com/story/dard-bhari-prem-kahani'
                scraped = adv_scraper.scrape_pratilipi(pratilipi_test_url, max_episodes=20)
                if scraped and len(scraped.get('paragraphs', [])) >= 10:
                    selected_url = pratilipi_test_url
                    selected_title = scraped['title']
                    selected_raw_text = scraped['raw_text']
            except Exception as e:
                print(f'  Pratilipi crawl notice: {e}')

        # 3. AI Mega Novel Fallback (Zero horror, purely high-stakes broken romance drama)
        if not selected_raw_text:
            print('  🤖 Generating fresh serialized Romance & Heartbreak novel via AI director...')
            from hunt_drama import AutoDramaHunter as LegacyHunter
            ai_novel = LegacyHunter().generate_ai_drama_novel(
                topic='बेवफा प्यार और टूटे दिल का दर्दनाक सच',
                hero='आर्यन',
                heroine='अनन्या',
                num_chapters=8
            )
            selected_url = 'ai_live_drama_novel'
            selected_title = ai_novel['title']
            selected_raw_text = ai_novel['raw_text']

        word_count = len(selected_raw_text.split())
        approx_hours = round(word_count / 8500, 2)
        safe_t = re.sub(r'[^\w\-_\. ]', '_', selected_title)[:30].strip().replace(' ', '_')
        story_id = f"live_{safe_t}_{int(time.time())}".lower()

        out_file = INPUT_STORIES_DIR / f"{story_id}.txt"
        out_file.write_text(selected_raw_text, encoding='utf-8')

        selected_display_title = f"💔 {selected_title} | Emotional Hindi Love Story | {channel_name}"
        if len(selected_display_title) > 98:
            selected_display_title = selected_display_title[:95] + '...'

        print(f'\n  📖 Story Title:   {selected_title}')
        print(f'  🔗 Live Source:   {selected_url}')
        print(f'  📊 Word Count:    {word_count:,} words (~{approx_hours} Hours)')
        print(f'  📺 YouTube Title: {selected_display_title}')

        # 4. Parse full novel into complete scene tasks with DramaScriptBuilder (0% dropped text, 0% fake hooks)
        print('\n  🎭 Converting full scraped story paragraph-by-paragraph with DramaScriptBuilder...')
        from story_engine.dialogue_parser import DramaScriptBuilder
        builder = DramaScriptBuilder()
        script_data = builder.build_full_audio_drama_script(
            raw_text=selected_raw_text,
            title=selected_title,
            add_climax_hook=False
        )

        script_path = SCRIPTS_DIR / f'master_{story_id}.json'
        script_path.write_text(json.dumps(script_data, indent=2, ensure_ascii=False), encoding='utf-8')
        total_scenes = len(script_data.get('scenes', []))
        print(f'  ✅ Generated master drama script with {total_scenes} complete scenes!')
        print(f'  💾 Saved to: {script_path}')

        # 5. Record in produced_stories.json
        db['current_in_progress'] = {
            'story_id': story_id,
            'title': selected_title,
            'url': selected_url,
            'file_name': out_file.name,
            'word_count': word_count,
            'approx_hours': approx_hours,
            'started_at': datetime.datetime.utcnow().isoformat() + 'Z'
        }
        self._save_produced_db(db)

        leads = script_data.get('characters', {})
        hero = leads.get('HERO', 'नायक')
        heroine = leads.get('HEROINE', 'नायिका')

        return {
            'story_id': story_id,
            'title': selected_title,
            'display_title': selected_display_title,
            'script_path': str(script_path),
            'source_file': out_file.name,
            'source_url': selected_url,
            'word_count': word_count,
            'approx_hours': approx_hours,
            'hero_name': hero,
            'heroine_name': heroine,
            'total_scenes': total_scenes
        }

    def mark_story_completed(
        self,
        story_id: str,
        youtube_id: str,
        youtube_url: str,
        duration_seconds: float = 0.0
    ):
        """Records completed video details in produced_stories.json persistent database."""
        db = self._load_produced_db()
        in_prog = db.get('current_in_progress') or {}

        record = {
            'story_id': story_id,
            'title': in_prog.get('title', story_id),
            'url': in_prog.get('url', ''),
            'file_name': in_prog.get('file_name', ''),
            'word_count': in_prog.get('word_count', 0),
            'approx_hours': round(duration_seconds / 3600.0, 2) if duration_seconds else in_prog.get('approx_hours', 0),
            'youtube_id': youtube_id,
            'youtube_url': youtube_url,
            'status': 'completed',
            'completed_at': datetime.datetime.utcnow().isoformat() + 'Z'
        }

        db['produced_stories'] = [s for s in db.get('produced_stories', []) if s.get('story_id') != story_id]
        db['produced_stories'].append(record)
        db['current_in_progress'] = None
        self._save_produced_db(db)

        print('\n' + '=' * 76)
        print(' ✅ LIVE WEB STORY PERMANENTLY RECORDED IN AUTOPILOT DATABASE!')
        print(f'   Story ID:    {story_id}')
        print(f'   Title:       {record.get("title")}')
        print(f'   URL:         {record.get("url")}')
        print(f'   YouTube ID:  {youtube_id}')
        print(f'   YouTube URL: {youtube_url}')
        print('=' * 76)

if __name__ == '__main__':
    hunter = AutoDramaHunter()
    drama = hunter.get_next_autopilot_drama()
    print(f"Selected: {drama['title']} with {drama['total_scenes']} scenes!")
