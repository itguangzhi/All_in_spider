# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

import pymysql
import pymysql.cursors
from twisted.enterprise import adbapi



class AllInSpiderPipeline(object):
    def process_item(self, item, spider):
        print(item)
        return item


class JsonWithEncodingPipeline(object):
    # 自定义json文件的导出
    def __init__(self):
        self.file = codecs.open("tianqihoubao.json", "w", "utf-8")

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self,spider):
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
        """%(item["item_uuid"]
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
                                    ,item["wind_black_direction"]
                                    ,item["item_wind_light"]
                                    ,item["item_wind_black"])

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


    def do_insert(self,cursor ,item):
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
