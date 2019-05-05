# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.http import Request


class SancunrenjianSpider(scrapy.Spider):
    name = 'sancunrenjian'
    allowed_domains = ['mingrenteahouse.com']
    start_urls = ['http://www.mingrenteahouse.com/shu/49149.html']

    def parse(self, response):
        book_tital = response.xpath('//div[@class="book-text"]/h1/text()').extract_first() # 书名
        book_actor = response.xpath('//div[@class="book-text"]/span/text()').extract_first(" ").split(" ")[0] # 作者
        book_intor = response.xpath('//div[@class="intro"]/text()').extract_first(" ") #简介
        book_id = response.url.split('/')[-1].split('.')[0]
        book_chapter_urls = response.xpath('//ul[2]/li/a/@href').extract() #章节url
        book_chapter_tital = response.xpath('//ul[2]/li/a/text()').extract() #章节名
        other_book_id = re.findall('javascript:go_page_from_id\(.*?,(.*?),.*?\)', book_chapter_urls[0])[0]
        for book_chapter_url in book_chapter_urls:
            book_chapter_id = re.findall('javascript:go_page_from_id\(.*?,.*?,(.*?)\)', book_chapter_url)[0]
            chapter_url = 'https://www.mingrenteahouse.com/files/article/html444/72/%s/%s.html' % (other_book_id, book_chapter_id)
            yield Request(url=chapter_url, callback=self.parse_detail)
            print(book_chapter_id)

    def parse_detail(self, response):

        pass



