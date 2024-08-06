import os
import pprint

from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()


class Video:
    """
    Класс для видео из ютуба
    """
    youtube = build('youtube', 'v3', developerKey=os.getenv('YT_API_KEY'))

    def __init__(self, video_id):
        self.video_id = video_id
        self.video_response = Video.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                    id=self.video_id).execute()
        self.video_title: str = self.video_response['items'][0]['snippet']['title']
        self.url: str = "https://youtu.be/" + self.video_id
        self.view_count: int = self.video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return f"{self.video_title}"

    def get_video(self):
        return self.video_response


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

