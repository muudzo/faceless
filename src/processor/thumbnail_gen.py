from moviepy.editor import VideoFileClip
from PIL import Image, ImageDraw, ImageFont
from src.config import PROCESSED_DATA_DIR
from src.processor.text_renderer import TextRenderer

from src.processor.niche_styler import NicheStyler

class ThumbnailGenerator:
    def __init__(self, output_dir=PROCESSED_DATA_DIR):
        self.output_dir = output_dir
        self.text_renderer = TextRenderer()
        self.styler = NicheStyler()

    def generate_thumbnail(self, video_path, text="SPACE FACT", output_name="thumbnail.jpg", niche="Space"):
        """
        Generates a high-CTR thumbnail with niche-specific styling.
        """
        style = self.styler.get_style(niche)
        
        clip = VideoFileClip(video_path)
        frame_time = min(1.0, clip.duration / 2)
        frame = clip.get_frame(frame_time)
        
        img = Image.fromarray(frame)
        draw = ImageDraw.Draw(img)
        w, h = img.size
        
        # Consistent professional styling
        fontsize = 120
        font_name = style.get("font", "Arial Black")
        try:
            font = ImageFont.truetype(font_name, fontsize)
        except:
            font = ImageFont.load_default()
            
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x, y = (w - tw) / 2, h * 0.2
        
        # Draw high-contrast outline for readability
        outline_color = "black"
        for offset in [(3,3), (-3,-3), (3,-3), (-3,3), (0,3), (3,0), (0,-3), (-3,0)]:
            draw.text((x+offset[0], y+offset[1]), text, font=font, fill=outline_color)
            
        text_color = style.get("text_color", "yellow")
        draw.text((x, y), text, font=font, fill=text_color)
        
        output_path = self.output_dir / output_name
        img.save(str(output_path), "JPEG", quality=95)
        clip.close()
        return str(output_path)

if __name__ == "__main__":
    print("ThumbnailGenerator initialized.")
    # In practice, this would be called after video generation
