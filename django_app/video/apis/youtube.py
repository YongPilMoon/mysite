from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
from video.models import Video

DEVELOPER_KEY = "AIzaSyDiarbwPOxSkXmNPfdv8UtHcZM6KySpk34"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_search(keyword, page_token, max_results=10):

    youtube = build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY
    )

    search_response = youtube.search().list(
        q=keyword,
        part="id,snippet",
        maxResults=max_results,
        pageToken=page_token
    ).execute()

    return search_response


def youtube_video(video_id_list, search_response):
    youtube = build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY
    )
    video_response = youtube.videos().list(
        part="id,snippet,statistics,contentDetails",
        id=",".join(video_id_list)
    ).execute()

    video_response['nextPageToken'] = search_response.get('nextPageToken')
    video_response['prevPageToken'] = search_response.get('prevPageToken')
    video_response['pageInfo']['totalResults'] = search_response['pageInfo']['totalResults']

    return video_response
