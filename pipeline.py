# -*- coding: utf-8 -*-
"""
Audio-Automation Master Pipeline: Desi Love, Romance & Emotional Twist Drama
Supports:
  - Testing Mode: Edge TTS (Rapid local prototyping & story flow testing)
  - Production Mode: Chatterbox V3 (Neural voice cloning & high-end audio)
"""

import os
import sys
import argparse
from pathlib import Path

# Force UTF-8 stdout on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config.settings import (
    CONFIG_DIR,
    SCRIPTS_DIR,
    AUDIO_CHUNKS_DIR,
    FINAL_MASTERS_DIR,
    DEFAULT_TTS_ENGINE
)
from story_engine.story_generator import StoryGenerator
from story_engine.script_parser import ScriptParser
from voice_engine.edge_tts_engine import EdgeTTSVoiceEngine
from voice_engine.chatterbox_tts import ChatterboxVoiceEngine
from audio_mixer.studio_mixer import StudioMixer

def run_audio_story_pipeline(
    topic: str = "आखिरी ख़त और वो बारिश की रात",
    hero_name: str = "कबीर",
    heroine_name: str = "आरुषि",
    duration_mins: int = 5,
    custom_script_path: str = None,
    output_prefix: str = "story",
    engine: str = DEFAULT_TTS_ENGINE
):
    print("=" * 72)
    print(" 💔 DESI ROMANCE & EMOTIONAL TWIST DRAMA AUDIO PIPELINE")
    print("=" * 72)
    print(f"  Topic: {topic}")
    print(f"  Hero: {hero_name} | Heroine: {heroine_name} | Target Duration: {duration_mins} min")
    print(f"  Voice Engine: {'⚡ Edge TTS (Testing Mode)' if engine == 'edge' else '🎙️ Chatterbox V3 (Production Mode)'}\n")

    # -------------------------------------------------------------
    # STAGE 1: SCRIPT GENERATION / RETRIEVAL
    # -------------------------------------------------------------
    print("--- [STAGE 1] SCRIPT ENGINE ---")
    if custom_script_path and os.path.exists(custom_script_path):
        script_file = Path(custom_script_path)
        print(f"  Using existing script: {script_file}")
    else:
        gen = StoryGenerator()
        story_data = gen.generate_story(
            topic=topic,
            duration_minutes=duration_mins,
            hero_name=hero_name,
            heroine_name=heroine_name
        )
        safe_title = "".join(c for c in topic if c.isalnum() or c in (" ", "_", "-")).rstrip().replace(" ", "_")
        script_file = list(SCRIPTS_DIR.glob(f"script_{safe_title}_*.json"))[-1]

    # -------------------------------------------------------------
    # STAGE 2: SCRIPT PARSING & VOICE MAPPING
    # -------------------------------------------------------------
    print("\n--- [STAGE 2] VOICE ALLOCATION & PARSING ---")
    voices_cfg = CONFIG_DIR / "voices_config.json"
    parser = ScriptParser(voices_cfg)
    scene_tasks = parser.parse_script(script_file)
    print(f"  Parsed {len(scene_tasks)} emotional dialogue segments.")

    # -------------------------------------------------------------
    # STAGE 3: VOICE SYNTHESIS & DSP ENHANCEMENT
    # -------------------------------------------------------------
    print(f"\n--- [STAGE 3] VOICE SYNTHESIS ({engine.upper()}) & STEP 11 DSP ---")
    if engine.lower() == "edge":
        voice_engine = EdgeTTSVoiceEngine()
    else:
        voice_engine = ChatterboxVoiceEngine()
        voice_engine.load_model()

    audio_files = []
    AUDIO_CHUNKS_DIR.mkdir(parents=True, exist_ok=True)

    for task in scene_tasks:
        idx = task["index"]
        char = task["character"]
        out_chunk = AUDIO_CHUNKS_DIR / f"chunk_{idx:03d}_{char.lower()}.wav"

        if engine.lower() == "edge":
            voice_engine.synthesize_segment(
                text=task["text"],
                output_path=out_chunk,
                character=char,
                mood=task.get("mood", "romantic"),
                auto_enhance=True
            )
        else:
            voice_engine.synthesize_segment(
                text=task["text"],
                output_path=out_chunk,
                reference_sample_path=task.get("reference_sample"),
                mood=task.get("mood", "romantic"),
                exaggeration=task.get("exaggeration", 0.65),
                cfg_weight=task.get("cfg_weight", 0.28),
                auto_enhance=True
            )
        audio_files.append(out_chunk)

    print(f"  ✅ All {len(audio_files)} voice chunks synthesized & enhanced!")

    # -------------------------------------------------------------
    # STAGE 4: STUDIO MULTI-TRACK MIXING & MASTERING
    # -------------------------------------------------------------
    print("\n--- [STAGE 4] STUDIO MULTI-TRACK MIXING & MASTERING ---")
    mixer = StudioMixer()
    master_wav, master_mp3 = mixer.mix_story(
        story_title=topic,
        scene_tasks=scene_tasks,
        audio_files=audio_files,
        output_prefix=output_prefix
    )

    # -------------------------------------------------------------
    # STAGE 5: YOUTUBE & PODCAST METADATA GENERATION
    # -------------------------------------------------------------
    print("--- [STAGE 5] METADATA & PACKAGING ---")
    meta_path = FINAL_MASTERS_DIR / f"{master_mp3.stem}_metadata.txt"
    metadata_content = f"""# 📺 YouTube & Podcast Publishing Package
Title: 💔 {topic} | सच्ची दर्दभरी प्रेम कहानी | Heart Touching Desi Romance Audio Story
Genre: Desi Love, Romance & Emotional Twist Drama
Engine: {'Edge TTS (Testing Mode)' if engine == 'edge' else 'Chatterbox V3 (Production Mode)'}

Description:
"बिछड़ के तुझसे किसी और का होना आसान न था, जो दर्द सीने में दबाया वो बयां करना आसान न था..."
सुनिए कबीर और आरुषि की एक ऐसी दर्दभरी और रूह कंपा देने वाली प्रेम कहानी, जो आपके दिल को छू जाएगी। जब तीन साल बाद एक अनसुलझा ख़त सामने आता है, तो प्यार और क़ुर्बानी की ऐसी सच्चाई खुलती है जिसे सुनकर आपकी आँखें भर आएँगी।

🎧 सर्वश्रेष्ठ अनुभव के लिए कृपया हेडफ़ोन (Headphones) का उपयोग करें।

Master Audio Files:
WAV: {master_wav}
MP3 (320kbps): {master_mp3}
"""
    with open(meta_path, "w", encoding="utf-8") as f:
        f.write(metadata_content)

    print(f"  ✅ YouTube/Podcast Metadata saved: {meta_path}")
    print("\n" + "=" * 72)
    print(" 🎉 PIPELINE EXECUTION SUCCESSFUL!")
    print(f"  Mode:        {'⚡ Testing Mode (Edge TTS)' if engine == 'edge' else '🎙️ Production (Chatterbox V3)'}")
    print(f"  Master WAV:  {master_wav}")
    print(f"  Master MP3:  {master_mp3} (320 kbps)")
    print("=" * 72)
    return master_wav, master_mp3

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Desi Love & Romance Audio Automation")
    parser.add_argument("--topic", type=str, default="आखिरी ख़त और वो बारिश की रात", help="Story Topic / Title")
    parser.add_argument("--hero", type=str, default="कबीर", help="Hero Character Name")
    parser.add_argument("--heroine", type=str, default="आरुषि", help="Heroine Character Name")
    parser.add_argument("--duration", type=int, default=5, help="Estimated duration in minutes")
    parser.add_argument("--script", type=str, default=None, help="Path to custom JSON script")
    parser.add_argument("--prefix", type=str, default="romance_drama", help="Output filename prefix")
    parser.add_argument("--engine", type=str, default=DEFAULT_TTS_ENGINE, choices=["edge", "chatterbox"], help="TTS Engine: edge (testing) or chatterbox (production)")

    args = parser.parse_args()
    run_audio_story_pipeline(
        topic=args.topic,
        hero_name=args.hero,
        heroine_name=args.heroine,
        duration_mins=args.duration,
        custom_script_path=args.script,
        output_prefix=args.prefix,
        engine=args.engine
    )
