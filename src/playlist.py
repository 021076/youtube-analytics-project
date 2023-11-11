import os
import datetime
import isodate
from googleapiclient.discovery import build


class PlayList:
    """Класс для плейлиста на ютуб"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id: str):
        self.playlist_id = playlist_id
        self.title = self.youtube.playlists().list(id=playlist_id, part='snippet,contentDetails',
                                                   maxResults=50).execute().get('items')[0].get('snippet').get('title')
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'
        self.playlist = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                          part='contentDetails',
                                                          maxResults=50,
                                                          ).execute()
        self.video_ids = []
        for video in self.playlist['items']:
            self.video_ids.append(str(video['contentDetails']['videoId']))
        self.video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                         id=','.join(self.video_ids)).execute()

    @property
    def total_duration(self):
        """возвращает суммарную длительность плейлиста"""
        total_duration = 0
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += datetime.timedelta.total_seconds(duration)
        return datetime.timedelta(seconds=total_duration)

    def show_best_video(self):
        """возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""
        video_like = {}
        for video in self.video_response['items']:
            video_like[f"{video['id']}"] = int(video['statistics']['likeCount'])
        max_video_like = max(video_like.values())
        return f'https://youtu.be/{(list(video_like.keys())[list(video_like.values()).index(max_video_like)])}'
