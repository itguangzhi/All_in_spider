# -*- coding: utf-8 -*-
import re
import time

import scrapy
from scrapy.http import Request
from urllib.request import urljoin
from scrapy import log
from All_in_spider.items import MaoyanMovieInfoItem


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['https://maoyan.com/films']
    start_urls = ['https://maoyan.com/films?showType=1',
                  'https://maoyan.com/films?showType=2',
                  'https://maoyan.com/films?showType=3', ]

    def parse(self, response):
        # 拿到获取当前页的cookie
        cookies = response.request.headers.getlist('Cookie')
        # 拿到当前页面的电影列表
        movie_url_list = response.xpath('//div[@class="movie-item"]/a/@href').extract()
        for movie_url in movie_url_list:
            movie_id = re.findall('\d+', movie_url)[0]
            log.msg(message="影片ID：" + movie_id)
            piaofang_url = 'https://piaofang.maoyan.com/movie/%s?_v_=yes' % movie_id
            yield Request(url=urljoin(response.url, movie_url),
                          callback=self.film_parse,
                          cookies=cookies,
                          dont_filter=True)
            time.sleep(2)

            # yield Request(url=piaofang_url,
            #               callback=self.movie_parse,
            #               dont_filter=True
            #               )

        # TODO E480 [2019/5/16 23:01] 寻找下一页
        next_page = response.xpath('//ul[@class="list-pager"]/li[4]/a/@href').extract_first("-")
        if next_page != '-':
            yield Request(url=urljoin(response.url, next_page),
                          callback=self.parse,
                          cookies=cookies,
                          dont_filter=True)
            log.msg(message="正常请求了下一页" + next_page)
        else:
            log.msg(message="已经是最后一页了")

    @staticmethod
    def movie_parse(response):
        movie_info_item = MaoyanMovieInfoItem()
        print(response.url)
        """
        这个是在猫眼票房中获取的影片信息
        :param response:
        :return:
        """
        # TODO E480 [2019/5/17 21:23]  影视公司相关

        # movie_info_item['director']
        # movie_info_item['performer']
        # movie_info_item['productions']
        # movie_info_item['production_makers']
        # movie_info_item['distributions']
        # movie_info_item['join_productions']
        # movie_info_item['join_production_makers']
        # movie_info_item['join_distributions']
        # movie_info_item['other_production_makers']
        # movie_info_item['other_productions']
        # movie_info_item['other_distributions']
        # movie_info_item['others']
        # movie_info_item['technology_parameter']

        return movie_info_item

    @staticmethod
    def film_parse(response):

        movie_info_item = MaoyanMovieInfoItem()
        """
        这个是在猫眼中请求获取的影片信息
        :param response:
        :return:
        """
        movie_id = re.findall(r'\d+', response.url)[0]
        name_cn = response.xpath('//h3[@class="name"]/text()').extract_first()
        name_en = response.xpath('//div[@class="ename ellipsis"]/text()').extract_first('-')
        type = response.xpath('//div[@class="movie-brief-container"]/ul/li[1]/text()').extract_first('-')
        score_tmp = response.xpath('//div[@class="star-on"]/@style').extract_first('-')
        try:
            score = str(int(re.findall(r"\d+", score_tmp)[0]) / 10)
        except:
            score = '-'
        # 地区和影片时长
        native_timeline = response.xpath('//div[@class="movie-brief-container"]/ul/li[2]/text()').extract_first()
        try:
            native = re.findall("(.*?)/(.*?)分钟", native_timeline.replace(" ", '').replace("\n", ""))[0][0]
            timeline = int(re.findall("(.*?)/(.*?)分钟", native_timeline.replace(" ", '').replace("\n", ""))[0][1])
        except:
            native = '-'
            timeline = 0
        release_date_nation = response.xpath('//div[@class="movie-brief-container"]/ul/li[3]/text()').extract_first()
        release_date = release_date_nation[0:10]
        release_native = release_date_nation[10:]
        desc = response.xpath('//span[@class="dra"]/text()').extract_first('-')

        celebrity_url = response.xpath('//div[@class="tab-desc tab-content active"]/div[2]/div[1]/a/@href').extract_first()
        yield Request(url=urljoin(response.url, celebrity_url))






        movie_info_item['movie_id'] = movie_id
        movie_info_item['name_cn'] = name_cn
        movie_info_item['name_en'] = name_en
        movie_info_item['score'] = score
        movie_info_item['desc'] = desc
        movie_info_item['type'] = type
        movie_info_item['country_make'] = native
        movie_info_item['timeline'] = int(timeline)
        movie_info_item['release'] = release_date

        yield movie_info_item

    @staticmethod
    def celebrity_info(response):
        # TODO E480 [2019/5/17 21:23]  演员相关
        celebrity_items = response.xpath(
            '//div[@class="celebrity-container"]/div[@class="celebrity-group"]/div[@class="celebrity-type"]/text()').extract()
        celebrity_item_num = response.xpath(
            '//div[@class="celebrity-container"]/div[@class="celebrity-group"]/div[@class="celebrity-type"]/span/text()').extract_first()
        celebrity_type = response.xpath(
            '//div[@class="tab-celebrity tab-content active"]/div/div[@class="celebrity-group"]/ul[@class="celebrity-list clearfix"]')
        for n, celebrity_item in enumerate(celebrity_items):
            item = celebrity_item.replace("\n", "").replace(" ", "")
            if item != '':
                celebrity_list_xpath = '//div[@class="tab-celebrity tab-content active"]/div/div[%s]/ul/li/a/@href' % str(
                    ((n - 1) / 2) + 1)
                celebrity_urls = response.xpath(celebrity_list_xpath).extract()
                for celebrit_url in celebrity_urls:
                    yield Request(url=urljoin(response.url, celebrit_url))
