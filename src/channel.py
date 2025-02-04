import json
import os
from googleapiclient.discovery import build

class Channel:
	"""Класс для ютуб-канала"""
	api_key: str = os.getenv('YT_API_KEY')
	youtube = build('youtube', 'v3', developerKey=api_key)
	
	def __init__(self, channel_id: str) -> None:
		self.channel_id = channel_id

	def print_info(self) -> None:
		"""Вывож информации о канале"""
		channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
		print(json.dumps(channel, indent=2, ensure_ascii=False))
