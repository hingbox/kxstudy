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
    start_urls = ['http://www.hexun.com/']

    def parse(self, response):
        #获取首页上的标签  股票/7*24小时快讯;
        #上面是对class 匹配，下面是对id进行模糊皮匹配  返回 新闻/事实;
        result1 = response.xpath('//div[contains(@id,"con_setA")]/div[@class="newsList"]/ul/li')
        #返回
        result2 = response.xpath('//div[contains(@id,"con_setQES")]/div[@class="newsList"]/ul/li')
        #和讯名家,行情追踪
        result3 = response.xpath('//div[@class="layout mg pt44 clearfix"]')
        #基金私募信托,互金理财债券
        result4 = response.xpath('//div[@class="layout mg pt44 pb20 clearfix"]')
        #原油，期货，现货
        result5 = response.xpath('//div[@class="layout mg pt10 clearfix"]')
        # for div_item in result1:
        #     item = HexunspiderItem()
        #     href = div_item.xpath('./a/@href').extract()[0]
        #     item['title'] = div_item.xpath('./a/text()').extract()[0]
        #     log.info('新闻，事实url----%s %s',div_item.xpath('./a/@href').extract()[0],div_item.xpath('./a/text()').extract()[0])
        #     request = scrapy.Request(href, callback=self.prase_detail)
        #     #将未完成的item 通过meta 传到下一个函数
        #     request.meta['item'] = item
        #     yield request
            # 等价于 另一种写法
            #yield scrapy.Request(href,callback=self.prase_detail,meta={'item':item})

        # for retust_tw in result2:
        #     item = HexunspiderItem()
        #     href = retust_tw.xpath('./a/@href').extract()[0]
        #     item['title'] = retust_tw.xpath('./a/text()').extract()[0]
        #     log.info(' 股票，7*24小时快讯url----%s',retust_tw.xpath('./a/@href').extract()[0])
        #     request = scrapy.Request(href, callback=self.prase_detail)
        #     request.meta['item'] = item
        #     yield request

        for div_item in result3:
            items =[]
            #得到
            urs = div_item.xpath('//div[@class="newsList"]/ul')
            for ul in urs:
                item = HexunspiderItem()
                item['url'] = ul.xpath('./li/a/@href').extract()[0]
                item['title'] = ul.xpath('./li/a/text()').extract()[0]
                items.append(item)
            for item in items:
                log.info('info three----url %s %s',item['url'],item['title'])
                request = scrapy.Request(item['url'],callback=self.prase_detail)
                request.meta['item'] = item
                yield request


        # for div_item in result4:
        #     #得到
        #     urs = div_item.xpath('//div[@class="newsList"]/ul')
        #     for ul in urs:
        #         log.info('所有----url %s',ul.xpath('./li/a/@href').extract()[0])


    def prase_detail(self, response):
        item = response.meta['item']#获取未完成的items
        item['content'] = response.xpath('//div[@class="art_context"]/div[@class="art_contextBox"]/p/text()').extract()
        #item['pushTime'] = response.xpath('//div[@class="clearfix"]/div[@class="tip fl"]/span[@class="pr20"]/text()').extract()[0]
        yield item #构造完成，生成

     #返回新闻，事实
    def return_result_one(self,response):
        return response.xpath('//div[contains(@id,"con_setA")]/div[@class="newsList"]/ul/li')
    #返回 股票，7*24小时快讯
    def return_result_two(self,response):
        return response.xpath('//div[contains(@id,"con_setQES")]/div[@class="newsList"]/ul/li')

    #和讯名家；行情追踪；基金私募信托;互金理财债券，原油;期货期指现货；银行消费金融，保险养老金;黄金白银;外汇汇率;科技数码;汽车车型
    def return_all(self,response):
        return response.xpath('//div[@class="layout mg pt44 clearfix"][1]/div[@class="c1"]/div[@class="newList"]/ul[1]/li')



