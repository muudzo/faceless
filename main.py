import argparse
from src.runner import VideoPipeline
from src.utils import setup_logger

logger = setup_logger()

def main():
    parser = argparse.ArgumentParser(description="Cosmic Curiosities: YouTube Automation Pipeline")
    parser.add_argument("--date", type=str, help="Specific date for NASA APOD (YYYY-MM-DD)")
    parser.add_argument("--upload", action="store_true", help="Upload the generated video to YouTube")
    
    args = parser.parse_args()
    
    pipeline = VideoPipeline()
    try:
        results = pipeline.run(args.date)
        if results:
            print(f"Success! Video created at: {results['video']}")
            print(f"Thumbnail created at: {results['thumbnail']}")
            
            if args.upload:
                # This will be implemented in the next phase
                print("YouTube upload requested. (Component coming soon)")
        else:
            print("Pipeline finished with no output (likely due to media_type mismatch).")
            
    except Exception as e:
        print(f"Pipeline failed: {e}")

if __name__ == "__main__":
    main()
