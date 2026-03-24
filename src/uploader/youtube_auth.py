import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service(client_secret_file='credentials.json'):
    credentials = None
    # token.pickle stores the user's access and refresh tokens
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)
            
    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            if not os.path.exists(client_secret_file):
                raise FileNotFoundError(f"Missing {client_secret_file}. Please download it from Google Cloud Console.")
            
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
            credentials = flow.run_local_server(port=0)
            
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(credentials, token)

    return build("youtube", "v3", credentials=credentials)

if __name__ == "__main__":
    print("YouTube Authentication helper initialized.")
