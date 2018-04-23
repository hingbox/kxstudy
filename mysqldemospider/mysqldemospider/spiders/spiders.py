#!/usr/bin/env python
# -*- coding:utf-8 -*-
#encoding=utf-8
'''
@描述：PyCharm
@作者：hingbox
@邮箱：hingbox@163.com
@版本：V1.0
@文件名称 : spiders.py
@创建时间：2018/4/23 21:38
'''
import scrapy
from mysqldemospider.items import MysqldemospiderItem
#导入封装的日志记录模块
import sys
reload(sys)
sys.setdefaultencoding('utf8')
class mysqldemospider(scrapy.Spider):
    name = "mysqldemo"
    #allowed_domains = ["www.yicai.com/"]
    start_urls = ['https://www.baidu.com/']
    def parse(self, response):
        res_items = response.xpath('//a')
        for res_item in res_items:
            item = MysqldemospiderItem()
            item['url'] = res_item.xpath('./@href').extract_first()
            item['title'] = res_item.xpath('./text()').extract_first()
            yield  item
