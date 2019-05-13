# -*- coding: utf-8 -*-
import scrapy


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['piaofang.maoyan.com']
    start_urls = ['https://piaofang.maoyan.com/movie/248172/']

    def parse(self, response):
        movie_tital = response.xpath('//p[@class="info-title"]/span/text()').extract_first('-')
        movie_id = response.url
        pass
