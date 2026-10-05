# -*- coding: utf-8 -*-
"""
Kavana & Pocket FM Style Hard Drama Engine
Specialized in high-stakes, explosive, non-boring romantic drama:
- Cold CEO / Billionaire Contract Romance ("Trapped By The Cold CEO")
- Enemies-to-Lovers / Toxic Obsession ("She Hates Me")
- Forced Desi Arrange Marriage Tension ("Arrange Marriage Vala Love")
- Secret Mafia Queen & Dark Romance ("My Sweet Girl is a Mafia Queen")
- Grief, Danger & Dark Protection ("After Her Boyfriend's Death")
- Bitter Exes Reunion & Unresolved Passion ("Still Yours")
"""

import json
from pathlib import Path
from typing import Dict, Any, List

KAVANA_HARD_DRAMA_STORIES = [
    {
        "id": "cold_ceo",
        "title": "Trapped By The Cold CEO (ट्रैप्ड बाय द कोल्ड सीईओ)",
        "genre": "Billionaire Hard Romance & Dominance",
        "synopsis": "तान्या सोचती थी कि वो केवल एक पीए की नौकरी कर रही है, लेकिन मुंबई के सबसे बेरहम और खौफनाक अरबपति रेयांश सिंघानिया ने उसके पिता के कर्ज़ के बदले उससे कॉन्ट्रैक्ट मैरिज की शर्त रख दी।",
        "characters": {
            "HERO": "रेयांश",
            "HEROINE": "तान्या",
            "NARRATOR": "कथावाचक"
        },
        "scenes": [
            {
                "character": "NARRATOR",
                "mood": "cinematic",
                "text": "रात के बारह बज रहे थे। सिंघानिया एम्पायर के पैंसठवें फ्लोर पर बने पेंटहाउस की कांच की खिड़कियों पर मूसलाधार बारिश टकरा रही थी। कमरे में सिर्फ सिगार के धुएं की हल्की महक थी और एक जानलेवा सन्नाटा। तान्या के सामने टेबल पर वो लीगल कॉन्ट्रैक्ट रखा था, जिस पर बड़े अक्षरों में लिखा था— मैरिज एग्रीमेंट।",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "HERO",
                "mood": "heartbroken",
                "text": "साइन करो तान्या। तुम्हारे पास सोचने के लिए सिर्फ दो मिनट हैं। या तो इस कागज़ पर तुम्हारा दस्तखत होगा, या कल सुबह तुम्हारे पिता आर्थर रोड जेल की सलाखों के पीछे होंगे।",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "HEROINE",
                "mood": "crying",
                "text": "तुम इंसान नहीं हो रेयांश! एक जानवर हो! तुम्हें क्या लगता है, तुम अपनी दौलत से मुझे खरीद सकते हो? मैं तुम्हारी इस झूठी शादी का खिलौना कभी नहीं बनूँगी!",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "NARRATOR",
                "mood": "cinematic",
                "text": "रेयांश अपनी भारी रिवॉल्विंग चेयर से उठा। उसके चेहरे पर न कोई गुस्सा था, न कोई पछतावा— सिर्फ एक सर्द, जानलेवा मुस्कान। उसने धीरे-धीरे कदम आगे बढ़ाए और तान्या को दीवार के सहारे घेर लिया। उसकी गहरी, काली आँखें तान्या के कांपते होठों पर टिक गईं।",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "HERO",
                "mood": "whisper",
                "text": "खिलौना? नहीं जान। खिलौने तो तोड़ दिए जाते हैं। तुम्हें तो मैं अपनी सांसों की तरह इस सीने में कैद रखूँगा। तुम मुझसे जितनी नफ़रत करोगी, मैं तुम्हें उतना ही अपने करीब खींचूँगा। अब ये पेन उठाओ... और अपनी ज़िंदगी मेरे नाम लिख दो।",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "HEROINE",
                "mood": "crying",
                "text": "रेयांश... प्लीज... छोड़ो मुझे... मैं सांस नहीं ले पा रही हूँ...",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "HERO",
                "mood": "whisper",
                "text": "सांस लेना भूल जाओ तान्या। क्योंकि इस कमरे में सिर्फ मेरी इजाज़त से हवा चलती है। आज की रात के बाद तुम मिसेज रेयांश सिंघानिया हो। और इस बात को याद रखना... जो मेरा है, उस पर खुदा भी हक नहीं जता सकता।",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "NARRATOR",
                "mood": "cinematic",
                "text": "तान्या के कांपते हाथों ने पेन उठाया। एक आंसू की बूंद उस सफ़ेद कागज़ पर गिरी और स्याही में घुल गई। उसे नहीं पता था कि ये शादी उसकी बर्बादी की शुरुआत थी... या एक ऐसी बेपनाह मोहब्बत की, जिसके आगे वो खुद को हारने वाली थी।",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            }
        ]
    },
    {
        "id": "she_hates_me",
        "title": "She Hates Me (शी हेट्स मी: नफ़रत से दीवानगी)",
        "genre": "Enemies to Lovers High-Voltage College Drama",
        "synopsis": "सेंट जेवियर्स कॉलेज का सबसे बिगड़ैल और ताकतवर लड़का कबीर, और कॉलेज की सबसे स्वाभिमानी टॉपर नैना। दोनों की नफ़रत पूरे कैंपस में मशहूर थी, लेकिन बारिश की उस एक तूफानी रात ने उनके बीच की दीवार तोड़ दी।",
        "characters": {
            "HERO": "कबीर",
            "HEROINE": "नैना",
            "NARRATOR": "कथावाचक"
        },
        "scenes": [
            {
                "character": "NARRATOR",
                "mood": "cinematic",
                "text": "कॉलेज की पार्किंग में तेज़ बारिश हो रही थी। नैना अपनी स्कूटी स्टार्ट करने की कोशिश कर रही थी, लेकिन तभी कबीर की ब्लैक मस्टैंग ने आंधी की तरह आकर उसका रास्ता रोक दिया। कार का दरवाज़ा खुला और कबीर भीगते हुए बाहर निकला, उसकी आँखों में वही पुरानी ज़िद और गुरूर था।",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "HEROINE",
                "mood": "heartbroken",
                "text": "कबीर! अपनी गाड़ी हटाओ यहाँ से! मुझे तुम्हारी ये घटिया हरकतें बिल्कुल बर्दाश्त नहीं हैं!",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "HERO",
                "mood": "heartbroken",
                "text": "और अगर न हटाऊँ तो? क्या करोगी मिस प्रेसिडेंट? डीन के पास जाकर फिर से मेरी शिकायत करोगी? तुम्हें लगता है कबीर मल्होत्रा तुम्हारी इन धमकियों से डरता है?",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "HEROINE",
                "mood": "crying",
                "text": "मैं तुमसे नफ़रत करती हूँ कबीर! समझ गए तुम? मुझे तुम्हारी शक्ल से, तुम्हारे नाम से, तुम्हारी मौजूदगी से घिन आती है!",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "NARRATOR",
                "mood": "cinematic",
                "text": "कबीर एक झटके में आगे बढ़ा। उसने नैना की कलाई पकड़ी और उसे अपनी तरफ खींच लिया। दोनों के बीच फासला मिट चुका था, बारिश की बूंदें उनके चेहरों से फिसल रही थीं और दोनों की तेज़ धड़कनें एक-दूसरे को सुनाई दे रही थीं।",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "HERO",
                "mood": "whisper",
                "text": "नफ़रत करती हो ना? तो फिर जब मैं पास आता हूँ तो तुम्हारी पलकें क्यों झुकती हैं? तुम्हारी ये धड़कनें इतनी बेकाबू क्यों हो जाती हैं? बोलो नैना! अपनी आँखों से कहो कि वो मुझसे झूठ बोलें!",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "HEROINE",
                "mood": "whisper",
                "text": "कबीर... छोड़ो मुझे... कोई देख लेगा...",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "HERO",
                "mood": "romantic",
                "text": "पूरी दुनिया देखे। मुझे कोई फर्क नहीं पड़ता। तुम चाहे मुझसे लाख नफ़रत करो नैना, लेकिन इस दिल की हर धड़कन पर सिर्फ तुम्हारा हक है। और ये बात तुम भी बहुत अच्छे से जानती हो।",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "NARRATOR",
                "mood": "cinematic",
                "text": "नैना की जुबान खामोश हो गई, लेकिन उसकी भीगी आँखों ने वो सब कह दिया जो वो सालों से अपने दिल में छुपाती आ रही थी। वो नफ़रत नहीं थी... वो तो एक ऐसी दीवानगी थी जिससे वो दोनों भाग रहे थे।",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            }
        ]
    },
    {
        "id": "arrange_marriage",
        "title": "Arrange Marriage Vala Love (अरेंज मैरिज वाला लव)",
        "genre": "Forced Desi Wedding & Dark Passion",
        "synopsis": "परिवार के दबाव में हुई एक अरेंज मैरिज। शादी की पहली रात देवराज जब सुहागरात के सजे कमरे में दाखिल हुआ, तो उसने अपनी दुल्हन अनन्या के सामने अपनी वो हक़ीक़त रख दी जिसे सुनकर अनन्या के होश उड़ गए।",
        "characters": {
            "HERO": "देवराज",
            "HEROINE": "अनन्या",
            "NARRATOR": "कथावाचक"
        },
        "scenes": [
            {
                "character": "NARRATOR",
                "mood": "cinematic",
                "text": "हवेली के सबसे बड़े बेडरूम में गुलाब के फूलों की महक फैली हुई थी। लाल जोड़े में सजी अनन्या घूंघट की ओट में बैठी कांप रही थी। तभी भारी दरवाज़ा खुला और देवराज अंदर दाखिल हुआ। उसने दरवाज़े की कुंडी बंद की और उसकी आवाज़ ने कमरे के सन्नाटे को चीर दिया।",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "HERO",
                "mood": "heartbroken",
                "text": "घूंघट उठा लो अनन्या। इस कमरे में कोई रस्म-ओ-रिवाज़ काम नहीं आएंगे। और न ही मैं उन मर्दों में से हूँ जो मीठी बातों से फुसलाते हैं।",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "HEROINE",
                "mood": "whisper",
                "text": "आप... आप ऐसे क्यों बात कर रहे हैं? हमारे घर वालों ने हमारी शादी की है...",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "HERO",
                "mood": "heartbroken",
                "text": "घर वालों ने एक सौदा किया है अनन्या! तुम्हारे पिता की डूबती हुई कंपनी को बचाने का सौदा। इस शादी से मुझे एक पत्नी नहीं, बल्कि अपने खानदान के लिए एक वारिस चाहिए। अगर तुम्हें लगता है कि तुम्हें यहाँ प्यार मिलेगा, तो ये सपना इसी वक्त भूल जाओ।",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "HEROINE",
                "mood": "crying",
                "text": "तो आपने मुझसे शादी ही क्यों की? अगर सिर्फ नफ़रत और सौदा था, तो मंडप में मेरे साथ सात फेरे क्यों लिए आपने?",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "NARRATOR",
                "mood": "cinematic",
                "text": "देवराज आगे बढ़ा और उसने अनन्या के लाल घूंघट को एक झटके में हटा दिया। अनन्या की रोती हुई खूबसूरत आँखें जब देवराज की सख्त आँखों से टकराईं, तो देवराज का एक पल के लिए दिल धड़कना भूल गया। लेकिन उसने अपने चेहरे पर वही कठोरता बरकरार रखी।",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "HERO",
                "mood": "whisper",
                "text": "फेरे इसलिए लिए क्योंकि मैं तुम्हें किसी और का होते हुए नहीं देख सकता था। हाँ, ये नफ़रत का रिश्ता हो सकता है... लेकिन अब इस हवेली से तुम्हारी डोली सिर्फ मेरी मर्जी से हिलेगी। तुम मेरी हो अनन्या... सिर्फ मेरी।",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "HEROINE",
                "mood": "crying",
                "text": "मैं आपकी कभी नहीं बनूँगी देवराज... कभी नहीं...",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "NARRATOR",
                "mood": "cinematic",
                "text": "अनन्या के गालों पर आंसू बह रहे थे, लेकिन देवराज की आँखों में एक अजीब सा जुनून था। उस रात उस बंद कमरे में एक ऐसी जंग शुरू हुई थी, जिसमें हारना और जीतना दोनों ही मोहब्बत के नाम होने वाला था।",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            }
        ]
    },
    {
        "id": "mafia_queen",
        "title": "My Sweet Girl is a Mafia Queen 👑🥀 (माफिया क्वीन: मासूम चेहरे का खौफ)",
        "genre": "Underworld Dark Romance & Secret Identity",
        "synopsis": "विवान अपनी गर्लफ्रेंड आरोही को एक सीधी-साधी, कॉलेज की मासूम लड़की समझता था। लेकिन जब शहर के सबसे खतरनाक अंडरवर्ल्ड डॉन ने विवान को किडनैप किया, तो आरोही ने अपना असली रूप दिखाया जिसे देखकर पूरा अंडरवर्ल्ड कांप उठा।",
        "characters": {
            "HERO": "विवान",
            "HEROINE": "आरोही",
            "NARRATOR": "कथावाचक"
        },
        "scenes": [
            {
                "character": "NARRATOR",
                "mood": "cinematic",
                "text": "एक पुराने अंधेरे वेयरहाउस में विवान लोहे की कुर्सी से बंधा हुआ था। उसके चेहरे पर खून बह रहा था। सामने शहर का बेरहम गैंगस्टर कालू खड़ा था। तभी भारी लोहे का दरवाज़ा एक धमाके के साथ खुला। सन्नाटे में हाई हील्स की खनक गूंज उठी।",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "HERO",
                "mood": "heartbroken",
                "text": "आरोही?! तुम यहाँ क्यों आई हो?! भागो यहाँ से! ये लोग तुम्हें मार देंगे!",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "NARRATOR",
                "mood": "cinematic",
                "text": "लेकिन आरोही के चेहरे पर कोई डर नहीं था। उसके हाथ में काले रंग का ओवरकोट था और आँखों में मौत जैसी ठंडक। उसके पीछे पचास हथियारबंद गाड़ियां आकर रुकीं। वेयरहाउस के सारे गुंडे कांपने लगे।",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "HEROINE",
                "mood": "heartbroken",
                "text": "कालू... तुम्हारी हिम्मत कैसे हुई मेरे विवान को छूने की? क्या तुम्हें पता नहीं है कि इस पूरे शहर का कानून मेरी उँगलियों के इशारे पर चलता है?",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "HERO",
                "mood": "whisper",
                "text": "आरोही... ये सब क्या है? तुम कौन हो?",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "NARRATOR",
                "mood": "cinematic",
                "text": "आरोही ने अपनी कमर से साइलेंसर वाली ग्लॉक निकाली और बिना पलक झपकाए कालू के पैर में गोली दाग दी। चीख पूरे वेयरहाउस में गूंज उठी। फिर वो विवान के पास आई, खून से सने उसके गाल को अपनी उँगलियों से छुआ और उसकी आँखों में देखा।",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "HEROINE",
                "mood": "romantic",
                "text": "माफ करना विवान। मैं तुमसे अपनी हक़ीक़त छुपाना चाहती थी। पूरी दुनिया के लिए मैं 'द ब्लैक क्वीन' हूँ... लेकिन तुम्हारे लिए, मैं सिर्फ तुम्हारी वही छोटी सी आरोही हूँ। अब चलो घर... तुम्हें बहुत दर्द हो रहा है।",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "NARRATOR",
                "mood": "cinematic",
                "text": "विवान अवाक रह गया। जिस लड़की को वो फूलों की तरह संभालता था, वो असल में कांटों का तख्त संभालती थी। लेकिन उस खौफनाक रात में, उसने उस माफिया क्वीन की आँखों में अपने लिए वो प्यार देखा जो दुनिया के हर डर से बड़ा था।",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            }
        ]
    },
    {
        "id": "after_death",
        "title": "After Her Boyfriend's Death (उसके जाने के बाद: खौफनाक हिफाजत)",
        "genre": "Dark Grief, Danger & Obsessive Protection",
        "synopsis": "आर्यन की रहस्यमयी मौत के बाद उसकी गर्लफ्रेंड सिया बिल्कुल अकेली पड़ गई थी। तभी आर्यन का सबसे खतरनाक और रहस्यमयी दोस्त रुद्र उसकी ज़िंदगी में आया, और उसने सिया की हिफाजत के लिए अपनी जान दांव पर लगा दी।",
        "characters": {
            "HERO": "रुद्र",
            "HEROINE": "सिया",
            "NARRATOR": "कथावाचक"
        },
        "scenes": [
            {
                "character": "NARRATOR",
                "mood": "cinematic",
                "text": "कब्रिस्तान में काले बादलों से बारिश बरस रही थी। आर्यन की ताज़ा कब्र के पास सिया घुटनों के बल बैठकर फूट-फूट कर रो रही थी। उसका पूरा वजूद भीग चुका था। तभी पीछे से एक बड़ा काला छाता उसके सिर पर आ गया। सिया ने मुड़कर देखा— वो रुद्र था।",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "HEROINE",
                "mood": "crying",
                "text": "तुम यहाँ क्यों आए हो रुद्र? आर्यन चला गया... मेरा सब कुछ खत्म हो गया! मुझे भी यहीं मर जाने दो!",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "HERO",
                "mood": "heartbroken",
                "text": "उठो सिया। ज़मीन गीली है, बीमार पड़ जाओगी। और जहाँ तक मरने की बात है... जब तक मेरी सांसें चल रही हैं, तुम्हें मौत भी छू नहीं सकती।",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "HEROINE",
                "mood": "crying",
                "text": "तुम होते कौन हो मुझे रोकने वाले? तुम तो हमेशा आर्यन से नफ़रत करते थे ना? फिर आज यहाँ हमदर्दी दिखाने क्यों आए हो?",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "NARRATOR",
                "mood": "cinematic",
                "text": "रुद्र ने सिया का हाथ पकड़कर उसे एक झटके में खड़ा किया। उसकी आँखों में एक दहकता हुआ दर्द था जो उसने कभी किसी को नहीं दिखाया था।",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "HERO",
                "mood": "whisper",
                "text": "आर्यन से नफ़रत थी क्योंकि वो तुम्हारा ख्याल नहीं रख सका! उसने अपनी जान गंवा दी और तुम्हें इन भेड़ियों के सामने अकेला छोड़ दिया। जिन लोगों ने आर्यन की कार का एक्सीडेंट करवाया था, वो अब तुम्हारी तलाश में हैं सिया। और मैंने आर्यन के मरने से पहले उससे वादा किया था... कि तुम्हारी एक भी चीख़ उन हत्यारों की मौत बनेगी।",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "HEROINE",
                "mood": "whisper",
                "text": "क्या... आर्यन का एक्सीडेंट नहीं हुआ था? उसका मर्डर हुआ था?",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "HERO",
                "mood": "heartbroken",
                "text": "हाँ। और अब तुम्हें सिर्फ मेरे साए में रहना होगा। चाहे तुम मुझसे नफ़रत करो या मुझे कातिल समझो... लेकिन मैं तुम्हें बचाऊंगा। चाहे इसके लिए मुझे पूरी दुनिया को जलाना पड़े।",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "NARRATOR",
                "mood": "cinematic",
                "text": "रुद्र ने सिया को अपने सीने से लगा लिया। बारिश का पानी और सिया के आंसू एक हो रहे थे, लेकिन उस सर्द रात में सिया को महसूस हुआ कि आर्यन के जाने के बाद, अब उसका मुहाफ़िज़ कोई आम इंसान नहीं... बल्कि एक खूंखार तूफ़ान था।",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            }
        ]
    },
    {
        "id": "still_yours",
        "title": "Still Yours (स्टिल योर्स: जुदाई और अधूरी रातें)",
        "genre": "Bitter Heartbreak & Unresolved Toxic Passion",
        "synopsis": "चार साल पहले मीरा ने समर को बिना कोई वजह बताए छोड़ दिया था। आज समर देश का सबसे बड़ा रॉकस्टार बन चुका है, और मीरा एक साधारण इवेंट मैनेजर। जब एक होटल के कमरे में दोनों का आमना-सामना हुआ, तो चार साल का दबा हुआ तूफ़ान फट पड़ा।",
        "characters": {
            "HERO": "समर",
            "HEROINE": "मीरा",
            "NARRATOR": "कथावाचक"
        },
        "scenes": [
            {
                "character": "NARRATOR",
                "mood": "cinematic",
                "text": "प्रेस कॉन्फ्रेंस खत्म होने के बाद समर अपने ग्रीन रूम में अकेला था। दरवाज़ा खुला और फाइल्स हाथ में लिए मीरा अंदर आई। समर को देखते ही उसके कदम वहीं जम गए। चार साल बाद... वही चेहरा, वही खुशबू, और वही चुभती हुई आँखें।",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "HERO",
                "mood": "heartbroken",
                "text": "चार साल मीरा। चार साल, दो महीने और ग्यारह दिन। तुमने सोचा था कि तुम मुझे एक टूटे हुए खिलौने की तरह फेंक कर अपनी नई ज़िंदगी बसा लोगी?",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "HEROINE",
                "mood": "crying",
                "text": "समर... प्लीज़, पुरानी बातें मत निकालो। मैं यहाँ सिर्फ एक इवेंट के सिलसिले में आई हूँ। ये पेपर्स साइन कर दो, मैं चली जाऊँगी।",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "HERO",
                "mood": "heartbroken",
                "text": "पेपर्स? तुम्हें लगता है मुझे इन रद्दी के टुकड़ों की परवाह है?",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "NARRATOR",
                "mood": "cinematic",
                "text": "समर ने पेपर्स छीनकर हवा में उड़ा दिए। सफेद पन्ने कमरे में बिखर गए। उसने मीरा का हाथ पकड़कर उसे अपनी ओर खींच लिया। मीरा का सीना समर के कोट से सट गया और दोनों की सांसें उलझने लगीं।",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "HERO",
                "mood": "whisper",
                "text": "मुझे जवाब चाहिए मीरा! उस रात तुम मुझे छोड़कर क्यों गई थीं? क्या मेरी मोहब्बत में कोई कमी थी? या मेरे पास तब वो दौलत नहीं थी जो आज मेरे पैरों में पड़ी है?",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "HEROINE",
                "mood": "crying",
                "text": "तुम कभी नहीं समझोगे समर! अगर मैं उस रात नहीं जाती, तो तुम्हारा करियर कभी नहीं बनता! तुम्हारे प्रोड्यूसर ने शर्त रखी थी कि अगर तुम एक शादीशुदा या रिलेशनशिप वाले लड़के रहोगे तो वो तुम्हें कभी लॉन्च नहीं करेंगे! मैंने तुम्हारी कामयाबी के लिए अपनी ज़िंदगी को नर्क बनाया था समर!",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "NARRATOR",
                "mood": "cinematic",
                "text": "कमरे में सन्नाटा छा गया। समर के हाथ ढीले पड़ गए। मीरा की आँखों से बहते आंसुओं ने समर के पत्थर बन चुके दिल को एक सेकंड में पिघला दिया। समर ने धीरे से मीरा का चेहरा अपने दोनों हाथों में थामा।",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "HERO",
                "mood": "whisper",
                "text": "पागल लड़की... उस कामयाबी की क्या औकात थी जो तुम्हारी मुस्कान से बड़ी होती? मुझे ये फेम नहीं चाहिए था मीरा... मुझे सिर्फ तुम चाहिए थीं। और आज भी... मैं सिर्फ तुम्हारा हूँ।",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            },
            {
                "character": "NARRATOR",
                "mood": "cinematic",
                "text": "मीरा समर के सीने से लगकर रो पड़ी। चार साल का दर्द, चार साल की तड़प उस एक आलिंगन में बह गई। बाहर रात की बारिश हो रही थी, और कमरे में दो टूटे हुए दिल एक बार फिर एक हो रहे थे।",
                "sfx_cue": "none",
                "bgm_cue": "romantic_sad_piano"
            }
        ]
    }
]

def get_kavana_stories() -> List[Dict[str, Any]]:
    return KAVANA_HARD_DRAMA_STORIES

def get_kavana_story_by_id(story_id: str) -> Dict[str, Any]:
    for s in KAVANA_HARD_DRAMA_STORIES:
        if s["id"] == story_id or story_id in s["title"].lower():
            return s
    return KAVANA_HARD_DRAMA_STORIES[0]
