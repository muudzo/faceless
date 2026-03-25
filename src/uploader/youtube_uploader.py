from googleapiclient.http import MediaFileUpload
from src.uploader.youtube_auth import get_authenticated_service

class YouTubeUploader:
    def __init__(self, client_secrets_file='credentials.json'):
        self.youtube = get_authenticated_service(client_secrets_file)

    def upload_video(self, file_path, title, description, tags=None, category_id="27", privacy_status="private"):
        """
        Uploads a video to YouTube with metadata and resumable tracking.
        """
        # Check if already uploaded
        import json
        state_file = "upload_state.json"
        if os.path.exists(state_file):
            with open(state_file, "r") as f:
                state = json.load(f)
                if state.get("file_path") == str(file_path) and state.get("status") == "success":
                    print(f"Video already uploaded: {state.get('video_id')}")
                    return state.get("video_id")

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

        media = MediaFileUpload(file_path, chunksize=1024*1024, resumable=True)
        request = self.youtube.videos().insert(part="snippet,status", body=body, media_body=media)
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"Uploaded {int(status.progress() * 100)}%")
        
        video_id = response.get("id")
        # Save success state
        with open(state_file, "w") as f:
            json.dump({"file_path": str(file_path), "video_id": video_id, "status": "success"}, f)
            
        self.log_quota_usage(1600)
        return video_id

    def log_quota_usage(self, units):
        """Simple quota logger."""
        import datetime
        with open("quota_usage.log", "a") as f:
            f.write(f"{datetime.datetime.now().isoformat()} - Used {units} units\n")

if __name__ == "__main__":
    print("YouTubeUploader initialized.")
