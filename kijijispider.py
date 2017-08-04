import scrapy
import json
import re
from scrapy.selector import Selector
from scrapy.http import FormRequest
from datetime import datetime

class KijijiSpider(scrapy.Spider):
	name = 'KijijiSpider'
	start_urls = ['http://www.kijiji.ca/b-programmer-computer-jobs/british-columbia/c54l9007']

	def parse(self, response):
		for href in response.css('.description a::attr(href)'):
			site = href.extract()
			# Ignoring the indeed.com matches for now
			if site[:1] == '/':
				yield scrapy.Request(response.urljoin(site), callback=self.parse_job)
		# next page
		hxs = Selector(response)
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

