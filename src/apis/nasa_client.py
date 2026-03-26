import os
from src.config import NASA_API_KEY, RAW_DATA_DIR
from src.apis.base_client import BaseAPIClient
from src.utils import retry

class NASAClient(BaseAPIClient):
    def __init__(self, api_key=NASA_API_KEY):
        super().__init__(base_url="https://api.nasa.gov/planetary/apod")
        self.api_key = api_key

    @retry(Exception, tries=3, delay=2) # Keep specific retry wrapper for non-HTTP errors if needed
    def get_daily_fact(self, date=None):
        """
        Fetches the Astronomy Picture of the Day for a given date.
        """
        params = {
            "api_key": self.api_key,
            "hd": "True"
        }
        if date:
            params["date"] = date

        # BaseAPIClient handles raise_for_status
        response = self.get(params=params)
        return response.json()

    def get_latest_image_fact(self, start_date=None, max_days=7):
        """
        Searches backwards from start_date for the most recent image APOD.
        """
        import datetime
        current_date = start_date or datetime.date.today()
        
        for _ in range(max_days):
            data = self.get_daily_fact(current_date.strftime("%Y-%m-%d"))
            if data.get("media_type") == "image":
                return data
            current_date -= datetime.timedelta(days=1)
        
        raise ValueError(f"No image APOD found in the last {max_days} days.")

    @retry(Exception, tries=3, delay=5)
    def download_image(self, url, filename):
        """
        Downloads the image from the given URL and saves it to the raw data directory.
        """
        save_path = RAW_DATA_DIR / filename
        response = self.session.get(url, stream=True)
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
