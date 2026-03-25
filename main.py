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

def main():
    parser = argparse.ArgumentParser(description="Cosmic Curiosities: YouTube Automation Pipeline")
    parser.add_argument("--date", type=validate_date, help="Specific date for NASA APOD (YYYY-MM-DD)")
    parser.add_argument("--upload", action="store_true", help="Upload the generated video to YouTube")
    
    args = parser.parse_args()
    
    date_val = args.date.strftime('%Y-%m-%d') if args.date else None
    
    pipeline = VideoPipeline()
    try:
        results = pipeline.run(date_val)
        if results:
            print(f"Success! Video created at: {results['video']}")
            
            if args.upload:
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
