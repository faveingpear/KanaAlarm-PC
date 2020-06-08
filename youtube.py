import webbrowser
import requests
from bs4 import BeautifulSoup

class Channel():

	def __init__(self,name=None,id=None,pfp=None,streamingStatus=False,streamThumbnail=None):
		self.name = name
		self.id = id
		self.pfp = pfp
		self.streamingStatus = streamingStatus
		self.streamThumbnail = streamThumbnail

		self.old_video_id_list = []

	def check_live(self):
		#if sort == self.branch:
		buff_video_id_set = self.get_live_video_id(self.id)
		#print("buff_video_id_set", buff_video_id_set)
		#print("self.old_video_id_list", self.old_video_id_list)
		if buff_video_id_set:
			for getting_video_id in buff_video_id_set:
				if not getting_video_id == "" and not getting_video_id is None:
					if not getting_video_id in self.old_video_id_list:
						self.old_video_id_list.append(getting_video_id)
						if len(self.old_video_id_list) > 30:
							self.old_video_id_list = self.old_video_id_list[1:]

						self.streamingStatus = True
						print(self.name + " is online: " + str(self.streamingStatus))
						return
		else:
			self.streamingStatus = False
			print(self.name + " is offline")
			
			
	def get_live_video_id(self, search_ch_id):
		dict_str = ""
		video_id_set = set()
		try:
			session = requests.Session()
			headers = {
				'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
			html = session.get("https://www.youtube.com/channel/" +
							   search_ch_id, headers=headers, timeout=10)
			soup = BeautifulSoup(html.text, 'html.parser')
			keyword = 'window["ytInitialData"]'
			for scrp in soup.find_all("script"):
				if keyword in str(scrp):
					dict_str = str(scrp).split(' = ', 1)[1]
			dict_str = dict_str.replace('false', 'False')
			dict_str = dict_str.replace('true', 'True')

			index = dict_str.find("\n")
			dict_str = dict_str[:index-1]
			dics = eval(dict_str)
			for section in dics.get("contents", {}).get("twoColumnBrowseResultsRenderer", {}).get("tabs", {})[0].get("tabRenderer", {}).get("content", {}).get("sectionListRenderer", {}).get("contents", {}):
				for itemsection in section.get("itemSectionRenderer", {}).get("contents", {}):
					items = {}
					if "shelfRenderer" in itemsection:
						for items in itemsection.get("shelfRenderer", {}).get("content", {}).values():
							for item in items.get("items", {}):
								for videoRenderer in item.values():
									for badge in videoRenderer.get("badges", {}):
										if badge.get("metadataBadgeRenderer", {}).get("style", {}) == "BADGE_STYLE_TYPE_LIVE_NOW":
											video_id_set.add(
												videoRenderer.get("videoId", ""))
					elif "channelFeaturedContentRenderer" in itemsection:
						for item in itemsection.get("channelFeaturedContentRenderer", {}).get("items", {}):
							for badge in item.get("videoRenderer", {}).get("badges", {}):
								if badge.get("metadataBadgeRenderer", {}).get("style", "") == "BADGE_STYLE_TYPE_LIVE_NOW":
									video_id_set.add(
										item.get("videoRenderer", {}).get("videoId", ""))
		except:
			return video_id_set
			
		self.videoid = video_id_set
		return video_id_set