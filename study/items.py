# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item

class StudyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class MeiJuItem(Item):
    name = scrapy.Field()
    status = scrapy.Field()
    place = scrapy.Field()


class XiaoHuaItem(Item):
    address = scrapy.Field()
    name = scrapy.Field()


class DongGuanItem(Item):
    title = scrapy.Field()
    num = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()


class DouBanItem(Item):
    title = scrapy.Field()#标题
    bd = scrapy.Field()#信息
    star = scrapy.Field()#评分
    quote = scrapy.Field()#简介