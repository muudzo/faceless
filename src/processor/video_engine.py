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
        Creates a video with native 9:16 support for YouTube Shorts.
        """
        narration = AudioFileClip(audio_path)
        image = ImageClip(image_path).with_duration(narration.duration)
        
        # 9:16 Vertical Framing Logic
        target_w, target_h = self.config["width"], self.config["height"]
        
        # Calculate scaling to fill the screen (crop if necessary)
        # This ensures we don't have black bars on the sides/top
        img_w, img_h = image.size
        scale = max(target_w / img_w, target_h / img_h)
        image = image.resized(scale)
        
        # Center the image in the vertical frame
        image = image.with_position("center")
        
        if effects:
            image = self.advanced_ken_burns(image)
        
        # Audio Mixing
        audio_tracks = [narration.volumex(1.2)]
        if bg_music_paths:
            for i, bg_path in enumerate(bg_music_paths):
                if os.path.exists(bg_path):
                    bg_clip = AudioFileClip(bg_path).volumex(0.1 / (i+1))
                    if bg_clip.duration < narration.duration:
                        bg_clip = audio_loop(bg_clip, duration=narration.duration)
                    else:
                        bg_clip = bg_clip.subclip(0, narration.duration)
                    audio_tracks.append(bg_clip)
        
        final_audio = CompositeAudioClip(audio_tracks)
        video = image.with_audio(final_audio)
        
        # Add background canvas to ensure size is exact
        bg_canvas = ColorClip(size=(target_w, target_h), color=(0,0,0)).with_duration(narration.duration)
        final_video = CompositeVideoClip([bg_canvas, video])
        
        output_path = PROCESSED_DATA_DIR / output_name
        final_video.write_videofile(
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
