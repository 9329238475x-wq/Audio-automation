# 🎙️ Audio-Automation: Desi Romance & Emotional Twist Drama

पूर्णतः स्वचालित (100% Automated) हाई-क्वालिटी ऑडियो स्टोरी और ड्रामा प्रोडक्शन सिस्टम।
यह सिस्टम विशेष रूप से **💔 Desi Love, Romance & Emotional Twist Drama (दर्दभरी व रोमांटिक प्रेम कहानियाँ)** के लिए डिज़ाइन किया गया है।

---

## 🌟 मुख्य विशेषताएँ (Key Highlights)

1. **🚫 शून्य रोबोटिक आवाज़ (Strictly NO Edge TTS):**
   - केवल **Chatterbox Multilingual V3** का उपयोग।
   - प्राकृतिक मानवीय आवाज़ (Natural Human Cadence & Emotion).
   - वॉयस क्लोनिंग (Voice Cloning) सपोर्ट: अपने पसंदीदा वॉयस सैंपल्स से हर किरदार की आवाज़ क्लोन करें।

2. **🎚️ सिनेमा-ग्रेड ऑडियो एन्हांसमेंट (Step 11 DSP Engine):**
   - **Spectral Gate:** ऑडियो से बैकग्राउंड नॉइज़ और फुसफुसाहट साफ़ करता है।
   - **Dynamic Compression:** धीमी दर्दभरी आवाज़ों को उभारता है और तेज़ आवाज़ों को बैलेंस करता है।
   - **Presence EQ (3 kHz Boost):** डायलॉग्स में क्रिस्टल क्लेरिटी और गर्माहट लाता है।
   - **Loudness Normalization (-23 LUFS / -16 LUFS):** यूट्यूब और पॉडकास्ट के प्रसारण मानकों के अनुसार।

3. **🎻 इंटेलिजेंट बीजीएम और डकिंग (Dynamic BGM Ducking & SFX):**
   - जब कोई किरदार बोलता है, बैकग्राउंड म्यूज़िक अपने आप **-24 dB** तक धीमा हो जाता है।
   - जब डायलॉग रुकता है या शायरी आती है, बीजीएम खूबसूरती से **-12 dB** तक ऊपर उठता है।
   - रियलिस्टिक साउंड इफेक्ट्स (बारिश, दिल की धड़कन, ख़त खोलने की आवाज़, सिसकियाँ)।

4. **⚡ डुअल मोड (Dual Mode - Local & Kaggle GPU):**
   - **Local Mode:** लोकल टेस्टिंग, स्क्रिप्ट जनरेशन और ऑडियो मास्टरिंग।
   - **Kaggle GPU Mode:** Kaggle के फ्री T4/P100 GPU पर Chatterbox V3 चलाने के लिए रेडी-टू-रन नोटबुक व स्क्रिप्ट्स।

---

## 📁 प्रोजेक्ट स्ट्रक्चर (Directory Tree)

```text
C:\Audio-automation\
├── config\
│   ├── settings.py              # ग्लोबल सेटिंग्स, सैंपल रेट, LUFS, डकिंग पैरामीटर्स
│   └── voices_config.json       # किरदार व आवाज़ मैपिंग (कथावाचक, कबीर, आरुषि आदि)
├── story_engine\
│   ├── romance_prompts.py       # दर्दभरी प्रेम कहानियों के मास्टर प्रॉम्प्ट्स व सैंपल्स
│   ├── story_generator.py       # AI व क्यूरेटेड स्क्रिप्ट जनरेटर
│   └── script_parser.py         # स्क्रिप्ट पार्सर व टास्क शेड्यूलर
├── voice_engine\
│   ├── chatterbox_tts.py        # Chatterbox Multilingual V3 वॉइस इंजन
│   ├── text_normalizer.py       # हिंदी टेक्स्ट नॉर्मलाइज़र व विराम-चिह्न फ़िक्सर
│   └── audio_enhancer.py        # स्टेप 11 सिनेमा DSP एन्हांसर
├── audio_mixer\
│   ├── bgm_manager.py           # दर्दभरे व रोमांटिक बीजीएम (पियानो, वायलिन, गिटार)
│   ├── sfx_manager.py           # फ़ोले साउंड इफेक्ट्स (बारिश, थंडर, हार्टबीट)
│   └── studio_mixer.py          # मल्टी-ट्रैक मिक्सर व 320kbps MP3 एक्सपोर्टर
├── voice_samples\               # वॉयस क्लोनिंग के लिए रेफरेंस WAV सैंपल्स
│   ├── narrator.wav
│   ├── hero_male.wav
│   └── heroine_female.wav
├── output\
│   ├── scripts\                 # जेनरेट की गई स्क्रिप्ट JSON फ़ाइलें
│   ├── audio_chunks\            # डायलॉग ऑडियो क्लिप्स
│   └── final_masters\           # फ़ाइनल मास्टर WAV, 320kbps MP3 और यूट्यूब मेटाडेटा
├── kaggle\
│   ├── Kaggle_Chatterbox_Audio_Runner.ipynb  # 1-क्लिक Kaggle GPU नोटबुक
│   ├── kernel-metadata.json
│   └── run_kaggle_pipeline.py
├── pipeline.py                  # मास्टर एंड-टू-एंड ऑटोमेशन स्क्रिप्ट
├── run_test.py                  # कम्पलीट टेस्ट सूट
└── push_to_kaggle.py            # Kaggle पर 1-कमांड डिप्लॉयमेंट
```

---

## 🚀 कैसे चलाएं (Quick Start)

### 1. एंड-टू-एंड टेस्ट चलाएं:
```bash
cd "C:\Audio-automation"
python run_test.py
```

### 2. कोई भी नई कहानी जेनरेट व मास्टर करें:
```bash
python pipeline.py --topic "आखिरी ख़त और वो बारिश की रात" --hero "कबीर" --heroine "आरुषि"
```

### 3. Kaggle GPU पर पुश करें:
```bash
python push_to_kaggle.py
```

### 4. कस्टम वॉइस सैंपल जोड़ें:
`voice_samples/` फ़ोल्डर में 8-15 सेकंड की साफ़ WAV फ़ाइल डालें:
- `narrator.wav` (कथावाचक की आवाज़)
- `hero_male.wav` (हीरो की आवाज़)
- `heroine_female.wav` (हीरोइन की आवाज़)
