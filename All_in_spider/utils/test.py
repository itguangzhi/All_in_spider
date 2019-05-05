#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib import request
import re
from fake_useragent import UserAgent

url = 'http://www.bjjfr.com/kezhao/'
listpage = 6
imgDIR = r'./kepian//'
ypimgDIR = r'./yangpian//'
yplistpage = 11
ua = UserAgent()
def getResponse(url):
    header = {}
    header['User-Agent'] = ua.random
    response = request.urlopen(url,)
    result = response.read().decode('utf-8')
    return result

def getDetail(response,dir):
    reg = '<img alt="" src="/uploads/allimg/(.*?).jpg" />'
    namereg = '<title>(.*?)_北京金夫人</title>'
    imglist = re.findall(reg,response)
    for imgURL in imglist:
        url = 'http://www.bjjfr.com/uploads/allimg/%s.jpg'%str(imgURL)
        name = str(re.findall(namereg,response)[0]).replace(' ','').replace('/','-')+'_'+imgURL.replace('/','-')
        request.urlretrieve(url,dir + name + '.jpg')

if __name__ == '__main__':
    # 客片
    for i in range(1,listpage+1):
        url = 'http://www.bjjfr.com/kezhao/'
        url = url + 'list'+str(i)+ '.html'
        result = getResponse(url)
        reg = '<a href="/kezhao/(.*?).html" target="_blank"><img src="/uploads/allimg/.*?" alt=".*?客片"></a>'
        kezhao = re.findall(reg,str(result))
        kezhao.append('1890')
        kezhao.append('1891')
        kezhao.append('1892')
        for kezhaoimg in kezhao:
            detailURL = 'http://www.bjjfr.com/kezhao/%s.html'%str(kezhaoimg)
            detail = getResponse(detailURL)
            res = getDetail(detail,imgDIR)
            print(detailURL)

        print(url, 'OK')

    # 样片
    for a in range(1,yplistpage+1):
        ypurl = 'http://www.bjjfr.com/zp/list%d.html'%a
        ypresult = getResponse(ypurl)
        ypreg = '<a href="/zuopin/(.*?).html" target="_blank"><img src=".*?" alt=""></a>'
        yplist = re.findall(ypreg,str(ypresult))
        for n in yplist:
            ypdetailurl = 'http://www.bjjfr.com/zuopin/%s.html'%str(n)
            ypdetail = getResponse(ypdetailurl)
            res = getDetail(ypdetail, ypimgDIR)
            print(ypdetailurl)
        print(ypurl, 'OK')
