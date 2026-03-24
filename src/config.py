import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
ASSETS_DIR = BASE_DIR / "assets"
MUSIC_DIR = ASSETS_DIR / "music"
FONTS_DIR = ASSETS_DIR / "fonts"

# API Keys
NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

# Video Settings
VIDEO_CONFIG = {
    "width": int(os.getenv("OUTPUT_WIDTH", 1080)),
    "height": int(os.getenv("OUTPUT_HEIGHT", 1920)),
    "fps": int(os.getenv("FPS", 30)),
}

# Ensure directories exist
for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, MUSIC_DIR, FONTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
