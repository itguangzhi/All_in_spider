# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from All_in_spider.items import Html5tracksItem


class Html5tricksSpider(scrapy.Spider):
    name = 'html5tricks'
    allowed_domains = ['www.html5tricks.com/category/html5-demo']
    start_urls = ['http://www.html5tricks.com/category/html5-demo/']

    def parse(self, response):
        '''
        获取页面解析内容，并进行下一页的解析
        :param response: download请求的结果
        :return: 返回item的信息
        '''
        html5tracks_item = Html5tracksItme()

        tital = response.xpath('//header[@class="entry-header"]/h1/a/text()').extract()
        url = response.xpath('//header[@class="entry-header"]/h1/a/@href').extract()
        desc = response.xpath('//div[@class="entry-content"]/p[1]').extract()
        img_url = response.xpath('//div[@class="entry-content"]/p[2]/a/img/@src').extract()
        demo = response.xpath('//p[@class="tricksButtons"]/a[@class="demo"]/@href').extract()
        download = response.xpath('//p[@class="tricksButtons"]/a[@class="download"]/@href').extract()
        date = response.xpath('//header[@class="entry-header"]/div[3]/text()').extract()
        next_url = response.xpath('//a[@class="nextpostslink"]/@href').extract_first('-')
        if next_url != "-":
            yield Request(url=next_url, callback=self.parse)
        for n in range(0, len(tital)):
            html5tracks_item['tital'] = tital[n]
            html5tracks_item['url'] = url[n]
            html5tracks_item['desc'] = desc[n]
            html5tracks_item['img_url'] = img_url[n]
            html5tracks_item['demo'] = demo[n]
            html5tracks_item['download'] = download[n]
            html5tracks_item['date'] = date[n].replace('\r', '').replace('\n', '')
            print(html5tracks_item)
            yield html5tracks_item



