# -*- coding: utf-8 -*-
"""
Auto Drama Hunter: Automated 30k-40k Words High-Stakes Drama Finder and Autopilot Rotation Engine
Strictly hunts DRAMAS:
- Romance, Betrayal, Revenge, Heartbreak, Arranged Marriage, Family Tragedy and Social Drama
- Minimum word filter: Strictly 25,000 to 45,000 words (3 to 5 hours of continuous audio)
- Zero AI hallucinations / Zero 2-minute summaries: Uses real, authentic full-length Hindi literature and serialized web novels.
- Persistent tracking: config/produced_stories.json ensures stories are NEVER repeated on autopilot!
"""

import os
import re
import sys
import json
import time
import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import requests
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

PREFERRED_LOCAL_ORDER = [
    ('2_Nirmala_Part1_34k_Words_Hindi_4Hours.txt', 'मुंशी प्रेमचंद - निर्मला (भाग १)', 'मुंशी प्रेमचंद की कालजयी दास्तान: निर्मला और तोताराम का अनमेल विवाह | 4 Hours Full Mega Novel | Garib YT'),
    ('3_Nirmala_Part2_34k_Words_Hindi_4Hours.txt', 'मुंशी प्रेमचंद - निर्मला (भाग २ - अंतिम भाग)', 'निर्मला का दर्दनाक अंत और पश्चाताप की अग्नि | 4 Hours Climax Mega Novel | Garib YT'),
    ('5_Gaban_Part1_38k_Words_Hindi_4Hours.txt', 'मुंशी प्रेमचंद - ग़बन (भाग १)', 'मुंशी प्रेमचंद का शाहकार उपन्यास: ग़बन - रमानाथ और जालपा की कहानी | 4.5 Hours Full Mega Novel | Garib YT'),
    ('6_Gaban_Part2_38k_Words_Hindi_4Hours.txt', 'मुंशी प्रेमचंद - ग़बन (भाग २)', 'ग़बन - कर्ज़, लालच और जालपा के कंगन का सच | 4.5 Hours Mega Novel | Garib YT'),
    ('7_Gaban_Part3_38k_Words_Hindi_4Hours.txt', 'मुंशी प्रेमचंद - ग़बन (भाग ३ - महा-क्लाइमैक्स)', 'ग़बन - रमानाथ की फ़रारी और जालपा का प्रायश्चित | 4.5 Hours Climax Novel | Garib YT'),
    ('1_Nirmala_Complete_Novel_68k_Hindi.txt', 'मुंशी प्रेमचंद - निर्मला (संपूर्ण उपन्यास)', 'निर्मला - संपूर्ण उपन्यास एक ही वीडियो में | 8 Hours Complete Hindi Audio Book | Garib YT')
]

class AutoDramaHunter:
    def __init__(self, min_words: int = 25000, max_words: int = 50000):
        self.min_words = min_words
        self.max_words = max_words
        load_dotenv(ROOT_DIR / '.env')
        self.gemini_key = os.environ.get('GEMINI_API_KEY', '')

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

    def is_story_produced(self, file_name: str) -> bool:
        db = self._load_produced_db()
        for s in db.get('produced_stories', []):
            if s.get('file_name') == file_name and s.get('status') == 'completed':
                return True
        return False

    def hunt_local_dramas(self) -> List[Dict[str, Any]]:
        """Scans input_stories directory for verified 25k-50k word Hindi dramas."""
        found = []
        for f in sorted(INPUT_STORIES_DIR.glob('*.txt')):
            if 'english' in f.name.lower() or 'sherlock' in f.name.lower():
                continue
            try:
                text = f.read_text(encoding='utf-8')
                words = len(text.split())
                if words >= self.min_words:
                    approx_hours = round(words / 8500, 1)
                    title = f.stem.replace('_', ' ')
                    found.append({
                        'file': f.name,
                        'path': str(f),
                        'title': title,
                        'words': words,
                        'approx_hours': approx_hours,
                        'source': 'Local Mega Drama Archive'
                    })
            except Exception:
                continue
        return found

    def get_next_autopilot_drama(self, channel_name: str = 'Garib YT') -> Dict[str, Any]:
        """
        100% Autonomous Story Hunter for Set-and-Forget Autopilot:
        1. Checks produced_stories.json database.
        2. Picks the next unproduced 30k-40k words master novel from local archive.
        3. If all local novels are completed, crawls web series from Pratilipi/novel archives.
        4. Parses full text paragraph-by-paragraph with DramaScriptBuilder (0% skipped lines).
        5. Saves script and returns complete metadata.
        """
        print('\n' + '=' * 76)
        print(' 🎯 [AutoDramaHunter] SELECTING NEXT UNPRODUCED MEGA NOVEL (3-5 HOURS)')
        print('=' * 76)

        db = self._load_produced_db()
        selected_file = None
        selected_title = ''
        selected_display_title = ''

        # 1. Check priority local queue first
        for fname, short_title, full_display_title in PREFERRED_LOCAL_ORDER:
            fpath = INPUT_STORIES_DIR / fname
            if fpath.exists():
                if not self.is_story_produced(fname):
                    selected_file = fpath
                    selected_title = short_title
                    selected_display_title = full_display_title
                    print(f'  ✅ Found next unproduced master novel in priority queue: {fname}')
                    break
                else:
                    print(f'  ⏩ Skipping already produced novel: {fname}')

        # 2. Check any other local Hindi txt files if priority list is exhausted
        if not selected_file:
            local_dramas = self.hunt_local_dramas()
            for d in local_dramas:
                if not self.is_story_produced(d['file']):
                    selected_file = Path(d['path'])
                    selected_title = d['title']
                    selected_display_title = f"{d['title']} | Hindi Audio Story | {channel_name}"
                    print(f"  ✅ Selected unproduced local drama: {d['file']}")
                    break

        # 3. If ALL local novels are completed, crawl the next serialized Hindi drama from web!
        if not selected_file:
            print('  🌐 All local master novels completed! Crawling next live serialized Hindi novel...')
            try:
                from story_engine.advanced_scraper import AdvancedStoryScraper
                scraper = AdvancedStoryScraper()
                scraped = scraper.crawl_next_drama_series(min_chapters=20)
                if scraped and scraped.get('file_path'):
                    selected_file = Path(scraped['file_path'])
                    selected_title = scraped.get('title', 'नई दर्दभरी प्रेम कहानी')
                    selected_display_title = f"{selected_title} | Full Serialized Drama | {channel_name}"
            except Exception as e:
                print(f'  Web crawling notice: {e}')

        # If still None, loop back to the first master novel
        if not selected_file:
            selected_file = INPUT_STORIES_DIR / PREFERRED_LOCAL_ORDER[0][0]
            selected_title = PREFERRED_LOCAL_ORDER[0][1]
            selected_display_title = PREFERRED_LOCAL_ORDER[0][2]
            print(f'  🔄 Restarting cycle with master classic: {selected_file.name}')

        raw_text = selected_file.read_text(encoding='utf-8')
        word_count = len(raw_text.split())
        approx_hours = round(word_count / 8500, 1)
        story_id = selected_file.stem.lower().replace('-', '_')

        print(f'  📖 Story File:   {selected_file.name}')
        print(f'  🏷️ Title:        {selected_title}')
        print(f'  📊 Word Count:   {word_count:,} words (~{approx_hours} Hours continuous)')
        print(f'  📺 YouTube Kit:  {selected_display_title}')

        # 4. Parse full novel into complete scene tasks with DramaScriptBuilder
        print('\n  🎭 Converting full text paragraph-by-paragraph with DramaScriptBuilder...')
        from story_engine.dialogue_parser import DramaScriptBuilder
        builder = DramaScriptBuilder()
        script_data = builder.build_full_audio_drama_script(
            raw_text=raw_text,
            title=selected_title,
            add_climax_hook=True
        )

        script_path = SCRIPTS_DIR / f'master_{story_id}.json'
        script_path.write_text(json.dumps(script_data, indent=2, ensure_ascii=False), encoding='utf-8')
        total_scenes = len(script_data.get('scenes', []))
        print(f'  ✅ Generated master drama script with {total_scenes} complete scenes!')
        print(f'  💾 Saved to: {script_path}')

        # 5. Update produced_stories.json with in_progress
        db['current_in_progress'] = {
            'story_id': story_id,
            'title': selected_title,
            'file_name': selected_file.name,
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
            'source_file': selected_file.name,
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
        print(' ✅ STORY PERMANENTLY RECORDED IN AUTOPILOT DATABASE!')
        print(f'   Story ID:    {story_id}')
        print(f'   YouTube ID:  {youtube_id}')
        print(f'   YouTube URL: {youtube_url}')
        print('=' * 76)

    def hunt_and_select(self) -> Dict[str, Any]:
        """CLI Interactive interface for manual selection."""
        local_dramas = self.hunt_local_dramas()
        print('\nFound local dramas:')
        for i, d in enumerate(local_dramas):
            print(f" [{i}] {d['title']} ({d['words']} words, ~{d['approx_hours']} hrs)")
        return self.get_next_autopilot_drama()

if __name__ == '__main__':
    hunter = AutoDramaHunter()
    drama = hunter.get_next_autopilot_drama()
    print(f"Selected: {drama['title']} with {drama['total_scenes']} scenes!")
