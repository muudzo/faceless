from src.processor.video_engine import VideoEngine
from src.processor.footage_manager import FootageManager
from src.utils import setup_logger
from moviepy import CompositeVideoClip, VideoFileClip

logger = setup_logger()

class ShortsGenerator:
    """
    Orchestrates the creation of vertical YouTube Shorts.
    """
    def __init__(self):
        self.engine = VideoEngine()
        self.footage = FootageManager()

    def create_short(self, image_path, audio_path, script, title, output_name="short_v1.mp4"):
        """
        Creates a high-quality vertical short with b-roll and captions.
        """
        logger.info(f"Creating vertical short for: {title}")
        
        # 1. Generate base video with image and audio
        base_video_path = self.engine.create_basic_video(
            image_path, 
            audio_path, 
            output_name="temp_base.mp4"
        )
        base_clip = VideoFileClip(base_video_path)
        
        # 2. Get relevant b-roll
        videos = self.footage.get_relevant_footage(script)
        
        clips = [base_clip]
        
        # 3. Add b-roll overlays (simplified logic)
        for i, v_info in enumerate(videos[:1]): # For now just one overlay for simplicity
            try:
                # In a real scenario, we'd download the video here
                # For this commit, we're building the structure
                pass
            except Exception as e:
                logger.warning(f"Failed to add b-roll overlay: {e}")
                
        # 4. Add dynamic captions (using VideoEngine's helper)
        caption = self.engine.create_text_clip(title.upper(), base_clip.duration, fontsize=90)
        caption = caption.with_position(('center', 200)) # Top position
        clips.append(caption)
        
        final_video = CompositeVideoClip(clips)
        final_path = self.engine.PROCESSED_DATA_DIR / output_name
        
        final_video.write_videofile(
            str(final_path),
            fps=self.engine.config["fps"],
            codec="libx264",
            audio_codec="aac"
        )
        
        base_clip.close()
        return str(final_path)
