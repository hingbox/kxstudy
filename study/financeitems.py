# -*- coding: utf-8 -*-
import scrapy
from scrapy.item import Item
#新浪财经
class SinaFinanceItem(scrapy.Item):
    title = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
#第一财经
class YiCaiFinanceItem(scrapy.Item):
    title = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()
    desc = scrapy.Field()
    content = scrapy.Field()
    pushTime = scrapy.Field()

# 华尔街见闻
class WallStreetItem(scrapy.Item):
    title = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()
    desc = scrapy.Field()
    content = scrapy.Field()
    pushTime = scrapy.Field()

#中金在线
class CnfolItem(scrapy.Item):
    title = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()
    desc = scrapy.Field()
    content = scrapy.Field()
    pushTime = scrapy.Field()


