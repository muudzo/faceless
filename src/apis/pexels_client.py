import requests
import os
from src.config import PEXELS_API_KEY, RAW_DATA_DIR

class PexelsClient:
    BASE_URL = "https://api.pexels.com/videos/search"

    def __init__(self, api_key=PEXELS_API_KEY):
        self.api_key = api_key
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({"Authorization": self.api_key})

    def search_videos(self, query, per_page=5):
        """
        Searches for videos on Pexels based on the query.
        """
        if not self.api_key:
            raise ValueError("PEXELS_API_KEY is not set.")

        params = {
            "query": query,
            "per_page": per_page,
            "orientation": "landscape"
        }
        
        response = self.session.get(self.BASE_URL, params=params)
        response.raise_for_status()
        return response.json()

    def download_video(self, url, filename):
        """
        Downloads the video from the given URL.
        """
        save_path = RAW_DATA_DIR / filename
        response = self.session.get(url, stream=True)
        response.raise_for_status()
        
        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return str(save_path)

if __name__ == "__main__":
    client = PexelsClient()
    try:
        # Search for space videos
        data = client.search_videos("galaxy")
        videos = data.get('videos', [])
        if videos:
            first_video = videos[0]
            # Get the link for a reasonably sized video unit
            video_files = first_video.get('video_files', [])
            # Filter for SD or HD, not 4K to save bandwidth
            target_file = next((f for f in video_files if f.get('quality') == 'hd'), video_files[0])
            path = client.download_video(target_file.get('link'), "pexels_space.mp4")
            print(f"Video downloaded to: {path}")
    except Exception as e:
        print(f"Error: {e}")
