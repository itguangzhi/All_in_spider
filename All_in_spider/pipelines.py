# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import logging

import pymysql
import pymysql.cursors
from scrapy import log
from twisted.enterprise import adbapi


class AllInSpiderPipeline(object):
    def process_item(self, item, spider):
        # print(item)
        return item


class JsonWithEncodingPipeline(object):
    # 自定义json文件的导出
    def __init__(self):
        self.file = codecs.open("tianqihoubao.json", "w", "utf-8")

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()


class JsonExporterPipeline(object):
    # 使用scrapy提供的json exporter导入json文件
    def __init__(self):
        self.file = open('tianqihoubao2.json', 'wb')
        from scrapy.exporters import JsonItemExporter
        self.export = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)

    def process_item(self, item, spider):
        self.export.export_item(item)
        return item

    def spider_closed(self, spider):
        self.export.finish_exporting()
        self.file.close()


class MysqlPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='spider', passwd='spider', db='spiderinc')
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            replace into wheather_info (uuid,
                                        city_id,
                                        regsion_name,
                                        city_name,
                                        city_pinyin,
                                        date,
                                        wheate_light,
                                        wheate_black,
                                        termperature_light,
                                        termperature_black,
                                        wind_light_direction,
                                        wind_black_direction,
                                        wind_light_level,
                                        wind_black_level) values (
                                       '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'
            )
        """ % (item["item_uuid"]
                                    , item["post_id"]
                                    , item["item_regsion"]
                                    , item["item_city_name"]
                                    , item["item_city_pinyin"]
                                    , item["item_date"]
                                    , item["item_weather_light"]
                                    , item["item_weather_black"]
                                    , item["item_temperature_light"]
                                    , item["item_temperature_black"]
                                    , item["wind_light_direction"]
                                    , item["wind_black_direction"]
                                    , item["item_wind_light"]
                                    , item["item_wind_black"])

        self.cur.execute(insert_sql)
        self.conn.commit()

        return item


class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            db=settings["MYSQL_DB"],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将数据插入变成异步执行的内容
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)

        # return item

    def handle_error(self, failure):
        # dbpool异常处理
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql = """
                    replace into wheather_info (uuid,
                                                city_id,
                                                regsion_name,
                                                city_name,
                                                city_pinyin,
                                                date,
                                                wheate_light,
                                                wheate_black,
                                                termperature_light,
                                                termperature_black,
                                                wind_light_direction,
                                                wind_black_direction,
                                                wind_light_level,
                                                wind_black_level) values (
                                               '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'
                    )
                """ % (item["item_uuid"]
                                            , item["post_id"]
                                            , item["item_regsion"]
                                            , item["item_city_name"]
                                            , item["item_city_pinyin"]
                                            , item["item_date"]
                                            , item["item_weather_light"]
                                            , item["item_weather_black"]
                                            , item["item_temperature_light"]
                                            , item["item_temperature_black"]
                                            , item["wind_light_direction"]
                                            , item["wind_black_direction"]
                                            , item["item_wind_light"]
                                            , item["item_wind_black"])

        cursor.execute(insert_sql)


class TianqihoubaoPipeline(object):
    def process_item(self, item, spider):
        return item


class MaoyanMysqlPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            db=settings["MYSQL_DB"],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将数据插入变成异步执行的内容
        if item['date_type'] == 'movie':
            query = self.dbpool.runInteraction(self.person_role_insert, item)
        elif item['date_type'] == 'roles':
            query = self.dbpool.runInteraction(self.person_role_insert, item)
        else:
            log.msg("数据格式不正确！")
            print(item)
        query.addErrback(self.handle_error, item)

        return item

    def handle_error(self, failure, item):
        # dbpool异常处理
        print(failure)
        # print("movieID:", item["movie_id"])
        # print(item)
# 影片数据入库的sql
    def film_insert(self, cursor, item):
        insert_sql = """
                            replace into maoyan_movie_info (movie_id,
                                                        name_cn,
                                                        name_en,
                                                        score,
                                                        `desc`,
                                                        `type`,
                                                        country_make,
                                                        timeline,
                                                        `release`) values (
                                                       '%s','%s','%s','%s','%s','%s','%s','%s','%s'
                            )
                        """ % (item["movie_id"]
                                                    , item["name_cn"]
                                                    , item["name_en"]
                                                    , item["score"]
                                                    , item["desc"]
                                                    , item["type"]
                                                    , item["country_make"]
                                                    , item["timeline"]
                                                    , item["release"]
                               )

        cursor.execute(insert_sql)
        log.msg(item["name_cn"] + "----入库成功")
# 影人角色入库的sql
    def person_role_insert(self, cursor, item):
        logging.debug("-----------演员角色入库信息---------")
        logging.debug(item)
        insert_sql = """
                            replace into maoyan_person_roles (person_id,
                                                            movie_name,
                                                            roles_id,
                                                            movie_id,
                                                            `role`,
                                                            role_duty) values (
                                                       '%d','%s','%s','%d','%s','%s'
                            )
                        """ % (item["person_id"]
                                                    , item["movie_name"]
                                                    , item["role_id"]
                                                    , item["movie_id"]
                                                    , item["role"]
                                                    , item["role_duty"]
                               )

        cursor.execute(insert_sql)
        log.msg(str(item["movie_id"])+" "+str(item['person_id'])+ "----入库成功")
