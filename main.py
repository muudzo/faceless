import argparse
import datetime
from src.runner import VideoPipeline
from src.utils import setup_logger

logger = setup_logger()

def validate_date(date_str):
    try:
        return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date format: '{date_str}'. Expected YYYY-MM-DD.")

import asyncio

async def main():
    parser = argparse.ArgumentParser(description="Cosmic Curiosities: YouTube Automation Pipeline")
    parser.add_argument("--date", type=validate_date, help="Specific date for NASA APOD (YYYY-MM-DD)")
    parser.add_argument("--upload", action="store_true", help="Upload the generated video to YouTube")
    parser.add_argument("--dry-run", action="store_true", help="Preview assets without rendering video")
    parser.add_argument("--session", type=str, help="Optional session ID for storage isolation")
    
    args = parser.parse_args()
    
    date_val = args.date.strftime('%Y-%m-%d') if args.date else None
    
    pipeline = VideoPipeline()
    try:
        results = await pipeline.run(date_val, dry_run=args.dry_run, session_id=args.session)
        if results:
            if args.dry_run:
                print(f"Dry Run successful!")
                print(f"Title: {results['title']}")
                print(f"Script: {results['description']}")
                print(f"Assets: {results['image']}, {results['audio']}")
            else:
                print(f"Success! Video created at: {results['video']}")
            
            if args.upload and not args.dry_run:
                from src.uploader.youtube_uploader import YouTubeUploader
                uploader = YouTubeUploader()
                vid_id = uploader.upload_video(
                    results['video'], 
                    results['title'], 
                    results['description']
                )
                print(f"Video uploaded successfully! ID: {vid_id}")
        else:
            print("Pipeline finished with no output.")
            
    except Exception as e:
        logger.error(f"Execution failed: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
