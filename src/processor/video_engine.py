from src.config import VIDEO_CONFIG, PROCESSED_DATA_DIR, FONTS_DIR
from src.processor.text_renderer import TextRenderer

class VideoEngine:
    def __init__(self, config=VIDEO_CONFIG):
        self.config = config
        self.text_renderer = TextRenderer()

    def create_text_clip(self, text, duration, fontsize=70, color="white", bgcolor=(0,0,0,128)):
        """
        Creates a text clip using the modular TextRenderer.
        """
        img_array = self.text_renderer.create_text_image(
            text, 
            self.config["width"], 
            200, 
            fontsize=fontsize, 
            color=color, 
            bgcolor=bgcolor
        )
        clip = ImageClip(img_array).set_duration(duration)
        return clip

    def zoom_in_effect(self, clip, zoom_ratio=0.04):
        """
        Applies a subtle zoom-in effect. Using a small zoom_ratio and 
        ensuring smooth interpolation.
        """
        return clip.resize(lambda t: 1 + zoom_ratio * t)

    def create_basic_video(self, image_path, audio_path, background_music_path=None, output_name="final_video.mp4", zoom=True, preset="medium"):
        """
        Creates a basic video with optimized ffmpeg presets.
        Presets: 'ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow'.
        """
        narration = AudioFileClip(audio_path)
        image = ImageClip(image_path).set_duration(narration.duration)
        
        # Resize image to fit screen (before zoom)
        w, h = self.config["width"], self.config["height"]
        image = image.resize(height=h) if image.w/image.h > w/h else image.resize(width=w)
        image = image.set_position("center")
        
        if zoom:
            image = self.zoom_in_effect(image)
        
        # Combine audio
        final_audio = narration
        if background_music_path and os.path.exists(background_music_path):
            bg_music = AudioFileClip(background_music_path).volumex(0.15)
            if bg_music.duration < narration.duration:
                from moviepy.audio.fx.all import audio_loop
                bg_music = audio_loop(bg_music, duration=narration.duration)
            else:
                bg_music = bg_music.subclip(0, narration.duration)
            
            from moviepy.audio.AudioClip import CompositeAudioClip
            final_audio = CompositeAudioClip([narration, bg_music])
            
        video = image.set_audio(final_audio)
        
        output_path = PROCESSED_DATA_DIR / output_name
        # Using optimized presets and threads for performance
        video.write_videofile(
            str(output_path), 
            fps=self.config["fps"], 
            codec="libx264", 
            audio_codec="aac",
            preset=preset,
            threads=4
        )
        
        return str(output_path)

if __name__ == "__main__":
    # Test would require actual files, so we'll just define the structure
    print("VideoEngine initialized. Ready for composition.")
