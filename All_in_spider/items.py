# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AllInSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class TianqihoubaoItem(scrapy.Item):
    # 定义天气后报中的数据字段
    item_city_name = scrapy.Field()
    item_city_pinyin = scrapy.Field()
    post_id = scrapy.Field()
    item_date = scrapy.Field()
    item_weather_black = scrapy.Field()
    item_weather_light = scrapy.Field()
    item_temperature_black = scrapy.Field()
    item_temperature_light = scrapy.Field()
    item_wind_black = scrapy.Field()
    item_wind_light = scrapy.Field()
    item_regsion = scrapy.Field()
    item_uuid = scrapy.Field()
    wind_light_direction = scrapy.Field()
    wind_black_direction = scrapy.Field()


class Html5tracksItme(scrapy.Item):
    tital = scrapy.Field()
    url = scrapy.Field()
    desc = scrapy.Field()
    img_url = scrapy.Field()
    demo = scrapy.Field()
    download = scrapy.Field()
    date = scrapy.Field()

