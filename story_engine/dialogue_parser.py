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
        combined = f"{tag} {verb}".lower()

        # 1. Child speakers (Highest priority)
        if any(w in combined for w in ['बच्ची', 'बिटिया', 'पिंकी', 'गुड़िया', 'लड़की', 'कन्या', 'छुटकी', 'child_female', 'kid_female', 'little_girl']):
            return 'CHILD_FEMALE'
        if any(w in combined for w in ['बच्चा', 'मुन्ना', 'गोलू', 'छोटू', 'बालक', 'child_male', 'kid_male', 'little_boy', 'kid', 'child']):
            return 'CHILD_MALE'

        # 2. Grandparents
        if any(w in combined for w in ['दादी', 'नानी', 'अम्मा', 'बुढ़िया', 'grandmother', 'dadi', 'nani']):
            return 'GRANDMOTHER'
        if any(w in combined for w in ['दादा', 'नाना', 'बाबा', 'बूढ़ा', 'वृद्ध', 'grandfather', 'dada', 'nana']):
            return 'GRANDFATHER'

        # 3. Mothers & Saas
        if any(w in combined for w in ['सास', 'कठोर माँ', 'saas', 'सासू']):
            return 'MOTHER_STRICT'
        if any(w in combined for w in ['माँ', 'माता', 'मैया', 'मां', 'अम्मी', 'mother', 'mom', 'maa']):
            return 'MOTHER'

        # 4. Fathers & Patriarchs
        if any(w in combined for w in ['सख्त पिता', 'कड़क पिता', 'मुखिया', 'ठाकुर', 'जमींदार', 'strict_father']):
            return 'FATHER_STRICT'
        if any(w in combined for w in ['पिता', 'पिताजी', 'बापू', 'अब्बा', 'पापा', 'बाबूजी', 'father', 'dad', 'pitaji']):
            return 'FATHER'

        # 5. Professionals (Police / Doctor / Lawyer)
        if any(w in combined for w in ['डॉक्टर', 'दरोगा', 'इंस्पेक्टर', 'हवलदार', 'वकील', 'जज', 'वैद्य', 'doctor', 'cop', 'inspector']):
            return 'COP_DOCTOR'

        # 6. Sister & Bhabhi/Aunt
        if any(w in combined for w in ['बहन', 'दीदी', 'बहना', 'sister', 'didi']):
            return 'SISTER'
        if any(w in combined for w in ['भाभी', 'चाची', 'ताई', 'मौसी', 'मामी', 'bhabhi', 'chachi']):
            return 'BHABHI'

        # 7. Antagonists (Villain / Vamp)
        if any(w in combined for w in ['सौतन', 'वैम्प', 'डायन', 'षड्यंत्रकारी', 'vamp', 'sautan']):
            return 'VAMP'
        if any(w in combined for w in ['खलनायक', 'विलेन', 'गुंडा', 'बदमाश', 'दुश्मन', 'villain', 'rival', 'gunda', 'dushman']):
            return 'VILLAIN'

        # 8. Servants & Helpers
        if any(w in combined for w in ['नौकर', 'ड्राइवर', 'माली', 'रसोइया', 'सेवक', 'servant', 'driver', 'ramu', 'helper', 'peon']):
            return 'SERVANT_MALE'

        # 9. Friends
        if any(w in combined for w in ['दोस्त', 'यार', 'मित्र', 'सखा', 'friend', 'buddy', 'pal']):
            return 'FRIEND_MALE'

        # 10. Heroine (Bold vs Romantic)
        if any(w in combined for w in ['सशक्त', 'बिंदास', 'गुस्सैल नायिका', 'चीखती हुई', 'bold']):
            return 'HEROINE_BOLD'
        if heroine.lower() in combined or any(w in combined for w in ['नायिका', 'पत्नी', 'पत्नी बोली']):
            return 'HEROINE'

        # 11. Hero (Angry vs Romantic)
        if any(w in combined for w in ['गुस्से में कबीर', 'दहाड़ा', 'क्रोधित', 'गर्जना', 'angry']):
            return 'HERO_ANGRY'
        if hero.lower() in combined or any(w in combined for w in ['नायक', 'पति', 'पति बोला']):
            return 'HERO'

        # Verb-based fallback with smart alternating speaker selection
        if any(v in verb for v in ['बोली', 'कही', 'कहने लगी', 'चिल्लाई', 'फुसफुसाई']):
            return 'HEROINE' if last_spk != 'HEROINE' else 'SISTER'
        if any(v in verb for v in ['बोला', 'कहा', 'कहने लगा', 'चिल्लाया', 'दहाड़ा']):
            return 'HERO' if last_spk != 'HERO' else 'FRIEND_MALE'

        # Dynamic rotation
        return 'HEROINE' if last_spk == 'HERO' else 'HERO'

    def _determine_quote_speaker(self, quote: str, context: str, hero: str, heroine: str, last_spk: str) -> str:
        ctx_lower = context.lower()
        quote_lower = quote.lower()
        combined = f"{ctx_lower} {quote_lower}"

        # 1. Child Cues
        if any(w in combined for w in ['बच्ची', 'बिटिया', 'पिंकी', 'गुड़िया', 'पापा मुझे डर लग रहा', 'मम्मी', 'खिलौना']):
            return 'CHILD_FEMALE'
        if any(w in combined for w in ['बच्चा', 'मुन्ना', 'गोलू', 'छोटू', 'दीदी खेलेंगे', 'भैया', 'गुल्ली']):
            return 'CHILD_MALE'

        # 2. Grandparents
        if any(w in combined for w in ['दादी', 'नानी', 'पोता', 'पोती', 'अम्मा जी', 'बेटा जुग जुग जियो']):
            return 'GRANDMOTHER'
        if any(w in combined for w in ['दादा', 'नाना', 'बाबा', 'नाती', 'वृद्ध', 'हमारे ज़माने में']):
            return 'GRANDFATHER'

        # 3. Parents
        if any(w in combined for w in ['सास', 'बहू', 'कुलच्छनी', 'खानदान की नाक']):
            return 'MOTHER_STRICT'
        if any(w in combined for w in ['माँ', 'माता', 'बेटा', 'मेरे बच्चे', 'ममता', 'खाना खा ले']):
            return 'MOTHER'
        if any(w in combined for w in ['सख्त पिता', 'कड़क पिता', 'ख़ामोश', 'मेरी मर्ज़ी', 'दहलीज़ पार मत करना']):
            return 'FATHER_STRICT'
        if any(w in combined for w in ['पिता', 'पिताजी', 'बाबूजी', 'बापू', 'पापा']):
            return 'FATHER'

        # 4. Professionals
        if any(w in combined for w in ['डॉक्टर', 'मरीज', 'दवा', 'इलाज', 'दरोगा', 'थाने', 'पुलिस', 'कानून', 'वारंट', 'हथकड़ी']):
            return 'COP_DOCTOR'

        # 5. Sister & Bhabhi
        if any(w in combined for w in ['बहन', 'दीदी', 'जीजू']):
            return 'SISTER'
        if any(w in combined for w in ['भाभी', 'देवर', 'चाची']):
            return 'BHABHI'

        # 6. Antagonists
        if any(w in combined for w in ['सौतन', 'वैम्प', 'बर्बाद कर दूंगी', 'कंगाल']):
            return 'VAMP'
        if any(w in combined for w in ['खलनायक', 'विलेन', 'बदला', 'मार डालूँगा', 'दुश्मन', 'औकात']):
            return 'VILLAIN'

        # 7. Servants & Helpers
        if any(w in combined for w in ['मालिक', 'हुजूर', 'सरकार', 'साहब जी', 'गाड़ी निकालूं', 'चाय लाऊं']):
            return 'SERVANT_MALE'

        # 8. Friends
        if any(w in combined for w in ['दोस्त', 'यार', 'भाई तू चिंता मत कर', 'अरे यार']):
            return 'FRIEND_MALE'

        # 9. Main Leads
        if any(w in combined for w in ['सशक्त', 'चीखती हुई', 'मैं नहीं झुकूंगी', 'मेरी जिंदगी']):
            return 'HEROINE_BOLD'
        if heroine.lower() in ctx_lower or any(w in ctx_lower for w in ['लड़की बोली', 'नायिका', 'कही']):
            return 'HEROINE'

        if any(w in combined for w in ['गुस्से में दहाड़ा', 'चिल्लाया', 'ख़ून खौल', 'बकवास बंद करो']):
            return 'HERO_ANGRY'
        if hero.lower() in ctx_lower or any(w in ctx_lower for w in ['लड़का बोला', 'नायक', 'कहा']):
            return 'HERO'

        # Dynamic turn taking
        return 'HEROINE' if last_spk == 'HERO' else 'HERO'

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