# -*- coding: utf-8 -*-
import re
import logging

import scrapy
import scrapy.responsetypes
from urllib import parse
from scrapy.http import Request
from All_in_spider.items import TianqihoubaoItem
from All_in_spider.utils.common import get_md5
'''
天气后报网站中，数据层次结构为 省，市，县三级城市结构，每个月的数据放一页中， 数据表格中的信息为每天的天气、温度和风向信息，
'''


class TianqihoubaoSpider(scrapy.Spider):
    name = 'tianqihoubao'
    allowed_domains = ['tianqihoubao.com']
    start_urls = ['http://www.tianqihoubao.com/lishi//']

    def parse(self, response):
        # 获取到省份和对应省份的url,并交给scrapy进行下载
        province_urls = response.xpath('//dt/a/@href').extract()
        for province_url in province_urls:
            next_level_url = parse.urljoin(response.url, province_url)
            yield Request(url=next_level_url,
                                 callback=self.regison_detail)

    def regison_detail(self, response):
        # 从省份点击到每个城市
        regison_urls = response.xpath('//dd/a/@href').extract()
        sheng_name = response.xpath('//*[@id="content"]/h1/text()').extract_first()
        region_name = re.findall(r'(.*?)历史天气预报查询', sheng_name)[0]
        print(region_name)
        for city_url in regison_urls:
            next_level_url = parse.urljoin(response.url, city_url)
            yield Request(url=next_level_url,
                          meta={"region_name": region_name},
                          callback=self.date_detail)



    def date_detail(self, response):
        # 从城市点击到对应城市的每个月中
        date_detail_urls = response.xpath('//div[@class="wdetail"]/div[@class="box pcity"]/ul/li/a/@href').extract()
        for date_detail_url in date_detail_urls:
            next_level_url = parse.urljoin(response.url, date_detail_url)
            yield Request(url=next_level_url,
                          meta={'region_name': response.meta['region_name']},
                          callback=self.parse_detail)


    def parse_detail(self, response):
        # 获取城市的当前月中的每天的数据信息

        tianqihoubao_item = TianqihoubaoItem()
        content_selectors = response.xpath('//*[@id="content"]/table/tr')
        item_city_name_tmp = response.xpath('//div[@class="wdetail"]/h1/text()').extract_first().replace('\r\n','').replace(' ','')
        item_city_name = re.findall('(.*?)历史天气预报.*?份', item_city_name_tmp)[0]
        item_city_pinyin_tmp = response.url
        item_city_pinyin = re.findall(r'http://www.tianqihoubao.com/lishi/(.*?)/month/.*?.html', item_city_pinyin_tmp)[0]
        item_regsion = response.meta['region_name']
        try:
            post_id = response.xpath('//*[@id="bd"]/div[2]/div[10]/div/text()[1]').extract()[0].replace('\r\n', '').replace(' ', '').split("：")[1]
        except:
            post_id = '0'
        for content_selector in range(2, len(content_selectors)):
            line_date_xpath = '//*[@id="content"]/table/tr[%d]/td[1]/a/text()' % content_selector
            line_weather_xpath = '//*[@id="content"]/table/tr[%d]/td[2]/text()' % content_selector
            line_temperature_xpath = '//*[@id="content"]/table/tr[%d]/td[3]/text()' % content_selector
            line_wind_xpath = '//*[@id="content"]/table/tr[%d]/td[4]/text()' % content_selector

            line_date = response.xpath(line_date_xpath).extract_first('9999年09月09日').replace('\r\n', '').replace(' ', '')
            item_date = line_date.replace('年', '-').replace('月', '-').replace('日', '')  # 数据处理
            line_weather = response.xpath(line_weather_xpath).extract()[0].replace('\r\n', '').replace(' ', '')
            item_weather_black = line_weather.replace('\r', '').split("/")[1]  # 数据处理
            item_weather_light = line_weather.replace('\r', '').split("/")[0]
            line_temperature = response.xpath(line_temperature_xpath).extract()[0].replace('\r\n', '').replace(' ', '')
            item_temperature_black = line_temperature.replace('\r', '').split("/")[1]  # 数据处理
            item_temperature_light = line_temperature.replace('\r', '').split("/")[0]  # 数据处理
            line_wind = response.xpath(line_wind_xpath).extract()[0].replace('\r\n', '').replace(' ', '')
            item_wind_black = line_wind.replace('\r', '').split("/")[1]
            item_wind_light = line_wind.replace('\r', '').split("/")[0]

            tianqihoubao_item["item_city_name"] = item_city_name
            tianqihoubao_item["item_city_pinyin"] = item_city_pinyin
            tianqihoubao_item["item_regsion"] = item_regsion
            tianqihoubao_item["post_id"] = post_id
            tianqihoubao_item["item_date"] = item_date
            tianqihoubao_item["item_weather_black"] = item_weather_black
            tianqihoubao_item["item_weather_light"] = item_weather_light
            tianqihoubao_item["item_temperature_black"] = item_temperature_black
            tianqihoubao_item["item_temperature_light"] = item_temperature_light
            tianqihoubao_item["item_wind_black"] = item_wind_black
            try:
                tianqihoubao_item["wind_light_direction"] = item_wind_black.split('风')[0]
            except:
                tianqihoubao_item["wind_light_direction"] = ""
            tianqihoubao_item["item_wind_light"] = item_wind_light
            try:
                tianqihoubao_item["wind_black_direction"] = item_wind_light.split('风')[0]
            except:
                tianqihoubao_item["wind_black_direction"] = item_wind_black.split('风')[0]

            tianqihoubao_item["item_uuid"] = get_md5(item_city_name+item_regsion+item_date)
            # print(tianqihoubao_item)


            yield tianqihoubao_item

        print(item_city_name_tmp)





