#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding:utf-8
from imp import reload

__author__ = 'haoning'
# !/usr/bin/env python
import time
import urllib2
import datetime
import requests
import json
import random
import sys
import platform
import uuid

reload(sys)
sys.setdefaultencoding("utf-8")
import re
import os
import MySQLdb as mdb
from bs4 import BeautifulSoup

DB_HOST = '127.0.0.1'
DB_USER = 'root'
DB_PASS = 'root'
# init database
conn = mdb.connect(DB_HOST, DB_USER, DB_PASS, 'pybbs-springboot', charset='utf8')
conn.autocommit(False)
curr = conn.cursor()

count = 0
how_many = 0

base_url = 'http://www.wechat-cloud.com'
url = base_url + "/index.php?s=/home/article/ajax_get_list.html&category_id={category_id}&page={page}&size={size}"

user_agents = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
]


def fake_header():
    agent = random.choice(user_agents)
    cookie = 'PHPSESSID=p5mokvec7ct1gqe9efcnth9d44; Hm_lvt_c364957e96174b029f292041f7d822b7=1487492811,1487556626; Hm_lpvt_c364957e96174b029f292041f7d822b7=1487564069'
    req_header = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        # 'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'www.wechat-cloud.com',
        # 'Cookie':cookie,
        'Referer': 'http://www.wechat-cloud.com/index.php?s=/home/index/index.html',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': agent,
        'X-Requested-With': 'XMLHttpRequest',
    }
    return req_header


def gethtml(url):
    try:
        header = fake_header()
        req = urllib2.Request(url, headers=header)
        response = urllib2.urlopen(req, None, 15)
        html = response.read()
        return html
    except Exception as e:
        print
        "e", e
    return None


def get_img_data(url):
    try:
        # 添加头信息，模仿浏览器抓取网页，对付返回403禁止访问的问题
        req = urllib2.Request(url)
        response = urllib2.urlopen(req, None, 15)
        dataimg = response.read()
        return dataimg
    except Exception as e:
        print
        "image data", e
    return None


def makeDateFolder(par, classify):
    try:
        if os.path.isdir(par):
            newFolderName = par + '//' + str(classify) + "//" + GetDateString()
            if not os.path.isdir(newFolderName):
                os.makedirs(newFolderName)
            return newFolderName
        else:
            return par
    except Exception as e:
        print( "kk", e)
    return par


def map_folder(what):
    return what


def GetDateString():
    when = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    foldername = str(when)
    return foldername


def get_extension(name):
    where = name.rfind('.')
    if where != -1:
        return name[where:len(name)]
    return "#"


def download_img(url, what):
    try:
        # print url
        extention = get_extension(url)
        dataimg = get_img_data(url)
        name = str(uuid.uuid1()).replace('-', '') + "-www.weixinapphome.com"
        # print "name",name
        classfiy_folder = map_folder(what)
        top = "E://wxapp_store"
        filename = makeDateFolder(top, classfiy_folder) + "//" + name + extention
        try:
            if not os.path.exists(filename):
                file_object = open(filename, 'w+b')
                file_object.write(dataimg)
                file_object.close()
                return classfiy_folder + "/" + GetDateString() + "/" + name + extention
            else:
                print("file exist")
                return None
        except IOError as e1:
            print("e1=", e1)
            # pass
        return None  # 如果没有下载下来就利用原来网站的链接
    except Exception as e:
        print("problem", e)
        pass
    return None


def work():
    page = 0
    global how_many
    while 1:
        try:
            page = page + 1
            begin_url = url.format(category_id=0, page=page, size=12).encode('utf-8')
            html = gethtml(begin_url)
            if html is not None:
                # print html
                json_results = json.loads(html)
                is_end = json_results['isEnd']
                if str(is_end) == "True":
                    break
                results = json_results['list']
                for result in results:
                    href = result['href']
                    detail_url = base_url + href
                    # print detail_url
                    detail_html = gethtml(detail_url)
                    if detail_html is not None:
                        soup = BeautifulSoup(detail_html)
                        icon_url = base_url + soup.find('div', {'class': 'icon fl'}).find('img').get('src')
                        name = soup.find('div', {'class': 'cont fl'}).find('h2').text
                        classify = soup.find('div', {'class': 'tab'}).find('span').text
                        classify = str(classify).replace("分类: ", "")
                        # print classify
                        barcode_path = base_url + soup.find('div', {'id': 'install-code'}).find('img').get('src')
                        view_num = soup.find('span', {'class': 'views'}).text
                        # view_num=filter(str.isalnum,str(view_num))
                        pic_path = base_url + soup.find('div', {'class': 'img-box'}).find('img').get('src')
                        temp = time.time()
                        x = time.localtime(float(temp))
                        acq_time = time.strftime("%Y-%m-%d %H:%M:%S", x)  # get time now
                        curr.execute('select id from pybbs_wxapp_store where `from`=%s', (detail_url))
                        y = curr.fetchone()
                        if not y:
                            y1 = download_img(icon_url, "icon")
                            y2 = download_img(barcode_path, "barcode")
                            y3 = download_img(pic_path, "pic")
                            if (y1 is not None) and (y2 is not None) and (y3 is not None):
                                name = name
                                author = None
                                classify = classify
                                describe = None
                                view_num = view_num
                                # print view_num
                                logo = y1
                                _from = detail_url
                                barcode = y2
                                acq_time = acq_time
                                hot_weight = -9999
                                pic_uuid = str(uuid.uuid1()).replace('-', '')
                                pic_path = y3
                                # print name,author,classify,describe,view_num,logo,_from,barcode,acq_time,hot_weight,pic_uuid
                                curr.execute(
                                    'INSERT INTO pybbs_wxapp_store(name,author,classify,`describe`,view_num,logo,`from`,barcode,acq_time,hot_weight,pic_path)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                                    (name, author, classify, describe, view_num, logo, _from, barcode, acq_time,
                                     hot_weight, pic_path))
                                curr.execute('select id from pybbs_wxapp_classify where `classify_name`=%s', (classify))
                                yx = curr.fetchone()
                                if not yx:
                                    describe = None
                                    temp = time.time()
                                    x = time.localtime(float(temp))
                                    record_time = time.strftime("%Y-%m-%d %H:%M:%S", x)  # get time now
                                    curr.execute(
                                        'INSERT INTO pybbs_wxapp_classify(classify_name,`describe`,record_time)VALUES(%s,%s,%s)',
                                        (classify, describe, record_time))
                                how_many += 1
                                print
                                "new comer:", pic_uuid, ">>", how_many
                                if how_many % 10 == 0:
                                    conn.commit()
                conn.commit()
        except Exception as e:
            print
            "while error", e


if __name__ == '__main__':
    i = 3
    while i > 0:
        work()
        i = i - 1