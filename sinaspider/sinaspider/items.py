# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaspiderItem(scrapy.Item):
    title = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()
    desc = scrapy.Field()
    content = scrapy.Field()
    pushTime = scrapy.Field()