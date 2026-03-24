# Cosmic Curiosities: Faceless YouTube Automation

This project automates the creation and uploading of short-form "Space Fact" videos to YouTube using free APIs.

## Features
- **Daily Content**: Fetches high-quality images and facts from NASA APOD.
- **Narrated Short**: Generates voiceover from facts using gTTS.
- **Cinematic Visuals**: Applies Ken Burns zoom effects and background music.
- **Dynamic Subtitles**: Automatically renders high-contrast text overlays.
- **One-Click Upload**: Integrated with YouTube Data API v3 for automated publishing.

## Setup

### 1. Prerequisites
- Python 3.12+
- FFmpeg (for MoviePy)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. API Keys
1.  **NASA APOD**: Get a key from [api.nasa.gov](https://api.nasa.gov/).
2.  **Pexels**: Get a key from [pexels.com/api](https://www.pexels.com/api/).
3.  **YouTube**:
    - Create a project in [Google Cloud Console](https://console.cloud.google.com/).
    - Enable YouTube Data API v3.
    - Create OAuth 2.0 Credentials and download `credentials.json`.
    - Place `credentials.json` in the project root.

### 4. Configuration
Rename `.env.example` to `.env` and fill in your keys.

## Usage

Run the full pipeline for today:
```bash
python main.py
```

Run for a specific date:
```bash
python main.py --date 2024-01-01
```

Upload to YouTube (requires `credentials.json`):
```bash
python main.py --upload
```

## Folder Structure
- `src/`: Core logic (APIs, generators, video engine, uploader).
- `data/`: Raw and processed assets.
- `assets/`: Music and fonts.
- `main.py`: CLI entry point.

## License
MIT
