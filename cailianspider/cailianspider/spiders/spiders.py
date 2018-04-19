#!/usr/bin/env python
# -*- coding:utf-8 -*-
#encoding=utf-8
'''
@描述：PyCharm
@作者：hingbox
@版本：V1.0
@文件名称 : spiders.py
@创建时间：2018/4/17 19:18
'''
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spider import CrawlSpider,Rule
from cailianspider.items import CailianspiderItem
#导入封装的日志记录模块
from cailianspider.logger import Logger
from scrapy import Spider,Request
import json
import sys
import time
import hashlib
import datetime
import re
reload(sys)
sys.setdefaultencoding('utf8')
 #创建日志记录对象
log = Logger()
class  HeXunSpider(scrapy.Spider):
    name = "cailian"
    allowed_domains = ["www.cailianpress.com"]
    #start_urls = ['http://www.cailianpress.com']
    start_urls = []

    for refresh_type in range(1,3):
        #先获得时间数组格式的日期
        threeDayAgo = (datetime.datetime.now() - datetime.timedelta(days = refresh_type))
        #转换为时间戳:
        timeStamp = int(time.mktime(threeDayAgo.timetuple()))
        #转换为其他字符串格式:
        otherStyleTime = threeDayAgo.strftime("%Y-%m-%d %H:%M:%S")
        # 10位时间戳
        #原始时间戳
        #time.sleep(15)
        last_time = int(1524031483)
        # 创建md5对象
        hl = hashlib.md5()
        hl.update(str(last_time).encode(encoding='utf-8'))
        print('MD5加密后为 ：' + hl.hexdigest())
        sign = hl.hexdigest()
        #last_time_ms = int(round(t * 1000))   #毫秒级时间戳
        urls = 'https://www.cailianpress.com/nodeapi/telegraphs?refresh_type='+str(1)+'&rn=20&last_time='+str(timeStamp)+'&sign='+sign
        start_urls.append(urls)
        print ('start_urls',start_urls)

    # 参数规则 时间戳+页码
    def parse(self, response):
        item = CailianspiderItem()
        js = json.loads(response.body_as_unicode())['data']['roll_data']
        for strStr in js:
            item['title']=strStr['title']
            item['content']=strStr['content']
            item['source']='电报'
            log.info('-------%s %s',strStr['title'],strStr['content'])
            yield item
            #yield Request(response.url,callback=self.parse)

