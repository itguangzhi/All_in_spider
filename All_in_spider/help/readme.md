# 注意事项

###  DEBUG: Filtered offsite request to
在进行爬虫的时候，从上一个页面请求到下一个页面中，发现无法请求，但是日志也没有报错，翻看日志发现，这样的一个debug内容
```angular2
 DEBUG: Filtered offsite request to 'www.tianqihoubao.com': <GET http://www.tianqihoubao.com/lishi/bj.htm>
```
遇到这种情况，有两种
1. 调用的Request中，没有设置过滤器为否，会将allowed_domains的连接过滤掉，遇到这种情况，设置dont_filter为True即可
2. 设置allowed_domains为一级域名，去掉www的绝对域名，如tianqihoubao.com，即可