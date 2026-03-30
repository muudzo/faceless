import os
from src.config import PEXELS_API_KEY, RAW_DATA_DIR
from src.apis.base_client import BaseAPIClient

class PexelsClient(BaseAPIClient):
    def __init__(self, api_key=PEXELS_API_KEY):
        headers = {}
        if api_key:
            headers["Authorization"] = api_key
            
        super().__init__(base_url="https://api.pexels.com/videos/search", headers=headers)
        self.api_key = api_key

    async def search_videos(self, query, per_page=5):
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
        
        response = await self.get(params=params)
        return response.json()

    async def download_video(self, url, filename, session_dir=None):
        """
        Downloads the video asynchronously.
        """
        save_path = (Path(session_dir) if session_dir else RAW_DATA_DIR) / filename
        
        async with self.client.stream("GET", url) as response:
            response.raise_for_status()
            with open(save_path, "wb") as f:
                async for chunk in response.aiter_bytes():
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
