from moviepy.editor import VideoFileClip
from PIL import Image, ImageDraw, ImageFont
import os
from src.config import PROCESSED_DATA_DIR

class ThumbnailGenerator:
    def __init__(self, output_dir=PROCESSED_DATA_DIR):
        self.output_dir = output_dir

    def generate_thumbnail(self, video_path, text="SPACE FACT!", output_name="thumbnail.jpg"):
        """
        Generates a thumbnail by extracting a frame and adding text.
        """
        clip = VideoFileClip(video_path)
        # Get frame at 1 second mark (or middle)
        frame_time = min(1.0, clip.duration / 2)
        frame = clip.get_frame(frame_time)
        
        img = Image.fromarray(frame)
        draw = ImageDraw.Draw(img)
        
        # Add a catchy text overlay
        w, h = img.size
        try:
            # Use a large, bold font
            font = ImageFont.truetype("Arial Black", 120)
        except:
            font = ImageFont.load_default()
            
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        
        # Draw shadow/outline for readability
        draw.text(((w - tw) / 2 + 5, (h - th) / 4 + 5), text, font=font, fill="black")
        draw.text(((w - tw) / 2, (h - th) / 4), text, font=font, fill="yellow")
        
        output_path = self.output_dir / output_name
        img.save(str(output_path), "JPEG")
        clip.close()
        
        return str(output_path)

if __name__ == "__main__":
    print("ThumbnailGenerator initialized.")
    # In practice, this would be called after video generation
