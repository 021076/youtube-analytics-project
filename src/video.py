import json
import os
from googleapiclient.discovery import build


class Video:
    """Класс для видео на ютуб"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str):
        self.video_id = video_id
        self.video = self.youtube.videos().list(id=self.video_id,
                                                part='snippet,statistics,contentDetails,topicDetails').execute()
        self.title = self.video["items"][0]["snippet"]["title"]
        self.url = f'https://www.youtube.com/watch?v={self.video_id}'
        self.viewCount = self.video["items"][0]["statistics"]["viewCount"]
        self.likeCount = self.video["items"][0]["statistics"]["likeCount"]

    def __str__(self):
        """Возвращает название видео"""
        # return f'{self.title}'
        return f'{json.dumps(self.video, indent=2, ensure_ascii=False)}'
        # вся информация по видео для анализа


class PLVideo(Video):
    """Дочерний класс плейлистов ютуба, наcлдеуется от класса Video"""

    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.channelId = self.video["items"][0]["snippet"]["channelId"]
        self.playlists = self.youtube.playlists().list(channelId=self.channelId,
                                                       part='contentDetails,snippet',
                                                       maxResults=50,
                                                       ).execute()
        self.playlist_id = playlist_id
        # вывод всех плейлистов, проверка наличия нужного
        # for playlist in self.playlists['items']:
        #     print(playlist)
        #     print()


class PlayList(PLVideo):
    pass
    """Дочерний класс плейлистов ютуба, наcледуется от класса Video"""

    def __init__(self, playlist_id: str, title_playlist: str, url_playlist: str, video_id: str):
        super().__init__(video_id, playlist_id)
        self.title_playlist = self.playlists["items"][0]["snippet"]["title"]
        self.url_playlist = f'https://www.youtube.com/playlist?list={self.playlist_id}'

    def total_duration(self):
        pass

    def show_best_video(self):
        pass
