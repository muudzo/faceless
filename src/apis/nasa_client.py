import requests
import os
from src.config import NASA_API_KEY, RAW_DATA_DIR
from src.utils import retry

class NASAClient:
    BASE_URL = "https://api.nasa.gov/planetary/apod"

    def __init__(self, api_key=NASA_API_KEY):
        self.api_key = api_key

    @retry(Exception, tries=3, delay=2)
    def get_daily_fact(self, date=None):
        """
        Fetches the Astronomy Picture of the Day for a given date.
        """
        params = {
            "api_key": self.api_key,
            "hd": True
        }
        if date:
            params["date"] = date

        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        return response.json()

    @retry(Exception, tries=3, delay=5)
    def download_image(self, url, filename):
        """
        Downloads the image from the given URL and saves it to the raw data directory.
        """
        save_path = RAW_DATA_DIR / filename
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return str(save_path)

if __name__ == "__main__":
    client = NASAClient()
    try:
        data = client.get_daily_fact()
        print(f"Title: {data.get('title')}")
        print(f"Explanation: {data.get('explanation')[:100]}...")
        if data.get('media_type') == 'image':
            path = client.download_image(data.get('url'), "daily_nasa.jpg")
            print(f"Image downloaded to: {path}")
    except Exception as e:
        print(f"Error: {e}")
