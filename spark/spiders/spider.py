import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import SparkItem
from itemloaders.processors import TakeFirst
pattern = r'(\xa0)?'

class SparkSpider(scrapy.Spider):
	name = 'spark'
	start_urls = ['https://www.sparkron.dk/om-sparekassen/nyheder']

	def parse(self, response):
		post_links = response.xpath('//div[@class="a-arrow-link__container"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//time/text()').get()
		title = response.xpath('//div[contains(@class,"frame__cell-item")]/h2/text()').get()
		if not title:
			title = response.xpath('//h2[@class="hero-module-b__title"]/text()').get()
		content = response.xpath('//div[@class="frame__cell-item"]//text()[not (ancestor::script)]').getall() + response.xpath('//div[contains(@class,"text-module-b__")]//text()[not (ancestor::script)]').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))


		item = ItemLoader(item=SparkItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
