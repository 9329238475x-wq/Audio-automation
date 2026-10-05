# -*- coding: utf-8 -*-
"""
Studio Video Renderer with Smartphone Music Player Header, Channel Branding, and Subtitles.
"""

import os
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Any

from config.settings import FINAL_MASTERS_DIR, CHANNEL_NAME
from video_engine.subtitle_builder import SubtitleBuilder
from video_engine.canvas_generator import CanvasGenerator

class VideoRenderer:
    def __init__(self):
        self.canvas_gen = CanvasGenerator()
        self.sub_builder = SubtitleBuilder()

    def render_audio_drama_video(
        self,
        master_audio_path: Path,
        story_title: str,
        scene_tasks: List[Dict[str, Any]],
        segment_durations: List[float],
        channel_name: str = CHANNEL_NAME,
        output_mp4_path: Optional[Path] = None,
        source_image_path: Optional[Path] = None,
        initial_offset_s: float = 0.5,
        pause_between_s: float = 0.40
    ) -> Path:
        master_audio_path = Path(master_audio_path)
        if not master_audio_path.exists():
            raise FileNotFoundError(f"Master audio not found: {master_audio_path}")

        if not output_mp4_path:
            FINAL_MASTERS_DIR.mkdir(parents=True, exist_ok=True)
            output_mp4_path = FINAL_MASTERS_DIR / f"{master_audio_path.stem}.mp4"
        else:
            output_mp4_path = Path(output_mp4_path)

        duration_s = self._get_duration(master_audio_path)
        print(f"\n[VideoRenderer] Rendering 1080p Video for: '{story_title}' ({duration_s:.1f}s / {duration_s/60:.2f} min)...")
        print(f"  Channel: {channel_name} | Phone-Player Center Marquee: Active (Zero Patti)")

        # 1. Build 1080p Backdrop Canvas (Top 100% clean, no patti; subtle lower vignette)
        canvas_path = output_mp4_path.with_name(f"{output_mp4_path.stem}_canvas.jpg")
        self.canvas_gen.create_canvas(
            story_title=story_title,
            output_path=canvas_path,
            channel_name=channel_name,
            source_image_path=source_image_path
        )

        # 2. Build Synchronized ASS Subtitles (Phone-Player Center Marquee + Channel + Subtitles)
        ass_path = output_mp4_path.with_name(f"{output_mp4_path.stem}_subtitles.ass")
        self.sub_builder.build_ass_subtitles(
            scene_tasks=scene_tasks,
            segment_durations=segment_durations,
            output_ass_path=ass_path,
            story_title=story_title,
            channel_name=channel_name,
            total_duration_s=duration_s,
            initial_offset_s=initial_offset_s,
            pause_between_s=pause_between_s
        )

        # 3. Clean Relative Subtitle Path for FFmpeg
        ass_filename = ass_path.name
        working_dir = ass_path.parent

        # 4. Construct Minimal Filter Graph:
        # Minimal Audio Wave (y=915, 900x40 line)
        # Progress Bar (y=1005, 1520px)
        filter_complex = (
            f"[1:a]showwaves=s=900x40:mode=line:colors=0x00e5ff@0.85:scale=sqrt,format=yuva420p[wave];"
            f"[0:v][wave]overlay=x=(W-w)/2:y=915:shortest=1[v1];"
            f"[v1]drawbox=x=200:y=1005:w=1520:h=4:color=white@0.20:t=fill,"
            f"drawbox=x=200:y=1005:w='min(1520, 1520*(t/{duration_s:.2f}))':h=4:color=0x00e5ff@0.95:t=fill,"
            f"subtitles={ass_filename}[v]"
        )

        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(canvas_path),
            "-i", str(master_audio_path),
            "-filter_complex", filter_complex,
            "-map", "[v]",
            "-map", "1:a",
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-tune", "stillimage",
            "-c:a", "aac",
            "-b:a", "192k",
            "-t", f"{duration_s:.2f}",
            "-pix_fmt", "yuv420p",
            str(output_mp4_path)
        ]

        print("  [VideoRenderer] Running Ultra-Fast FFmpeg encode...")
        res = subprocess.run(cmd, cwd=str(working_dir), capture_output=True, text=True, encoding="utf-8")
        if res.returncode != 0:
            print(f"  [VideoRenderer] FFmpeg error: {res.stderr[-1000:]}")
            raise RuntimeError(f"FFmpeg video render failed: {res.stderr[-500:]}")

        size_mb = output_mp4_path.stat().st_size / (1024 * 1024)
        print(f"  [VideoRenderer] Master 1080p MP4 Ready: {output_mp4_path.name} ({size_mb:.2f} MB)")

        if canvas_path.exists():
            try:
                canvas_path.unlink()
            except Exception:
                pass

        return output_mp4_path

    def _get_duration(self, audio_path: Path) -> float:
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(audio_path)
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        try:
            return float(res.stdout.strip())
        except Exception:
            return 30.0
