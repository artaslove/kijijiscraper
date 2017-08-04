import scrapy
import re
from scrapy.selector import Selector

class KijijiSpider(scrapy.Spider):
	name = 'KijijiSpider'
	start_urls = ['http://www.kijiji.ca/b-programmer-computer-jobs/british-columbia/c54l9007']

	def parse(self, response):
		hxs = Selector(response)
		for href in hxs.xpath('//td[@class="description"]/a/@href').extract():
			# Ignoring links to other partner sites for sake of simplicity
			if href[:1] == '/':
				yield scrapy.Request(response.urljoin(href), callback=self.parse_job)
		next = hxs.xpath('//div[@class="pagination"]/a[@title="Next"]/@href').extract_first()
		if next is not None:
			yield scrapy.Request(response.urljoin(next), callback=self.parse)

	def parse_job(self, response):
		hxs = Selector(response)
		adid = re.sub('^.*/', '', response.url)
		adid = re.sub('\?.*$', '', adid)
		thedate = hxs.xpath('//time/@datetime').extract_first()
		address = hxs.xpath('//span[contains(@class,"address-")]/text()').extract_first()
		content = hxs.xpath('//div[contains(@class,"descriptionContainer-")]/div[1]').extract_first()
		title = hxs.xpath('//h1[contains(@class,"title-")]/text()').extract_first()
		link = response.url
		yield {
			'date': thedate,
			'address': address,
			'content': content,
			'link': link,
			'title': title,
			'adid': adid
		}

