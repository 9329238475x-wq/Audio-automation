# -*- coding: utf-8 -*-
"""
Cinematic Canvas Generator:
- Clean Top Area: NO HEADLINE, NO background patti, NO ribbons, NO boxes.
- The thumbnail artwork stays fully visible and unblocked.
- Subtle lower vignette (bottom 42%) ensures dialogue subtitles, audio wave, and progress bar remain razor sharp.
"""

from pathlib import Path
from typing import Optional
from PIL import Image, ImageDraw

class CanvasGenerator:
    def __init__(self, width: int = 1920, height: int = 1080):
        self.width = width
        self.height = height

    def create_canvas(
        self,
        story_title: str,
        output_path: Path,
        channel_name: str = "DESI AUDIO STORIES",
        source_image_path: Optional[Path] = None
    ) -> Path:
        """
        Creates 1080p canvas with clean artwork on top and subtle lower vignette for dialogue captions.
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if source_image_path and Path(source_image_path).exists():
            try:
                base_img = Image.open(source_image_path).convert("RGB")
                img = self._crop_to_16_9(base_img)
            except Exception as e:
                print(f"  [CanvasGenerator] Note on source image: {e}. Generating default backdrop.")
                img = self._generate_default_gradient()
        else:
            img = self._generate_default_gradient()

        overlay = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        draw_ov = ImageDraw.Draw(overlay)

        # Lower 42% Dark Vignette for Subtitles & Audio Wave (Top is 100% CLEAN - NO PATTI)
        vignette_start = int(self.height * 0.58)
        for y in range(vignette_start, self.height):
            factor = (y - vignette_start) / float(self.height - vignette_start)
            alpha = int(235 * (factor ** 1.25))
            draw_ov.line([(0, y), (self.width, y)], fill=(6, 8, 14, alpha))

        img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
        img.save(str(output_path), quality=96)
        print(f"  [CanvasGenerator] Created Clean 1080p Canvas (Artwork preserved, zero patti) -> {output_path.name}")
        return output_path

    def _generate_default_gradient(self) -> Image.Image:
        img = Image.new("RGB", (self.width, self.height), (12, 16, 26))
        draw = ImageDraw.Draw(img)
        for y in range(self.height):
            alpha = y / float(self.height)
            r = int(14 + 8 * (1 - alpha))
            g = int(18 + 10 * (1 - alpha))
            b = int(32 + 16 * (1 - alpha))
            draw.line([(0, y), (self.width, y)], fill=(r, g, b))
        return img

    def _crop_to_16_9(self, img: Image.Image) -> Image.Image:
        target_w, target_h = self.width, self.height
        src_w, src_h = img.size
        scale = max(target_w / src_w, target_h / src_h)
        new_w = int(src_w * scale)
        new_h = int(src_h * scale)
        resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        left = (new_w - target_w) // 2
        top = (new_h - target_h) // 2
        return resized.crop((left, top, left + target_w, top + target_h))
