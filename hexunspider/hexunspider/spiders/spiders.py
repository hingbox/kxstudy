# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spider import CrawlSpider,Rule
from hexunspider.items import HexunspiderItem
#导入封装的日志记录模块
from hexunspider.logger import Logger
from scrapy import Spider,Request
import json
import sys
import time
import re
reload(sys)
sys.setdefaultencoding('utf8')
#和讯网(解析页面元素,得到数据,并入库)

 #创建日志记录对象
log = Logger()
class HeXunSpider(scrapy.Spider):
    name = "hexun"
    allowed_domains = ["news.hexun.com"]
    start_urls = ['http://news.hexun.com/']
    def parse(self, response):
        #获取首页上的标签  新闻/事实;股票/7*24小时快讯;
        div_items = response.xpath('//*[starts-with(@class,"c1")]/div[@class="newsTop"]')
        log.info('----%s',div_items)
        # for div_item in div_items:
        #     link = div_item.xpath('./li/a[1]/@href').extract()[0]
        #     title = div_item.xpath('./li/a[1]/text()').extract()[0]
        #     print ('------link----',link,'-----title------ ',title)
        #     #print url
        #     yield scrapy.FormRequest(
        #         url=link,
        #         meta={
        #             'url': link,
        #             'title': title
        #         },
        #         method='GET',
        #         dont_filter=True,
        #         callback=self.prase_detail
        #     )

    def prase_detail(self, response):
        item = HeXunItem()
        item['url'] = response.meta['url']
        item['title'] = response.meta['title']
        item['content'] = response.xpath('//div[@class="art_context"]/div[@class="art_contextBox"]/p/text()').extract()
        #item['pushTime'] = response.xpath('//div[@class="clearfix"]/div[@class="tip fl"]/span[@class="pr20"]/text()').extract()[0]
        return item

# class HeXunSpider(scrapy.Spider):
#     name = "hexun"
#     allowed_domains = ["news.hexun.com"]
#     start_urls = ['http://news.hexun.com/']
#     def parse(self, response):
#         #从左边开始匹配
#         div_items = response.xpath('//*[starts-with(@class,"m_news")]/ul')
#         for div_item in div_items:
#             link = div_item.xpath('./li/a[1]/@href').extract()[0]
#             title = div_item.xpath('./li/a[1]/text()').extract()[0]
#             print ('------link----',link,'-----title------ ',title)
#             #print url
#             yield scrapy.FormRequest(
#                 url=link,
#                 meta={
#                     'url': link,
#                     'title': title
#                 },
#                 method='GET',
#                 dont_filter=True,
#                 callback=self.prase_detail
#             )
#
#     def prase_detail(self, response):
#         item = HeXunItem()
#         item['url'] = response.meta['url']
#         item['title'] = response.meta['title']
#         item['content'] = response.xpath('//div[@class="art_context"]/div[@class="art_contextBox"]/p/text()').extract()
#         #item['pushTime'] = response.xpath('//div[@class="clearfix"]/div[@class="tip fl"]/span[@class="pr20"]/text()').extract()[0]
#         return item