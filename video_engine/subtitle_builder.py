# -*- coding: utf-8 -*-
"""
Dynamic ASS Subtitle Builder with:
1. Smartphone Music Player Style Scrolling Title (Centered Marquee inside [440..1480], no edge spill, seamless loop)
2. Channel Name centered below title (Pure white/silver with black shadow, NO patti)
3. Bottom Spoken Dialogue Captions (Bold white text, black shadow, actor badges)
"""

from pathlib import Path
from typing import List, Dict, Any
from PIL import Image, ImageDraw, ImageFont

CHARACTER_BADGE_COLORS = {
    "NARRATOR": "&H00E0E0&",       # Golden Champagne
    "HERO": "&H00D7FF&",           # Soft Warm Gold
    "HERO_ANGRY": "&H0055FF&",     # Fiery Orange
    "HEROINE": "&H8080FF&",        # Rosy Coral
    "HEROINE_BOLD": "&HB030FF&",   # Electric Pink
    "CHILD_FEMALE": "&HFFFF00&",   # Mint Cyan
    "CHILD_MALE": "&HFFCC00&",     # Sky Blue
    "MOTHER": "&HDDA0DD&",         # Tender Lavender
    "MOTHER_STRICT": "&H800080&",  # Deep Plum
    "FATHER": "&H3399FF&",         # Mellow Amber
    "FATHER_STRICT": "&H3333CC&",  # Crimson Maroon
    "COP_DOCTOR": "&HEEE000&",     # Slate Cyan
    "GRANDMOTHER": "&HAAB0EE&",    # Warm Rose
    "GRANDFATHER": "&HAACCAA&",    # Muted Sage
    "SISTER": "&H88CCFF&",         # Peach
    "BHABHI": "&H44BBFF&",         # Amber Glow
    "FRIEND_MALE": "&H88FF88&",    # Lime Mint
    "VILLAIN": "&H0000FF&",        # Blood Red
    "VAMP": "&H8800CC&",           # Ruby Magenta
    "SERVANT_MALE": "&HCCCCCC&"    # Soft Warm Silver
}

def format_ass_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int(round((seconds - int(seconds)) * 100))
    if cs >= 100:
        cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

class SubtitleBuilder:
    def __init__(self, font_name: str = "Nirmala UI", font_size: int = 42):
        self.font_name = font_name
        self.font_size = font_size

    def _measure_text_width(self, text: str) -> int:
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/Nirmala.ttc", self.font_size, index=0)
            dummy = Image.new("RGB", (100, 100))
            draw = ImageDraw.Draw(dummy)
            bbox = draw.textbbox((0, 0), text, font=font)
            return max(300, bbox[2] - bbox[0])
        except Exception:
            return max(300, len(text) * 22)

    def build_ass_subtitles(
        self,
        scene_tasks: List[Dict[str, Any]],
        segment_durations: List[float],
        output_ass_path: Path,
        story_title: str = "Audio Story",
        channel_name: str = "DESI AUDIO STORIES",
        total_duration_s: float = 30.0,
        initial_offset_s: float = 0.5,
        pause_between_s: float = 0.40
    ) -> Path:
        output_ass_path = Path(output_ass_path)
        output_ass_path.parent.mkdir(parents=True, exist_ok=True)

        ass_header = f"""[Script Info]
Title: Smartphone Music Player Audio Drama Captions
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: TitlePlayer,{self.font_name},{self.font_size},&H00FFFFFF,&H000000FF,&H00000000,&H90000000,1,0,0,0,100,100,0,0,1,3.5,2.5,7,0,0,0,1
Style: ChannelName,{self.font_name},24,&H00E6E6E6,&H000000FF,&H00000000,&H90000000,1,0,0,0,100,100,0,0,1,2.5,2.0,8,0,0,140,1
Style: DialogueStyle,{self.font_name},{self.font_size},&H00FFFFFF,&H000000FF,&H00000000,&H90000000,1,0,0,0,100,100,0,0,1,3.8,2.2,2,140,140,210,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        events = []

        # 1. Smartphone Music Player Marquee Title:
        # - Strictly clipped inside center window [440..1480] (width 1040px, never touches outer screen ends)
        # - Pure White Bold Hindi text with Deep Black Shadow
        # - Smooth reading speed (~68 px/s), seamlessly loops from start (t=0) to finish (total_duration_s)
        clean_title = story_title.strip()
        sep = "    •    "
        unit = f"{clean_title}{sep}"
        unit_w = self._measure_text_width(unit)
        full_marquee_text = unit * 4

        x_clip1, y_clip1, x_clip2, y_clip2 = 440, 15, 1480, 125
        cycle_dur = max(6.0, round(unit_w / 68.0, 2))
        x_start = 500
        x_end = x_start - unit_w

        num_cycles = max(1, int(total_duration_s // cycle_dur) + 2)
        for c in range(num_cycles):
            t_start = c * cycle_dur
            t_end = min(total_duration_s, (c + 1) * cycle_dur)
            if t_start >= total_duration_s:
                break
            st_str = format_ass_time(t_start)
            en_str = format_ass_time(t_end)
            events.append(
                f"Dialogue: 1,{st_str},{en_str},TitlePlayer,,0,0,0,,{{\\q2\\clip({x_clip1},{y_clip1},{x_clip2},{y_clip2})\\move({x_start},68,{x_end},68)}}{full_marquee_text}"
            )

        # 2. Channel Name Branding (Centered cleanly at y=140, White/Silver with Black Shadow, ZERO PATTI)
        clean_channel = channel_name.strip().upper()
        total_time_str = format_ass_time(total_duration_s)
        events.append(
            f"Dialogue: 1,0:00:00.00,{total_time_str},ChannelName,,0,0,0,,{clean_channel}"
        )

        # 3. Bottom Spoken Dialogue Captions (White text, black outline + actor badge)
        current_time = initial_offset_s
        for idx, (task, dur) in enumerate(zip(scene_tasks, segment_durations)):
            char = task.get("character", "NARRATOR").upper()
            role_name = task.get("role_name", char)
            display_name = char
            if "(" in role_name:
                display_name = role_name.split("(")[0].strip()
            elif "/" in role_name:
                display_name = role_name.split("/")[0].strip()

            raw_text = task.get("text", "").strip()
            if not raw_text:
                current_time += dur + pause_between_s
                continue

            start_t = current_time
            end_t = current_time + dur

            start_str = format_ass_time(start_t)
            end_str = format_ass_time(end_t)
            badge_color = CHARACTER_BADGE_COLORS.get(char, "&H00D7FF&")

            styled_text = f"{{\\b1\\c{badge_color}}}[{display_name}]:{{\\b0\\c&HFFFFFF&}} {raw_text}"
            events.append(f"Dialogue: 0,{start_str},{end_str},DialogueStyle,,0,0,0,,{styled_text}")
            current_time = end_t + pause_between_s

        full_content = ass_header + "\n".join(events) + "\n"
        with open(output_ass_path, "w", encoding="utf-8") as f:
            f.write(full_content)

        print(f"  [SubtitleBuilder] Generated {len(events)} ASS cues (Phone Marquee + Channel + Subtitles) -> {output_ass_path.name}")
        return output_ass_path
