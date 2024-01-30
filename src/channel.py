import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        self.__channel_id = channel_id
        self.channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.channel["items"][0]["snippet"]["title"]
        self.description = self.channel["items"][0]["snippet"]["description"]
        self.url = f'https://www.youtube.com/{self.__channel_id}'
        self.subscriberCount = self.channel["items"][0]["statistics"]["subscriberCount"]
        self.video_count = self.channel["items"][0]["statistics"]["videoCount"]
        self.viewCount = self.channel["items"][0]["statistics"]["viewCount"]

    def print_info(self) -> None:
        """Вывод информации о канале"""
        channal_data = json.dumps(self.__channel_id, indent=2, ensure_ascii=False)
        print(channal_data)

    @classmethod
    def get_service(cls) -> None:
        """ Возвращает объект для работы с YouTube API"""
        return cls.youtube

    @property
    def channel_id(self):
        """Устанавливает приватный режим для атрибута channel_id"""
        return self.__channel_id

    # @channel_id.setter
    # def channel_id(self, value):
    #     """используем, если нужно иметь возможность присваивать значение атрибуту channel_id, закомментировано чтобы показать,
    #     что без setter будет ошибка AttributeError: property 'channel_id' of 'Channel' object has no setter (см. main.py)"""
    #     self.__channel_id = value

    def to_json(self, file_json) -> None:
        """ Сохраняет в файл json значения атрибутов экземпляра `Channel` """
        attribute_data = {"channel_id": self.__channel_id, "title": self.title, "description": self.description,
                          "url": self.url, "subscriberCount": self.subscriberCount, "videoCount": self.video_count,
                          "viewCount": self.viewCount}
        with open(file_json, 'w', encoding='windows-1251') as file:
            json.dump(attribute_data, file, indent=2, ensure_ascii=False)

    def __str__(self):
        """Возвращает название и ссылку на канал по шаблону <название_канала> (<ссылка_на_канал>)"""
        return f'{self.__channel_id} ({self.url})'

    def __add__(self, other):
        """Метод для операции сложения"""
        return int(self.subscriberCount) + int(other.subscriberCount)

    def __sub__(self, other):
        """Метод для операции вычитания"""
        return int(self.subscriberCount) - int(other.subscriberCount)

    def __lt__(self, other):
        """Метод для операции сравнения меньше"""
        return int(self.subscriberCount) < int(other.subscriberCount)

    def __le__(self, other):
        """Метод для операции сравнения меньше или равно"""
        return int(self.subscriberCount) <= int(other.subscriberCount)

    def __gt__(self, other):
        """Метод для операции сравнения больше"""
        return int(self.subscriberCount) > int(other.subscriberCount)

    def __ge__(self, other):
        """Метод для операции сравнения больше или равно"""
        return int(self.subscriberCount) >= int(other.subscriberCount)

    def __eq__(self, other):
        """Метод для операции эквивалентности'"""
        return int(self.subscriberCount) == int(other.subscriberCount)