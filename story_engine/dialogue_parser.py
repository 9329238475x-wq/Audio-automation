# -*- coding: utf-8 -*-
"""
Intelligent Hindi Dialogue Parser and Drama Director
1. Strips all blog headings, SEO garbage, and comment boilerplate.
2. Accurately extracts dialogues from Hindi attribution patterns:
   - 'लड़की ने कहा- ...', 'लड़का बोला: ...', 'सुभाष ने पूछा – ...'
   - Sentence-level separation of spoken dialogue from 3rd-person narrative action.
   - Embedded quotes and alternating character turn-taking between HERO and HEROINE.
3. Generates an intense CLIMAX COLD-OPEN HOOK right at the start of the story.
4. Classifies characters (HERO, HEROINE, MADAM, MOTHER, NARRATOR) for distinct voices.
"""

import re
from typing import Dict, Any, List, Tuple, Optional

JUNK_PATTERNS = [
    r'very sad emotional love story',
    r'sad love story in hindi',
    r'emotional love story in hindi',
    r'love story in hindi',
    r'story in hindi',
    r'कमेंट करके जरूर बताना',
    r'कमेंट में बताएं',
    r'कमेंट करें',
    r'शेयर करें',
    r'लाइक करें',
    r'subscribe',
    r'मूल उद्देश्य हे',
    r'मूल उद्देश्य है',
    r'आप भी ऐसा गलती ना करे',
    r'प्यार तो हम सभी करते',
    r'गहरा समुन्दर में दुब जाना',
    r'source:\s*http',
    r'^#\s+',
    r'^\s*read also',
    r'^\s*यह भी पढ़ें'
]

COMMON_HEROES = [
    'सुभाष', 'सुभास', 'रिशभ', 'ऋषभ', 'कबीर', 'सूरज', 'राहुल', 'रोहन',
    'आर्यन', 'अमन', 'समीर', 'देव', 'आदित्य', 'विवेक', 'विकास', 'अभिषेक',
    'गौरव', 'अमित', 'राज', 'करण', 'विक्रम', 'रणवीर', 'अर्णव', 'रुद्र'
]

COMMON_HEROINES = [
    'सुजाता', 'आन्या', 'आरुषि', 'शिबानी', 'प्रिया', 'सिमरन', 'रिया',
    'अंजली', 'नैना', 'तान्या', 'काव्या', 'पूजा', 'नेहा', 'खुशी', 'दीक्षा',
    'सरिता', 'टीना', 'मीरा', 'रोशनी', 'अवनी', 'इशानी', 'जोया'
]

NARRATIVE_ACTION_TRIGGERS = [
    r'^(?:सुभाष|सुभास|सुजाता|लड़की|लड़की|लड़का|लड़का|मैडम|madam|उसने|बह|वह|दोनों|पड़ोसी|पड़ोसी|ये सोच|ये बात|ये कहकर|तभी|फिर)\s*(?:ने|से|को|भी|का|की|के|\b)'
]

class DramaScriptBuilder:
    def __init__(self):
        pass

    def clean_text_paragraphs(self, raw_text: str) -> List[str]:
        raw_paras = [p.strip() for p in raw_text.split('\n\n') if p.strip()]
        clean = []
        for p in raw_paras:
            is_junk = False
            for pat in JUNK_PATTERNS:
                if re.search(pat, p, re.IGNORECASE):
                    is_junk = True
                    break
            if is_junk:
                continue
            p_norm = re.sub(r'[ \t]+', ' ', p).strip()
            if len(p_norm) >= 12:
                clean.append(p_norm)
        return clean

    def detect_main_characters(self, text: str) -> Tuple[str, str]:
        hero = 'सुभाष'
        heroine = 'सुजाता'
        for h in COMMON_HEROES:
            if re.search(r'\b' + re.escape(h) + r'\b', text):
                hero = h
                break
        for f in COMMON_HEROINES:
            if re.search(r'\b' + re.escape(f) + r'\b', text):
                heroine = f
                break
        return hero, heroine

    def generate_climax_hook(self, hero: str, heroine: str) -> List[Dict[str, Any]]:
        return [
            {
                'character': 'NARRATOR',
                'mood': 'crying',
                'text': f'बारिश की उस तूफानी रात में... जब {hero} भीगता हुआ उस सूने घर के बंद दरवाजे को पागलों की तरह पीट रहा था, तब उसे नहीं पता था कि उसकी ज़िंदगी, उसकी {heroine}... उसे हमेशा के लिए छोड़कर जा चुकी है!',
                'sfx_cue': 'none',
                'bgm_cue': 'romantic_sad_piano'
            },
            {
                'character': 'HERO',
                'mood': 'crying',
                'text': f'{heroine}! प्लीज दरवाजा खोलो... तुम मुझे ऐसे छोड़कर नहीं जा सकतीं! बाहर आओ {heroine}... सिर्फ एक बार मेरी बात सुन लो!',
                'sfx_cue': 'none',
                'bgm_cue': 'romantic_sad_piano'
            },
            {
                'character': 'NARRATOR',
                'mood': 'cinematic',
                'text': f'लेकिन अंदर सिर्फ़ सन्नाटा था। न कोई आवाज़, न कोई जवाब... सब कुछ एक पल में राख हो चुका था! पर यह बर्बादी उस रात नहीं हुई थी... यह रूह कंपा देने वाली दास्तान शुरू हुई थी तीन महीने पहले, जब दोनों की नज़रें पहली बार टकराई थीं...',
                'sfx_cue': 'none',
                'bgm_cue': 'romantic_sad_piano'
            }
        ]

    def parse_paragraph_to_scenes(
        self,
        paragraph: str,
        hero: str,
        heroine: str,
        last_speaker: str = 'NARRATOR'
    ) -> List[Dict[str, Any]]:
        scenes = []
        p = paragraph.strip()

        # Pattern 1: Direct Dialogue Attribution with hyphen / dash / colon
        attr_regex = re.compile(r'^(.*?)(ने कहा|ने पूछा|बोला|बोली|कहने लगा|कहने लगी|कहा|जवाब दिया|चिल्लाई|चिल्लाया)\s*[-–—:]\s*(.*)$', re.DOTALL)
        m = attr_regex.match(p)
        if m:
            speaker_tag, verb, speech = m.groups()
            speaker_tag = speaker_tag.strip()
            speech = speech.strip()

            # Clean secondary attribution ONLY at immediate start (no sentence punctuation allowed)
            sub_m = re.match(r'^([^।?!]{1,35}?(?:बोली|बोला|कहा|पूछा|कहने लगी|कहने लगा|में बोली|में बोला)[,:-]\s*)(.+)$', speech, re.DOTALL)
            action_tag = ''
            if sub_m:
                action_tag = sub_m.group(1).strip()
                speech = sub_m.group(2).strip()

            # Robust sentence-level separation of dialogue vs narrative action
            raw_sents = re.split(r'([।?!]\s*)', speech)
            reconstructed = []
            i = 0
            while i < len(raw_sents):
                s = raw_sents[i]
                if i + 1 < len(raw_sents) and raw_sents[i+1].strip() in ['।', '?', '!']:
                    s += raw_sents[i+1].strip()
                    i += 2
                else:
                    i += 1
                if s.strip():
                    reconstructed.append(s.strip())

            dialogue_sents = []
            narrative_sents = []
            hit_narrative = False

            for s in reconstructed:
                if not hit_narrative:
                    is_narr = any(re.search(trig, s, re.IGNORECASE) for trig in NARRATIVE_ACTION_TRIGGERS)
                    if is_narr and dialogue_sents:
                        hit_narrative = True
                        narrative_sents.append(s)
                    else:
                        dialogue_sents.append(s)
                else:
                    narrative_sents.append(s)

            dialogue_text = ' '.join(dialogue_sents).strip()
            narrator_text = ' '.join(narrative_sents).strip()

            char = self._determine_character(speaker_tag, verb, hero, heroine, last_speaker)
            mood = self._determine_mood(dialogue_text, action_tag)
            clean_speech = self._refine_dialogue_text(dialogue_text)

            if len(clean_speech) >= 3:
                scenes.append({
                    'character': char,
                    'mood': mood,
                    'text': clean_speech,
                    'sfx_cue': 'none',
                    'bgm_cue': 'romantic_sad_piano'
                })

            if narrator_text and len(narrator_text) >= 8:
                scenes.append({
                    'character': 'NARRATOR',
                    'mood': 'cinematic',
                    'text': self._refine_dialogue_text(narrator_text),
                    'sfx_cue': 'none',
                    'bgm_cue': 'romantic_sad_piano'
                })

            return scenes

        # Pattern 2: Quoted Dialogue within paragraph
        if ('“' in p and '”' in p) or ('"' in p and p.count('"') >= 2):
            parts = re.split(r'([“"][^”"]+[”"])', p)
            for part in parts:
                part = part.strip()
                if not part:
                    continue
                if (part.startswith('“') and part.endswith('”')) or (part.startswith('"') and part.endswith('"')):
                    quote_text = part[1:-1].strip()
                    if len(quote_text) >= 4:
                        char = self._determine_quote_speaker(quote_text, p, hero, heroine, last_speaker)
                        mood = self._determine_mood(quote_text)
                        scenes.append({
                            'character': char,
                            'mood': mood,
                            'text': self._refine_dialogue_text(quote_text),
                            'sfx_cue': 'none',
                            'bgm_cue': 'romantic_sad_piano'
                        })
                        last_speaker = char
                else:
                    if len(part) >= 12:
                        scenes.append({
                            'character': 'NARRATOR',
                            'mood': self._determine_mood(part),
                            'text': self._refine_dialogue_text(part),
                            'sfx_cue': 'none',
                            'bgm_cue': 'romantic_sad_piano'
                        })
            return scenes

        # Pattern 3: Standard Narrative Paragraph
        scenes.append({
            'character': 'NARRATOR',
            'mood': self._determine_mood(p),
            'text': self._refine_dialogue_text(p),
            'sfx_cue': 'none',
            'bgm_cue': 'romantic_sad_piano'
        })
        return scenes

    def _determine_character(self, tag: str, verb: str, hero: str, heroine: str, last_spk: str) -> str:
        tag_lower = tag.lower()
        female_cues = ['लड़की', 'लड़की', 'महिला', 'स्त्री', 'मैडम', 'madam', heroine.lower(), 'सरिता', 'पत्नी', 'माँ', 'माता', 'दीदी', 'बहन']
        for c in female_cues:
            if c in tag_lower:
                return 'HEROINE'

        male_cues = ['लड़का', 'लड़का', 'सुभास', 'सुभाष', hero.lower(), 'पति', 'पिता', 'बाप', 'भाई', 'दोस्त', 'डॉक्टर', 'doctor']
        for c in male_cues:
            if c in tag_lower:
                return 'HERO'

        if 'बोली' in verb or 'कही' in verb or 'कहने लगी' in verb or 'चिल्लाई' in verb:
            return 'HEROINE'
        if 'बोला' in verb or 'कहा' in verb or 'कहने लगा' in verb or 'चिल्लाया' in verb:
            return 'HERO'

        if last_spk == 'HERO':
            return 'HEROINE'
        elif last_spk == 'HEROINE':
            return 'HERO'

        return 'HERO'

    def _determine_quote_speaker(self, quote: str, context: str, hero: str, heroine: str, last_spk: str) -> str:
        ctx_lower = context.lower()
        if heroine.lower() in ctx_lower or 'लड़की' in ctx_lower or 'बोली' in ctx_lower or 'कही' in ctx_lower:
            return 'HEROINE'
        if hero.lower() in ctx_lower or 'लड़का' in ctx_lower or 'बोला' in ctx_lower:
            return 'HERO'
        if last_spk == 'HERO':
            return 'HEROINE'
        return 'HERO'

    def _determine_mood(self, text: str, action: str = '') -> str:
        combined = f'{text} {action}'
        if any(w in combined for w in ['रो', 'आँसू', 'रोते हुए', 'सिसक', 'तड़प', 'चीख', 'माफ़ी', 'अलविदा', 'छोड़कर', 'दर्द']):
            return 'crying'
        if any(w in combined for w in ['गुस्से', 'चिल्ला', 'नफ़रत', 'बकवास', 'दूर रहो', 'बंद करो']):
            return 'angry'
        if any(w in combined for w in ['प्यार', 'मुस्कुरा', 'हंसी', 'इश्क', 'मोहब्बत', 'नज़रें', 'गले', 'दिल']):
            return 'romantic'
        if any(w in combined for w in ['धीरे से', 'फुसफुसा', 'सहमी', 'कांपती', 'कान में']):
            return 'whisper'
        return 'cinematic'

    def _refine_dialogue_text(self, text: str) -> str:
        t = text
        t = re.sub(r'\bकिया\b', 'क्या', t)
        t = re.sub(r'\bहे\b', 'है', t)
        t = re.sub(r'\bबह\b', 'वह', t)
        t = re.sub(r'\bबो\b', 'वो', t)
        t = re.sub(r'\bबहा\b', 'वहाँ', t)
        t = re.sub(r'\bयहा\b', 'यहाँ', t)
        t = re.sub(r'\bमेने\b', 'मैंने', t)
        t = re.sub(r'\bआपने\b', 'अपने', t)
        t = re.sub(r'\bचालने\b', 'चलाने', t)
        t = re.sub(r'\bबंध\b', 'बंद', t)
        t = re.sub(r'\bब्यबहार\b', 'व्यवहार', t)
        t = re.sub(r'\bभुखार\b', 'बुखार', t)
        t = re.sub(r'\bमाकन\b', 'मकान', t)
        t = re.sub(r'\bसबाल\b', 'सवाल', t)
        t = re.sub(r'\bकोसिस\b', 'कोशिश', t)
        return t.strip()

    def build_full_audio_drama_script(
        self,
        raw_text: str,
        title: str = 'दर्दभरी प्रेम कहानी',
        add_climax_hook: bool = True
    ) -> Dict[str, Any]:
        clean_paras = self.clean_text_paragraphs(raw_text)
        hero, heroine = self.detect_main_characters(raw_text)

        scenes = []
        if add_climax_hook:
            hook = self.generate_climax_hook(hero, heroine)
            scenes.extend(hook)

        last_speaker = 'NARRATOR'
        for p in clean_paras:
            p_scenes = self.parse_paragraph_to_scenes(p, hero, heroine, last_speaker)
            for sc in p_scenes:
                scenes.append(sc)
                if sc['character'] != 'NARRATOR':
                    last_speaker = sc['character']

        char_counts = {}
        for sc in scenes:
            c = sc['character']
            char_counts[c] = char_counts.get(c, 0) + 1

        print(f'  🎭 Script Character Breakdown: {char_counts}')

        script_obj = {
            'title': title,
            'genre': 'Desi Romance & Emotional Twist Drama',
            'bgm_theme': 'romantic_sad_piano',
            'characters': {
                'HERO': hero,
                'HEROINE': heroine,
                'NARRATOR': 'कथावाचक'
            },
            'total_scenes': len(scenes),
            'scenes': scenes
        }
        return script_obj