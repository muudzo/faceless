from googleapiclient.http import MediaFileUpload
from src.uploader.youtube_auth import get_authenticated_service

class YouTubeUploader:
    def __init__(self, client_secrets_file='credentials.json'):
        self.youtube = get_authenticated_service(client_secrets_file)

    def upload_video(self, file_path, title, description, tags=None, category_id="27", privacy_status="private"):
        """
        Uploads a video to YouTube with metadata.
        """
        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags or ["space", "science", "nasa", "astronomy"],
                "categoryId": category_id
            },
            "status": {
                "privacyStatus": privacy_status,
                "selfDeclaredMadeForKids": False
            }
        }

        # Create media file upload object
        media = MediaFileUpload(file_path, chunksize=-1, resumable=True)

        # Execute upload
        request = self.youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media
        )
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"Uploaded {int(status.progress() * 100)}%")
        
        # YouTube Quota: A video upload costs approx 1600 units
        self.log_quota_usage(1600)
        
        return response.get("id")

    def log_quota_usage(self, units):
        """Simple quota logger."""
        import datetime
        with open("quota_usage.log", "a") as f:
            f.write(f"{datetime.datetime.now().isoformat()} - Used {units} units\n")

if __name__ == "__main__":
    print("YouTubeUploader initialized.")
