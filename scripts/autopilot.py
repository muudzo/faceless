import time
import schedule
import datetime
from src.runner import VideoPipeline
from src.utils import setup_logger

logger = setup_logger()

def run_job():
    """
    Executes a single pipeline run.
    """
    logger.info(f"--- Autopilot Run Started: {datetime.datetime.now()} ---")
    pipeline = VideoPipeline()
    try:
        # Generate video for today
        result = pipeline.run()
        if result:
            logger.info(f"Successfully produced video: {result['title']}")
            # In a real scenario, we'd trigger the uploader here 
            # if we wanted full E2E automation in the daemon.
    except Exception as e:
        logger.error(f"Autopilot job failed: {e}")
    logger.info("--- Autopilot Run Finished ---")

def main():
    logger.info("Autopilot daemon started. Interval: Every 8 hours.")
    
    # Schedule the job
    schedule.every(8).hours.do(run_job)
    
    # Run once immediately for verification
    run_job()
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
