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


class Html5tracksItem(scrapy.Item):
    tital = scrapy.Field()
    url = scrapy.Field()
    desc = scrapy.Field()
    img_url = scrapy.Field()
    demo = scrapy.Field()
    download = scrapy.Field()
    date = scrapy.Field()


class MaoyanMovieInfoItem(scrapy.Item):
    """
    影片信息的item
    """
    date_type = scrapy.Field() # 区分不同数据源
    movie_id = scrapy.Field()
    name_cn = scrapy.Field()
    name_en = scrapy.Field()
    score = scrapy.Field()
    desc = scrapy.Field()
    type = scrapy.Field()
    country_make = scrapy.Field()
    timeline = scrapy.Field()
    release = scrapy.Field()
    director = scrapy.Field()
    performer = scrapy.Field()
    productions = scrapy.Field()
    production_makers = scrapy.Field()
    distributions = scrapy.Field()
    join_productions = scrapy.Field()
    join_production_makers = scrapy.Field()
    join_distributions = scrapy.Field()
    other_production_makers = scrapy.Field()
    other_productions = scrapy.Field()
    other_distributions = scrapy.Field()
    others = scrapy.Field()
    technology_parameter = scrapy.Field()


class MaoyanPersonInfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class MaoyanPersonRoleItem(scrapy.Item):
    date_type = scrapy.Field() # 区分不同数据源
    role_id = scrapy.Field()
    person_id = scrapy.Field()
    movie_name = scrapy.Field()
    movie_id = scrapy.Field()
    role = scrapy.Field()
    role_duty = scrapy.Field()


