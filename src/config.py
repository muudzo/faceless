import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, Field, validator

# Load environment variables
load_dotenv()

class Settings(BaseModel):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = Field(default_factory=lambda: Path(__file__).resolve().parent.parent / "data")
    RAW_DATA_DIR: Path = Field(default_factory=lambda: Path(__file__).resolve().parent.parent / "data" / "raw")
    PROCESSED_DATA_DIR: Path = Field(default_factory=lambda: Path(__file__).resolve().parent.parent / "data" / "processed")
    ASSETS_DIR: Path = Field(default_factory=lambda: Path(__file__).resolve().parent.parent / "assets")
    MUSIC_DIR: Path = Field(default_factory=lambda: Path(__file__).resolve().parent.parent / "assets" / "music")
    FONTS_DIR: Path = Field(default_factory=lambda: Path(__file__).resolve().parent.parent / "assets" / "fonts")

    # API Keys
    NASA_API_KEY: str = os.getenv("NASA_API_KEY", "DEMO_KEY")
    PEXELS_API_KEY: str = os.getenv("PEXELS_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

    # Output Settings
    OUTPUT_WIDTH: int = int(os.getenv("OUTPUT_WIDTH", 1080))
    OUTPUT_HEIGHT: int = int(os.getenv("OUTPUT_HEIGHT", 1920))
    FPS: int = int(os.getenv("FPS", 30))

    class Config:
        arbitrary_types_allowed = True

settings = Settings()

# Export for compatibility
BASE_DIR = settings.BASE_DIR
DATA_DIR = settings.DATA_DIR
RAW_DATA_DIR = settings.RAW_DATA_DIR
PROCESSED_DATA_DIR = settings.PROCESSED_DATA_DIR
ASSETS_DIR = settings.ASSETS_DIR
MUSIC_DIR = settings.MUSIC_DIR
FONTS_DIR = settings.FONTS_DIR
NASA_API_KEY = settings.NASA_API_KEY
PEXELS_API_KEY = settings.PEXELS_API_KEY
GROQ_API_KEY = settings.GROQ_API_KEY

VIDEO_CONFIG = {
    "width": settings.OUTPUT_WIDTH,
    "height": settings.OUTPUT_HEIGHT,
    "fps": settings.FPS,
}

# Ensure directories exist
for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, MUSIC_DIR, FONTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
