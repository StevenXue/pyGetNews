#-*-coding=UTF-8-*-
from sgmllib import SGMLParser

class NewsParser(SGMLParser):
	"""
	继承SGMLParser
	提取出新闻的正文内容
	"""
	def __init__(self,site="163"):
		SGMLParser.__init__(self)
		self.site = site
	def reset(self):
		self.newsText = []
		self.flag = False
		self.getdata = False
		self.verbatim = 0
		SGMLParser.reset(self)
		
	def start_div(self,attrs):
		if self.flag == True:
				self.verbatim += 1
				return

		for k,v in attrs:
				if k == dirForDiv[self.site][0] and v == dirForDiv[self.site][1]:
						self.flag = True
						return
	
	def end_div(self):
		if self.verbatim == 0:
				self.flag = False
		if self.flag == True:
				self.verbatim -= 1
	
	def start_p(self,attrs):
		if self.flag == False:
				return
		self.getdata = True
	def end_p(self):
		if self.getdata:
				self.getdata = False
	def start_script(self,attrs):
		if self.getdata and self.site == "ZXW":
			self.getdata = False
	def handle_data(self,text):
		if self.getdata:
				self.newsText.append(text)