import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.runner import VideoPipeline
from src.utils import setup_logger

logger = setup_logger("stress_test")

async def run_worker(worker_id, date=None):
    logger.info(f"Worker {worker_id} starting for date {date}...")
    pipeline = VideoPipeline()
    try:
        # Run in dry-run mode to save bandwidth/rendering while testing concurrency
        results = await pipeline.run(date=date, dry_run=True, session_id=f"stress_{worker_id}")
        logger.info(f"Worker {worker_id} finished: {results['title']}")
    except Exception as e:
        logger.error(f"Worker {worker_id} failed: {e}")

async def main():
    logger.info("Starting Scalability Stress Test (Parallel Jobs)...")
    
    # Simulate 3 parallel runs with different dates
    workers = [
        run_worker(1, "2024-03-20"),
        run_worker(2, "2024-03-19"),
        run_worker(3, "2024-03-18"),
    ]
    
    await asyncio.gather(*workers)
    logger.info("Stress test complete.")

if __name__ == "__main__":
    asyncio.run(main())
