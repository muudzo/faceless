from src.apis.nasa_client import NASAClient
from src.apis.pexels_client import PexelsClient
from src.generators.script_gen import ScriptGenerator
from src.generators.edge_voice_gen import EdgeVoiceGenerator
from src.generators.shorts_generator import ShortsGenerator
from src.processor.thumbnail_gen import ThumbnailGenerator
from src.utils import setup_logger, PipelineError
import os
import datetime

logger = setup_logger()

from src.apis.research_client import ResearchClient
from src.uploader.seo_optimizer import SEOOptimizer

class VideoPipeline:
    def __init__(self):
        self.nasa = NASAClient()
        self.pexels = PexelsClient()
        self.script_gen = ScriptGenerator()
        self.voice_gen = EdgeVoiceGenerator()
        self.shorts_gen = ShortsGenerator()
        self.thumb_gen = ThumbnailGenerator()
        self.research = ResearchClient()
        self.seo = SEOOptimizer()

    async def fetch_data(self, date=None):
        logger.info("Step 1: Fetching NASA data and performing research...")
        data = await self.nasa.get_latest_image_fact(
            start_date=datetime.datetime.strptime(date, '%Y-%m-%d').date() if date else None
        )
        # Attempt to verify with Wikipedia for more context
        research = await self.research.search_and_verify(data.get("title"))
        if research:
            logger.info(f"Fact verified on Wikipedia: {research['url']}")
            data["research_summary"] = research["summary"]
        else:
            logger.warning("No Wikipedia verification found for this topic.")
            
        return data

    async def generate_content(self, title, explanation, research_context=None):
        logger.info("Step 2 & 4: Generating script and voiceover...")
        script = await self.script_gen.generate_short_script(title, explanation, research_context)
        # Voice generation is already async in EdgeVoiceGenerator.generate_voice (wait, checking...)
        # Actually it's a wrapper, I'll call it via thread if needed or make it truly async.
        # EdgeVoiceGenerator.generate_voice uses asyncio.run() - BAD for nested loops.
        # I'll update EdgeVoiceGenerator next.
        voice_path = self.voice_gen.generate_voice(script, "voiceover.mp3")
        return script, voice_path

    async def run(self, date=None, dry_run=False, session_id=None):
        from src.processor.storage_manager import StorageManager
        storage = StorageManager()
        session_dir = storage.get_session_dir(session_id)
        
        logger.info(f"Starting async pipeline (Session: {session_dir})")
        try:
            data = await self.fetch_data(date)
            title, explanation = data.get("title"), data.get("explanation")
            
            # Parallel Execution: Fetch Pexels + Generate Script + Download NASA Image
            import asyncio
            
            # Task 1: Generate Script and Voice
            script_task = self.generate_content(title, explanation, data.get("research_summary"))
            # Task 2: Download NASA Image
            image_task = self.nasa.download_image(data.get("url"), "nasa_daily.jpg", session_dir=session_dir)
            # Task 3: SEO Optimization
            seo_task = self.seo.optimize_metadata(title)
            
            # Batch await
            (script, voice_path), img_path, seo_data = await asyncio.gather(
                script_task, image_task, seo_task
            )
            
            if dry_run:
                preview_thumb = self.thumb_gen.generate_thumbnail(img_path, text=title.upper(), niche="Space")
                return {
                    "title": title, "description": script, "image": img_path, 
                    "audio": voice_path, "thumbnail": preview_thumb
                }

            logger.info("Step 5: Composing vertical video utilizing ShortsGenerator...")
            video_path = self.shorts_gen.create_short(
                image_path=img_path, audio_path=voice_path, 
                script=script, title=title, output_name="final_short.mp4"
            )
            
            logger.info("Step 6: Generating thumbnail...")
            thumb_path = self.thumb_gen.generate_thumbnail(video_path, text=title.upper())
            
            return {
                "video": video_path, "thumbnail": thumb_path,
                "title": seo_data["title"], "description": script, "tags": seo_data["tags"]
            }
        except Exception as e:
            logger.exception("Pipeline failed")
            raise PipelineError(str(e))

if __name__ == "__main__":
    pipeline = VideoPipeline()
    pipeline.run()
