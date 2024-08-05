import json
import os
import isodate
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()


class Channel:
    """Класс для ютуб-канала"""
    youtube = build('youtube', 'v3', developerKey=os.getenv('YT_API_KEY'))

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title = self.channel["items"][0]["snippet"]['title']
        self.description = self.channel["items"][0]["snippet"]['description']
        self.url = self.channel["items"][0]["snippet"]["thumbnails"]["default"]["url"]
        self.video_count = self.channel["items"][0]["statistics"]["videoCount"]
        self.view_count = self.channel["items"][0]["statistics"]["viewCount"]
        self.subscriber_count = self.channel["items"][0]["statistics"]["subscriberCount"]

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        return cls.youtube

    def to_json(self, name_json_file: str) -> None:
        """Сохраняем в файл значения атрибутов экземпляра Channel"""
        parameters_of_instance = {}
        parameters_of_instance["id"] = self.__channel_id
        parameters_of_instance["title"] = self.title
        parameters_of_instance["description_chanel"] = self.description
        parameters_of_instance["url"] = self.url
        parameters_of_instance["subscriberCount_chanel"] = self.subscriber_count
        parameters_of_instance["video_count"] = self.video_count
        parameters_of_instance["view_count"] = self.view_count

        json_object = json.dumps(parameters_of_instance, indent=4, ensure_ascii=False)
        path_file_statistic = os.path.join(os.getcwd(), "../statistic/" + name_json_file)

        with open(path_file_statistic, "w") as f:
            f.write(json_object)

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        if isinstance(other, Channel):
            return int(self.subscriber_count) + int(other.subscriber_count)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if isinstance(other, Channel):
            return int(self.subscriber_count) - int(other.subscriber_count)

    def __rsub__(self, other):
        return self - other

    def __eq__(self, other):
        return int(self.subscriber_count) == int(other.subscriber_count)

    def __lt__(self, other):
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        return int(self.subscriber_count) <= int(other.subscriber_count)



