import os
from moviepy import ImageClip, AudioFileClip, VideoFileClip, CompositeVideoClip
from moviepy.audio.AudioClip import CompositeAudioClip
from moviepy.audio.tools.cuts import audio_loop
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
        return ImageClip(img_array).with_duration(duration)

    def advanced_ken_burns(self, clip, zoom_ratio=0.1, direction="random"):
        """
        Applies a multi-directional Ken Burns pan and zoom effect.
        Directions: 'center', 'left-to-right', 'right-to-left', 'top-to-bottom', 'bottom-to-top'.
        """
        import random
        if direction == "random":
            direction = random.choice(['center', 'left-to-right', 'right-to-left', 'top-to-bottom', 'bottom-to-top'])
            
        duration = clip.duration
        w, h = clip.size
        
        # Base zoom
        scaled_clip = clip.resized(lambda t: 1 + (zoom_ratio * t / duration))
        
        if direction == "left-to-right":
            return scaled_clip.with_position(lambda t: (int(-20 * t / duration), 'center'))
        elif direction == "right-to-left":
            return scaled_clip.with_position(lambda t: (int(20 * t / duration), 'center'))
        elif direction == "top-to-bottom":
            return scaled_clip.with_position(lambda t: ('center', int(-20 * t / duration)))
        elif direction == "bottom-to-top":
            return scaled_clip.with_position(lambda t: ('center', int(20 * t / duration)))
            
        return scaled_clip.with_position('center')

    def create_basic_video(self, image_path, audio_path, bg_music_paths=None, output_name="final_video.mp4", effects=True, preset="medium"):
        """
        Creates a video with advanced multi-track audio mixing and normalization.
        """
        narration = AudioFileClip(audio_path)
        image = ImageClip(image_path).set_duration(narration.duration)
        
        # Resize image
        w, h = self.config["width"], self.config["height"]
        image = image.resize(height=h) if image.w/image.h > w/h else image.resize(width=w)
        image = image.set_position("center")
        
        if zoom:
            image = self.zoom_in_effect(image)
        
        # Audio Mixing
        audio_tracks = [narration.volumex(1.2)] # Slightly boost narration
        
        if bg_music_paths:
            for i, bg_path in enumerate(bg_music_paths):
                if os.path.exists(bg_path):
                    bg_clip = AudioFileClip(bg_path).volumex(0.1 / (i+1)) # Lower volume for layered tracks
                    if bg_clip.duration < narration.duration:
                        bg_clip = audio_loop(bg_clip, duration=narration.duration)
                    else:
                        bg_clip = bg_clip.subclip(0, narration.duration)
                    audio_tracks.append(bg_clip)
        
        final_audio = CompositeAudioClip(audio_tracks)
        
        video = image.set_audio(final_audio)
        
        output_path = PROCESSED_DATA_DIR / output_name
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
