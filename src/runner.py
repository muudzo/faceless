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

    def fetch_data(self, date=None):
        logger.info("Step 1: Fetching NASA data...")
        return self.nasa.get_latest_image_fact(
            start_date=datetime.datetime.strptime(date, '%Y-%m-%d').date() if date else None
        )

    def generate_content(self, title, explanation):
        logger.info("Step 2 & 4: Generating script and voiceover...")
        script = self.script_gen.generate_short_script(title, explanation)
        voice_path = self.voice_gen.generate_voice(script, "voiceover.mp3")
        return script, voice_path

    def run(self, date=None, dry_run=False):
        logger.info(f"Starting pipeline (Dry Run: {dry_run})")
        try:
            data = self.fetch_data(date)
            title, explanation = data.get("title"), data.get("explanation")
            
            script, voice_path = self.generate_content(title, explanation)
            img_path = self.nasa.download_image(data.get("url"), "nasa_daily.jpg")
            
            if dry_run:
                return {"title": title, "description": script, "image": img_path, "audio": voice_path}

            logger.info("Step 5: Composing video...")
            video_path = self.video_engine.create_basic_video(img_path, voice_path, output_name="final_short.mp4")
            
            logger.info("Step 6: Generating thumbnail...")
            thumb_path = self.thumb_gen.generate_thumbnail(video_path, text=title.upper())
            
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
