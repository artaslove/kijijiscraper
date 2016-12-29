import scrapy
import json
import re
from scrapy.selector import Selector
from scrapy.http import FormRequest
from datetime import datetime

class KijijiSpider(scrapy.Spider):
	name = 'KijijiSpider'
	start_urls = ['http://www.kijiji.ca/b-programmer-computer-jobs/vancouver/c54l1700287',
		      'http://www.kijiji.ca/b-programmer-computer-jobs/nelson/c54l1700226',
		      'http://www.kijiji.ca/b-programmer-computer-jobs/victoria-bc/c54l1700173',
		      'http://www.kijiji.ca/b-programmer-computer-jobs/kelowna/c54l1700228',
		      'http://www.kijiji.ca/b-programmer-computer-jobs/cranbrook/c54l1700224',
		      'http://www.kijiji.ca/b-programmer-computer-jobs/kamloops/c54l1700227',
		      'http://www.kijiji.ca/b-programmer-computer-jobs/vernon/c54l1700229',
		      'http://www.kijiji.ca/b-programmer-computer-jobs/gta-greater-toronto-area/c54l1700272']
	# todo: add additional places

	def parse(self, response):
		for href in response.css('.description a::attr(href)'):
			full_url = response.urljoin(href.extract())
			request = scrapy.Request(full_url, callback=self.parse_job)
			yield request

	def parse_job(self, response):
		hxs = Selector(response)
		adid = re.sub('^.*/', '', response.url)
		request = FormRequest('http://www.kijiji.ca/j-vac-inc-get.json',formdata={'adId': adid},callback=self.parse_json,method='GET')
		tempdate = datetime.strptime(response.css('.ad-attributes td::text').extract()[0], '%d-%b-%y')
		request.meta['date'] = tempdate.strftime('%Y-%m-%d')
		request.meta['address'] = response.css('.ad-attributes td::text').extract()[1]
		request.meta['content'] = hxs.xpath('//div[@id="UserContent"]').extract()
		request.meta['title'] = hxs.xpath('/html/head/title/text()').extract()
		request.meta['link'] = response.url
		request.meta['adid'] = adid
		return request


	def parse_json(self, response):
		data = json.loads(response.body)
		yield {
			'date': response.meta['date'],
			'address': response.meta['address'],
			'content': response.meta['content'],
			'link': response.meta['link'],
			'title': response.meta['title'],
			'adid': response.meta['adid'],
			'visits': data['numVisits'],
		}

