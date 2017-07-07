import scrapy
import re

class test1(scrapy.Spider):
	name = "test1"
	allowed_domains = ['jingcaiyuedu.com']
	start_urls = ["http://www.jingcaiyuedu.com/book/46702.html"]
	text_list = dict()  # all novel title and content
	unit_list = list()  # order of novel directory

	def parse(self, response):
		for a in response.xpath("//dl[@id='list']//a"):
			url = response.urljoin(a.xpath("@href").extract()[0])
			if re.search('第(.+)章', a.xpath("text()").extract()[0]):
				self.unit_list.append(a.xpath("text()").extract()[0])
				yield scrapy.Request(url, callback=self.parse_note)

	def parse_note(self, response):
		title = response.xpath("//div[@class='panel-heading']/text()").extract()[0]
		text = response.xpath("//div[@class='panel-body content-body content-ext']").extract()[0].replace('<br>', "\n").replace("&ubsp;", ' ')[160:-109]
		self.text_list[title] = text

	def closed(self, reason):
		# print("sum %d unit, start sorted..." % len(self.text_list.keys()))
		# print(self.text_list.keys())
		# sort_unit = sorted(self.text_list.keys(), key=lambda x:int(re.search('[0-9]+', x).group()))
		# print("finish sorted, start write into file...")
		with open("test.txt", 'w') as f:
			for unit in self.unit_list:
				f.write(unit+"\n")
				f.write(self.text_list[unit]+"\n\n")
		print("finish write")

	# 接收章节名，返回整形的章节数
	def unit_sorted(str):
		str = re.search("第(.+)章", str).group(1)  # cut unit numble
		if re.search('[\d]+', str):
			return int(re.search('[\d]+', str).group())
		else:
			d = dict(zip("零一二三四五六七八九十", "01234567890"))
			unit = [d[x] for x in str if x in d.keys()]
			


