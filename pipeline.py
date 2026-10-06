# -*- coding: utf-8 -*-
"""
Audio-Automation Master Pipeline: Desi Love, Romance & Emotional Twist Drama
Supports:
  - Testing Mode: Edge TTS (Rapid local prototyping & story flow testing)
  - Production Mode: Chatterbox V3 (Neural voice cloning & high-end audio)
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Force UTF-8 stdout on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config.settings import (
    CHANNEL_NAME,
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
    engine: str = DEFAULT_TTS_ENGINE,
    render_video: bool = True,
    thumbnail_path: str = None,
    channel_name: str = CHANNEL_NAME,
    clear_cache: bool = True
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
    if clear_cache:
        print("  🧹 Purging old audio chunks to ensure 100% fresh, loud, effect-free audio...")
        for old_f in AUDIO_CHUNKS_DIR.glob("*.wav"):
            try:
                old_f.unlink()
            except Exception:
                pass

    total_tasks = len(scene_tasks)
    for task in scene_tasks:
        idx = task["index"]
        char = task["character"]
        out_chunk = AUDIO_CHUNKS_DIR / f"chunk_{idx:05d}_{char.lower()}.wav"

        # Smart Cache & Crash-Resilience: Skip already synthesized chunks
        if out_chunk.exists() and out_chunk.stat().st_size > 1000:
            audio_files.append(out_chunk)
        if idx % 50 == 0:
            import gc
            gc.collect()
            try:
                import torch
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
            except Exception:
                pass
            print(f"  📊 [Progress] {idx}/{total_tasks} chunks synthesized ({idx/total_tasks*100:.1f}%)")
            if idx % 50 == 0 or idx == total_tasks:
                print(f"  ⏩ [Cached] Chunk {idx}/{total_tasks} ({idx/total_tasks*100:.1f}%) already synthesized.")
            continue

        if engine.lower() == "edge":
            voice_engine.synthesize_segment(
                text=task["text"],
                output_path=out_chunk,
                character=char,
                mood=task.get("mood", "romantic"),
                auto_enhance=False
            )
        else:
            voice_engine.synthesize_segment(
                text=task["text"],
                output_path=out_chunk,
                character=char,
                reference_sample_path=task.get("reference_sample"),
                mood=task.get("mood", "romantic"),
                exaggeration=task.get("exaggeration", 0.65),
                cfg_weight=task.get("cfg_weight", 0.28),
                auto_enhance=False
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
        output_prefix=output_prefix,
        bgm_level=0.02,
        rain_level=0.0,
        voice_reverb_wet=0.0
    )

    # -------------------------------------------------------------
    # STAGE 5: FULL HD 1080P VIDEO GENERATION (RADIO FM VISUALIZER)
    # -------------------------------------------------------------
    print("\n--- [STAGE 5] FULL HD 1080P VIDEO GENERATION (RADIO FM VISUALIZER) ---")
    master_mp4 = None
    if render_video:
        try:
            import soundfile as sf
            from video_engine.video_renderer import VideoRenderer
            from seo_engine.ai_thumbnail_generator import AIThumbnailGenerator

            # 1. Resolve or Auto-Generate 16:9 Glowing Thumbnail
            if not thumbnail_path or not os.path.exists(thumbnail_path):
                # Check if script has embedded thumbnail_path
                try:
                    with open(script_file, "r", encoding="utf-8") as sf_f:
                        s_data = json.load(sf_f)
                        if s_data.get("thumbnail_path") and os.path.exists(s_data["thumbnail_path"]):
                            thumbnail_path = s_data["thumbnail_path"]
                except Exception:
                    pass

            if not thumbnail_path or not os.path.exists(thumbnail_path):
                # Auto-generate 16:9 glowing poster
                intense_text = " ".join([t.get("text", "") for t in scene_tasks[:4]])
                thumb_file = AIThumbnailGenerator().generate_story_thumbnail(
                    story_title=topic,
                    story_text=intense_text
                )
                thumbnail_path = str(thumb_file)
            
            durations = []
            for f in audio_files:
                try:
                    durations.append(sf.info(str(f)).duration)
                except Exception:
                    durations.append(3.0)
            
            v_renderer = VideoRenderer()
            master_mp4 = v_renderer.render_audio_drama_video(
                master_audio_path=master_wav,
                story_title=topic,
                scene_tasks=scene_tasks,
                segment_durations=durations,
                source_image_path=thumbnail_path if thumbnail_path and os.path.exists(thumbnail_path) else None,
                channel_name=channel_name
            )
        except Exception as vid_err:
            print(f"⚠️ [Pipeline] Video rendering notice: {vid_err}")

    # -------------------------------------------------------------
    # STAGE 6: YOUTUBE & PODCAST METADATA GENERATION
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

Master Media Files:
MP4 (1080p Video): {master_mp4 if master_mp4 else 'N/A'}
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
    if master_mp4:
        print(f"  Master MP4:  {master_mp4} (Full HD 1080p Video)")
    print("=" * 72)

    # -------------------------------------------------------------
    # STAGE 5: AUTOMATIC GMAIL NOTIFICATION UPON COMPLETION
    # -------------------------------------------------------------
    try:
        from audio_mixer.email_notifier import send_drama_complete_email
        char_dist = {}
        for t in scene_tasks:
            c = t.get("character", "NARRATOR")
            char_dist[c] = char_dist.get(c, 0) + 1
        
        # Estimate duration
        total_dur_s = len(scene_tasks) * 8.5
        dur_str = f"{round(total_dur_s/3600, 1)} Hours (~{round(total_dur_s/60)} mins)"
        word_cnt = sum(len(t.get("text", "").split()) for t in scene_tasks)
        
        send_drama_complete_email(
            story_title=topic,
            duration_str=dur_str,
            word_count=word_cnt,
            master_file_path=str(master_mp4 if master_mp4 else master_mp3),
            character_breakdown=char_dist,
            engine_name="Chatterbox V3 Neural TTS (GPU)" if engine == "chatterbox" else "Edge TTS"
        )
    except Exception as em_err:
        print(f"⚠️ [Pipeline] Email notification notice: {em_err}")

    return master_wav, master_mp3, master_mp4

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Desi Love & Romance Audio Automation")
    parser.add_argument("--topic", type=str, default="आखिरी ख़त और वो बारिश की रात", help="Story Topic / Title")
    parser.add_argument("--hero", type=str, default="कबीर", help="Hero Character Name")
    parser.add_argument("--heroine", type=str, default="आरुषि", help="Heroine Character Name")
    parser.add_argument("--duration", type=int, default=5, help="Estimated duration in minutes")
    parser.add_argument("--script", type=str, default=None, help="Path to custom JSON script")
    parser.add_argument("--prefix", type=str, default="romance_drama", help="Output filename prefix")
    parser.add_argument("--engine", type=str, default="chatterbox", choices=["chatterbox", "edge"], help="TTS Engine: edge (testing) or chatterbox (production)")
    parser.add_argument("--video", action="store_true", default=True, help="Generate Full HD 1080p MP4 Video with visualizer")
    parser.add_argument("--thumbnail", type=str, default=None, help="Optional custom background/thumbnail image path")
    parser.add_argument("--channel", type=str, default=CHANNEL_NAME, help="YouTube Channel Name branding")

    args = parser.parse_args()
    run_audio_story_pipeline(
        topic=args.topic,
        hero_name=args.hero,
        heroine_name=args.heroine,
        duration_mins=args.duration,
        custom_script_path=args.script,
        output_prefix=args.prefix,
        engine=args.engine,
        render_video=args.video,
        thumbnail_path=args.thumbnail,
        channel_name=args.channel
    )
