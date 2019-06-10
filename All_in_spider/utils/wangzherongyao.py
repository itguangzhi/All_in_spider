#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
                            _ooOoo_  
                           o8888888o  
                           88" . "88  
                          (|  -_-  |)  
                           O\  =  /O  
                        ____/`---'\____  
                      .   ' \\| |// `.  
                       / \\||| : |||// \  
                     / _||||| -:- |||||- \  
                       | | \\\ - /// | |  
                     | \_| ''\---/'' | |  
                      \ .-\__ `-` ___/-. /  
                   ___`. .' /--.--\ `. . __  
                ."" '< `.___\_<|>_/___.' >'"".  
               | | : `- \`.;`\ _ /`;.`/ - ` : | |  
                 \ \ `-. \_ __\ /__ _/ .-` / /  
         ======`-.____`-.___\_____/___.-`____.-'======  
                            `=---='  
  
         .............................................  
                  佛祖镇楼                  BUG辟易  
          佛曰:  
                  写字楼里写字间，写字间里程序员；  
                  程序人员写程序，又拿程序换酒钱。  
                  酒醒只在网上坐，酒醉还来网下眠；  
                  酒醉酒醒日复日，网上网下年复年。  
                  但愿老死电脑间，不愿鞠躬老板前；  
                  奔驰宝马贵者趣，公交自行程序员。  
                  别人笑我忒疯癫，我笑自己命太贱；  
                  不见满街漂亮妹，哪个归得程序员？ 
'''
# @File  : wangzherongyao.py
# @Author: huguangzhi
# @Drivce: Thinkpad E470
# @ContactEmail : huguangzhi@ucsdigital.com.com 
# @ContactPhone : 13121961510 
# @Date  : 2019-06-10 - 15:29
# @Desc  :

import requests

import os
from fake_useragent import UserAgent
ua = UserAgent()

url = 'http://pvp.qq.com/web201605/js/herolist.json'


head = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'}
response = requests.get(url, headers=head)
hero_list = response.json()

# 提取英雄名字和数字
hero_name=list(map(lambda x:x['cname'], hero_list))

hero_number=list(map(lambda x:x['ename'], hero_list))

hero_name_title=list(map(lambda x:x['title'], hero_list))

h_l='http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/'


for n,i in enumerate(hero_number):
    headers = {
        "User-Agent": ua.random,
        "referer": "https://pvp.qq.com/web201605/herodetail/%s.shtml"%i
    }
    # 逐一遍历皮肤，此处假定一个英雄最多有15个皮肤
    for sk_num in range(15):
        hsl = h_l + str(i)+'/'+str(i)+'-bigskin-'+str(sk_num)+'.jpg'
        hl = requests.get(hsl,headers=headers)
        filepath = "./img/"+hero_name[n]+ "_" + hero_name_title[n]+str(sk_num) + '.jpg'
        if hl.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(hl.content)
                print(hero_name[n] + "ok" + str(sk_num))
        else:
            break
