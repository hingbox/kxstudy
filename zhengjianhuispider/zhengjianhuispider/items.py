# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#证监会
class ZhengjianhuispiderItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    source = scrapy.Field()
    pubsh_time = scrapy.Field()
#央行
class YanghangspiderItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    source = scrapy.Field()
    pubsh_time = scrapy.Field()

#银监会
class YingjianhuispiderItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    source = scrapy.Field()
    pubsh_time = scrapy.Field()

#统计局
class TongjijuspiderItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    source = scrapy.Field()
    pubsh_time = scrapy.Field()


#财政新闻
class CaizhengxinwenspiderItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    source = scrapy.Field()
    pubsh_time = scrapy.Field()

#同花顺
class TonghuashunspiderItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    describe = scrapy.Field()
    source = scrapy.Field()
    pubsh_time = scrapy.Field()

 #中证热点网
class ZhongzhengredianspiderItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    describe = scrapy.Field()
    source = scrapy.Field()
    pubsh_time = scrapy.Field()

#金融界
class JinrongjiespiderItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    describe = scrapy.Field()
    source = scrapy.Field()
    type =scrapy.Field()
    pubsh_time = scrapy.Field()

#中古橡胶网
class XiangjiaowangspiderItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    describe = scrapy.Field()
    source = scrapy.Field()
    type =scrapy.Field()
    pubsh_time = scrapy.Field()