# -*- coding: utf-8 -*-
import json
from urllib.parse import urlencode
import scrapy
from scrapy import Request, Spider
from images360.items import ImagesItem


class ImagesSpider(scrapy.Spider):
    name = 'images'
    allowed_domains = ['images.so.com']
    start_urls = ['http://images.so.com/']

    def start_requests(self):
        data = {
            'ch': 'beauty',
            'listtpye': 'new'
        }
        base_url = 'https://image.so.com/zj?'
        for page in range(1, self.settings.get("MAX_PAGE") + 1):
            data['sn'] = page * 30
            params = urlencode(data)
            url = base_url + params
            yield Request(url, self.parse)

    def parse(self, response):
        result = json.loads(response.text)
        for image in result.get('list'):
            item = ImagesItem()
            item['id'] = image.get('imageid')
            item['title'] = image.get('group_title')
            item['url'] = image.get('qhimg_url')
            item['thumb'] = image.get('qhimg_thumb_url')
            yield item
