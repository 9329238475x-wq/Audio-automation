import os
import sys
import shutil
from pathlib import Path

# Add C:\Audio-automation to path
sys.path.insert(0, r"C:\Audio-automation")

from pipeline import run_audio_story_pipeline

AUDIO_DIR = Path(r"C:\Audio-automation")
chunks_dir = AUDIO_DIR / "output" / "audio_chunks"

# Clear old single-narrator chunks so new multi-speaker chunks are generated fresh
if chunks_dir.exists():
    for f in chunks_dir.glob("*.wav"):
        try:
            f.unlink()
        except Exception:
            pass
    print("🧹 Cleared old chunks to synthesize fresh MULTI-SPEAKER dialogue files.")

script_path = AUDIO_DIR / "output" / "scripts" / "scraped_Very_Sad_Emotional_Love_S_1791103037.json"
topic = "सुजाता और सुभाष की बेपनाह मोहब्बत की दास्तान"

print(f"\n🚀 Launching MULTI-SPEAKER Audio Drama Pipeline...")
print(f"  Script: {script_path.name}")
print(f"  Engine: Edge TTS (Multi-Speaker: Hero [Male] + Heroine [Female] + Narrator [Baritone])")

master_wav, master_mp3 = run_audio_story_pipeline(
    topic=topic,
    hero_name="सुभाष",
    heroine_name="सुजाता",
    custom_script_path=str(script_path),
    output_prefix="multi_speaker_sujata_subhash",
    engine="edge"
)

print("\n" + "="*70)
print("🎉 MULTI-SPEAKER AUDIO DRAMA MASTER COMPLETE!")
print(f"Master WAV: {master_wav}")
print(f"Master MP3: {master_mp3}")
if Path(master_mp3).exists():
    size_mb = Path(master_mp3).stat().st_size / (1024 * 1024)
    print(f"MP3 Size: {size_mb:.2f} MB")
print("="*70)