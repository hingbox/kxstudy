# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

'''
新浪新闻item
'''
class SinaspiderItem(scrapy.Item):
    title = scrapy.Field()#标题
    source = scrapy.Field()#来源
    orgurl = scrapy.Field()#原始url
    type = scrapy.Field()#类型
    content = scrapy.Field()#内容
    writer = scrapy.Field()#作者
    summary = scrapy.Field()#摘要
    pubdate = scrapy.Field()#发布日期
    create_date = scrapy.Field()#创建时间
    recorddate = scrapy.Field#记录日期
    sourcecategory = scrapy.Field()#资源类别
    tags = scrapy.Field()#标签
    opinion = scrapy.Field()#看法
    remarks = scrapy.Field()#备注
    category_id = scrapy.Field()#栏目