from moviepy.editor import ImageClip, AudioFileClip, VideoFileClip, CompositeVideoClip
import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from src.config import VIDEO_CONFIG, PROCESSED_DATA_DIR, FONTS_DIR

class VideoEngine:
    def __init__(self, config=VIDEO_CONFIG):
        self.config = config

    def create_text_clip(self, text, duration, fontsize=70, color="white", bgcolor=(0,0,0,128)):
        """
        Creates a text clip using Pillow as a workaround for ImageMagick.
        """
        w, h = self.config["width"], 200 # Fixed height for subtitle bar
        img = Image.new("RGBA", (w, h), bgcolor)
        draw = ImageDraw.Draw(img)
        
        # Try to find a font, fallback to default
        try:
            font = ImageFont.truetype("Arial", fontsize)
        except:
            font = ImageFont.load_default()
            
        # Get text size and center it
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((w - tw) / 2, (h - th) / 2), text, font=font, fill=color)
        
        # Convert PIL image to numpy array for MoviePy
        img_array = np.array(img)
        clip = ImageClip(img_array).set_duration(duration)
        return clip

    def create_basic_video(self, image_path, audio_path, output_name="final_video.mp4"):
        """
        Creates a basic video by combining an image and an audio track.
        """
        audio = AudioFileClip(audio_path)
        image = ImageClip(image_path).set_duration(audio.duration)
        
        # Resize image to fit screen while maintaining aspect ratio or cropping
        # For shorts (1080x1920), we usually want to 'fill'
        w, h = self.config["width"], self.config["height"]
        image = image.resize(height=h) if image.w/image.h > w/h else image.resize(width=w)
        # Center crop
        image = image.set_position("center")
        
        video = image.set_audio(audio)
        
        output_path = PROCESSED_DATA_DIR / output_name
        video.write_videofile(str(output_path), fps=self.config["fps"], codec="libx264", audio_codec="aac")
        
        return str(output_path)

if __name__ == "__main__":
    # Test would require actual files, so we'll just define the structure
    print("VideoEngine initialized. Ready for composition.")
