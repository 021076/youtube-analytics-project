import os
from googleapiclient.discovery import build


class Video:
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str):
        self.video_id = video_id
        self.video = self.youtube.videos().list(id=self.video_id,
                                                part='snippet,statistics,contentDetails,topicDetails').execute()
        self.title = self.video["items"][0]["snippet"]["title"]
        self.url = f'https://www.youtube.com/{self.video_id}'
        self.viewCount = self.video["items"][0]["statistics"]["viewCount"]
        self.likeCount = self.video["items"][0]["statistics"]["likeCount"]

    def __str__(self):
        """Возвращает название видео"""
        return f'{self.title}'
        # return f'{json.dumps(self.video, indent=2, ensure_ascii=False)}' -- вся информация по видео для анализа


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.channelId = self.video["items"][0]["snippet"]["channelId"]
        playlists = self.youtube.playlists().list(channelId=self.channelId,
                                                  part='contentDetails,snippet',
                                                  maxResults=50,
                                                  ).execute()
        self.playlist_id = playlist_id
        # вывод всех плейлистов, проверка наличия нужного
        # for playlist in playlists['items']:
        #     print(playlist)
        #     print()
