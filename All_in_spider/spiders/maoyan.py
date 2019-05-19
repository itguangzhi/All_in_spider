# -*- coding: utf-8 -*-
import re
import time
import math

import scrapy
from scrapy.http import Request
from urllib.request import urljoin
from scrapy import log
from All_in_spider.items import MaoyanMovieInfoItem, MaoyanPersonRoleItem


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['https://maoyan.com/films']
    start_urls = [
        'https://maoyan.com/films?showType=3&offset=0', ]

    start_urls = ['https://maoyan.com/films?showType=3&offset=%s' % str(id * 30) for id in range(0, 27918)]

    # 'https://maoyan.com/films?showType=1',
    # 'https://maoyan.com/films?showType=2',

    # def parse(self, response):
    #     log.msg(message="正常请求第一个页面URL" + response.url)
    #     page_nums = response.xpath('//ul[@class="list-pager"]/li[7]/a/text()').extract_first("-")
    #     for page_num in range(1, int(page_nums) + 1):
    #         next_page = 'https://maoyan.com/films?showType=3&offset=%s' % str(page_num * 30)
    #         Request(url=urljoin(response.url, next_page),
    #                 callback=self.parse_page,
    #                 dont_filter=True)

    # next_page = response.xpath('//ul[@class="list-pager"]/li[8]/a/@href').extract_first("-")

    def parse(self, response):
        log.msg(message="正常请求页面URL" + response.url + str(response.status))
        # # 拿到获取当前页的cookie
        cookies = response.request.headers.getlist('Cookie')
        # cookies1 = response.request.headers
        # # 拿到当前页面的电影列表
        movie_url_list = response.xpath('//div[@class="movie-item"]/a/@href').extract()
        movie_id_list = [re.findall('\d+', id)[0] for id in movie_url_list]
        for movie_url in movie_url_list:
            movie_id = re.findall('\d+', movie_url)[0]
            log.msg(message="开始请求影片ID：" + movie_id)
            piaofang_url = 'https://piaofang.maoyan.com/movie/%s?_v_=yes' % movie_id
            yield Request(url=urljoin(response.url, movie_url),
                          callback=self.film_parse,
                          cookies=cookies,
                          dont_filter=True)
            # 与这部电影相关人
            celebrity_url = 'https://piaofang.maoyan.com/movie/%s/celebritylist' % movie_id
            yield Request(url=celebrity_url,
                          callback=self.celebrity_roles,
                          cookies=cookies,
                          dont_filter=True)

        # yield Request(url=piaofang_url,
        #               callback=self.movie_parse,
        #               dont_filter=True
        #               )

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
        log.msg(message="开始解析影片ID：" + movie_id)
        name_cn = response.xpath('//h3[@class="name"]/text()').extract_first()
        log.msg(message="影片名：" + name_cn)
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
        try:
            release_date = release_date_nation[0:10]
        except:
            release_date = '1970-01-01'
        # release_native = release_date_nation[10:]
        desc = response.xpath('//span[@class="dra"]/text()').extract_first('-')


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


    def celebrity_roles(self, response):
        # TODO E480 [2019/5/17 21:23]  演员相关
        maoyanpersonrole = MaoyanPersonRoleItem()
        log.msg("已经解析到了影片ID：%s的影人相关的信息页面" % re.findall('\d+', response.url)[0])
        # 影人类别的名字：导演、演员、副导演、灯光……
        celebrity_type_name_list = response.xpath('//span[@class="title-name"]/text()').extract()
        celebrity_type_name_num_list_tmp = response.xpath('//em[@class="title-count"]/text()').extract()
        celebrity_type_name_num_list = [re.findall('\d+', t)[0] for t in celebrity_type_name_num_list_tmp]
        # 遍历所有的类别标签，拿到每个标签下：都有哪些人，这些人的ID
        for n, celebrity_type in enumerate(celebrity_type_name_list):
            person_url_list_xpath = '//*[@id="panelWrapper"]/dl[%s]/dd/div/div/a[@class="p-link"]/@href' % str(n+1)
            person_name_cn_list_xpath = '//*[@id="panelWrapper"]/dl[%s]/dd/div/div/a[@class="p-link"]/div[@class="p-desc"]/p[@class="p-item-name ellipsis-1"]/text()' % str(n+1)
            person_name_en_list_xpath = '//*[@id="panelWrapper"]/dl[%s]/dd/div/div/a[@class="p-link"]/div[@class="p-desc"]/p[@class="p-item-e-name ellipsis-1"]/text()' % str(n+1)
            person_role_list_xpath = '//*[@id="panelWrapper"]/dl[%s]/dd/div/div/a[@class="p-link"]/div[@class="p-desc"]/p[@class="p-item-play ellipsis-1"]/text()' % str(n+1)

            for celebrity in range(int(celebrity_type_name_num_list[n])):
                person_url = response.xpath(person_url_list_xpath).extract_first()
                person_name_cn = response.xpath(person_name_cn_list_xpath).extract_first()
                person_name_en = response.xpath(person_name_en_list_xpath).extract_first()
                try:
                    person_role = response.xpath(person_role_list_xpath).extract_first('0')
                except:
                    person_role = '-'

                maoyanpersonrole['person_id'] = int(re.findall('\d+', person_url)[0])
                maoyanpersonrole['movie_name'] = '-'
                maoyanpersonrole['movie_id'] = int(re.findall('\d+', response.url)[0])
                maoyanpersonrole['role'] = person_role
                maoyanpersonrole['role_duty'] = celebrity_type

                yield maoyanpersonrole

                yield Request(url=urljoin(response.url, person_url),
                              callback=self.celebrity_info,
                              dont_filter=True)


    @staticmethod
    def celebrity_info(response):
        pass