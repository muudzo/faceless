from src.apis.nasa_client import NASAClient
from src.apis.pexels_client import PexelsClient
from src.generators.script_gen import ScriptGenerator
from src.generators.voice_gen import VoiceGenerator
from src.processor.video_engine import VideoEngine
from src.processor.thumbnail_gen import ThumbnailGenerator
from src.utils import setup_logger, PipelineError
import os
import datetime

logger = setup_logger()

class VideoPipeline:
    def __init__(self):
        self.nasa = NASAClient()
        self.pexels = PexelsClient()
        self.script_gen = ScriptGenerator()
        self.voice_gen = VoiceGenerator()
        self.video_engine = VideoEngine()
        self.thumb_gen = ThumbnailGenerator()

    def run(self, date=None, dry_run=False):
        logger.info(f"Starting pipeline for date: {date or 'today'} (Dry Run: {dry_run})")
        
        try:
            # 1. Fetch NASA data using fallback logic
            data = self.nasa.get_latest_image_fact(
                start_date=datetime.datetime.strptime(date, '%Y-%m-%d').date() if date else None
            )
            title = data.get("title")
            explanation = data.get("explanation")
            logger.info(f"Fetched fact: {title}")
            
            # 2. Generate script
            script = self.script_gen.generate_short_script(title, explanation)
            logger.info(f"Generated script: {script}")
            
            # 3. Download image
            if data.get("media_type") != "image":
                logger.warning("Today's APOD is not an image (maybe a video). Skipping.")
                return None
            
            img_path = self.nasa.download_image(data.get("url"), "nasa_daily.jpg")
            logger.info(f"Downloaded NASA image: {img_path}")
            
            # 4. Generate voiceover
            voice_path = self.voice_gen.generate_voice(script, "voiceover.mp3")
            logger.info(f"Generated voiceover: {voice_path}")
            
            if dry_run:
                logger.info("Dry run enabled. Skipping video assembly and upload.")
                return {
                    "title": title,
                    "description": script,
                    "image": img_path,
                    "audio": voice_path
                }

            # 5. Assemble video
            video_path = self.video_engine.create_basic_video(img_path, voice_path, output_name="final_short.mp4")
            logger.info(f"Assembled video: {video_path}")
            
            # 6. Generate thumbnail
            thumb_path = self.thumb_gen.generate_thumbnail(video_path, text=title.upper())
            logger.info(f"Generated thumbnail: {thumb_path}")
            
            return {
                "video": video_path,
                "thumbnail": thumb_path,
                "title": title,
                "description": script
            }
            
        except Exception as e:
            logger.exception("Pipeline failed")
            raise PipelineError(str(e))

if __name__ == "__main__":
    pipeline = VideoPipeline()
    pipeline.run()
