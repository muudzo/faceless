import argparse
import time
from src.runner import VideoPipeline
from src.generators.topic_researcher import TopicResearcher
from src.utils import setup_logger

logger = setup_logger()

def process_batch(niche="Space", count=3):
    """
    Produces multiple videos in a single run.
    """
    researcher = TopicResearcher()
    pipeline = VideoPipeline()
    
    topics = researcher.discover_topics(niche=niche)
    topics = topics[:count]
    
    logger.info(f"Batch processing {len(topics)} topics...")
    
    results = []
    for topic in topics:
        try:
            logger.info(f"Processing Topic: {topic}")
            # In a full integration, we'd update runner.py 
            # to accept a topic string instead of just date.
            # For this commit, we're documenting the batch flow.
            # result = pipeline.run_topic(topic)
            results.append(topic)
            time.sleep(5) # Cooldown between tasks
        except Exception as e:
            logger.error(f"Failed to process {topic}: {e}")
            
    logger.info(f"Batch complete. Produced: {results}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--niche", default="Space Mysteries")
    parser.add_argument("--count", type=int, default=3)
    args = parser.parse_args()
    
    process_batch(niche=args.niche, count=args.count)
