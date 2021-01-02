import urllib.request
import json
import os
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from oauth2client.file import Storage
from google.oauth2.credentials import Credentials


from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage

api_key = "API_KEY"


def get_stats(channel_id, video_id):
    stats = {
        "subscribers": 0,
        "comments": 0,
        "likes": 0,
        "views": 0

    }
    with urllib.request.urlopen(
            f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={api_key}') as response:
        data = response.read()

        subs = json.loads(data)["items"][0]["statistics"]["subscriberCount"]

        stats["subscribers"] = subs

    with urllib.request.urlopen(
            f'https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={api_key}') as response:
        data = response.read()

        stats["comments"] = json.loads(data)["items"][0]["statistics"]["commentCount"]

        stats["likes"] = json.loads(data)["items"][0]["statistics"]["likeCount"]

        stats["views"] = json.loads(data)["items"][0]["statistics"]["viewCount"]

    return stats

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def update_title(video_id, title):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    CLIENT_SECRETS_FILE = "CLIENT_SECRETS_FILE.json"

    CREDENTIALS_PICKLE_FILE = "credentials_file"


    # Get credentials and create an API client

    def get_authenticated_service():
        if os.path.exists(CREDENTIALS_PICKLE_FILE):
            with open(CREDENTIALS_PICKLE_FILE, 'rb') as f:
                credentials = pickle.load(f)
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes)
            credentials = flow.run_console()
            with open(CREDENTIALS_PICKLE_FILE, 'wb') as f:
                pickle.dump(credentials, f)
        return googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)



    youtube = get_authenticated_service()

    request = youtube.videos().update(
        part="snippet,status,localizations",
        body={
            "id": video_id,
            "snippet": {
                    "title": title,
                    "categoryId": '22'

            }

        }
    )
    response = request.execute()

def delete_video(video_id):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    CLIENT_SECRETS_FILE = "CLIENT_SECRETS_FILE.json"

    CREDENTIALS_PICKLE_FILE = "credentials_file"


    # Get credentials and create an API client

    def get_authenticated_service():
        if os.path.exists(CREDENTIALS_PICKLE_FILE):
            with open(CREDENTIALS_PICKLE_FILE, 'rb') as f:
                credentials = pickle.load(f)
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes)
            credentials = flow.run_console()
            with open(CREDENTIALS_PICKLE_FILE, 'wb') as f:
                pickle.dump(credentials, f)
        return googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)



    youtube = get_authenticated_service()

    request = youtube.videos().delete(id=video_id)
    response = request.execute()

print(get_stats("UCjYr2rHyKLzjL5iJQTfrPhw", "gyuJiGmrW0k", ))



