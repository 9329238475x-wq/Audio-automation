# 🎙️ Multi-Speaker Studio Voice Reference Samples (Radio FM / Pocket FM)

यहाँ सभी 20 मुख्य पात्रों (Characters) के **Studio-Grade 24000Hz 16-bit Mono PCM WAV Files** सुरक्षित हैं।
ये सैम्पल्स Chatterbox V3 Neural TTS के `audio_prompt_path` में जाकर जीरो-शॉट वॉइस क्लोनिंग और रेडियो ब्रॉडकास्ट क्वालिटी प्रदान करते हैं।

---

### 📋 Full 20-Character Voice Cast List:

#### 👦👧 Child Speakers (बच्चे)
1. `19_child_kid_female.wav` - **छोटी बच्ची / बिटिया / पिंकी** (Sweet, lively, high-pitched innocent girl)
2. `20_child_kid_male.wav` - **छोटा बच्चा / मुन्ना / गोलू** (Playful, energetic, bright innocent boy)

#### 👩 Adult Female Speakers (महिलाएं)
3. `11_heroine_soft_female.wav` - **नायिका / हीरोइन (सॉफ्ट)** (Sweet, tender, melodious female lead)
4. `12_heroine_bold_female.wav` - **नायिका / हीरोइन (बोल्ड / बिंदास)** (Confident, articulate, modern bold female)
5. `13_sister_young_female.wav` - **बहन / दीदी** (Playful, chirpy, affectionate young sister)
6. `14_vamp_cunning_female.wav` - **वैम्प / षड्यंत्रकारी सौतन** (Cunning, sarcastic, seductive rival)
7. `15_mother_gentle_female.wav` - **ममतामयी माँ** (Affectionate, warm, gentle Indian mother)
8. `16_mother_strict_female.wav` - **सख्त माँ / सास** (Orthodox, sharp, commanding matriarch)
9. `17_bhabhi_mature_female.wav` - **भाभी / चाची** (Mature, humorous, wise sister-in-law)
10. `18_elder_grandmother_female.wav` - **दादी / नानी** (Aged, gentle, fragile, story-telling grandmother)

#### 👨 Adult Male Speakers (पुरुष)
11. `01_narrator_male.wav` - **सूत्रधार / नरेटर** (Deep, resonant baritone cinematic storyteller)
12. `02_hero_romantic_male.wav` - **नायक / हीरो (रोमांटिक)** (Passionate, emotional, loving male lead)
13. `03_hero_angry_male.wav` - **नायक / हीरो (गुस्सैल / आक्रामक)** (Fierce, intense, heartbroken male lead)
14. `04_friend_young_male.wav` - **सच्चा दोस्त / यार** (Casual, supportive, loyal young buddy)
15. `05_villain_rough_male.wav` - **खलनायक / विलेन** (Harsh, gritty, menacing, arrogant antagonist)
16. `06_father_emotional_male.wav` - **भावुक पिता** (Affectionate, burdened, loving father)
17. `07_father_strict_male.wav` - **सख्त पिता / मुखिया** (Authoritative, stern, disciplinary patriarch)
18. `08_cop_doctor_male.wav` - **दरोगा / पुलिस इंस्पेक्टर / डॉक्टर** (Firm, grave, authoritative professional)
19. `09_elder_grandfather_male.wav` - **दादाजी / नानाजी** (Wise, trembling, affectionate aged grandfather)
20. `10_servant_utility_male.wav` - **नौकर / ड्राइवर / हेल्पर** (Humble, loyal, rustic polite Indian helper)

---

### 📻 Radio FM & Cinema Acoustic Chains (Step 11 DSP)
1. **Child Chain**: High-pass @ 120Hz (zero chest rumble) + Presence EQ @ 2800Hz (+2.5dB) + Sweet de-esser @ 6000Hz (-4dB).
2. **Female Chain**: High-pass @ 80Hz + Chest Warmth @ 240Hz (+3.5dB) + Anti-Nasal @ 3400Hz (-4.5dB) + De-Esser Notch @ 4800Hz (-8dB) + Silky Roll-Off @ 5500Hz.
3. **Male Chain**: High-pass @ 65Hz + Baritone Chest @ 150Hz (+3.8dB) + Anti-Harsh @ 3200Hz (-4.5dB) + De-Sibilance @ 5200Hz (-4dB).
4. **Elderly Chain**: High-pass @ 75Hz + Mellow Body @ 200Hz (+2.5dB) + Soft high roll-off > 5200Hz.
