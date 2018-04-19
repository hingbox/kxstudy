#!/usr/bin/env python
# -*- coding:utf-8 -*-
#encoding=utf-8
'''
@描述：快讯
@作者：hingbox
@版本：V1.0
@文件名称 : spiders.py
@创建时间：2018/4/18 17:14
'''
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spider import CrawlSpider,Rule
from kuaixunspider.items import KuaixunspiderItem
#导入封装的日志记录模块
from kuaixunspider.logger import Logger
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

class KuaixunSpider(scrapy.Spider):
    name = "kuaixun"
    allowed_domains = ["kuaixun.stcn.com"]
    start_urls = ['http://www.stcn.com/']
    #获取页面a标签的url
    def parse(self, response):
        div = response.xpath('//div[@class="kuaixun"]/div[@class="title"]')
        url = div.xpath('./a/@href').extract()[0]
        #log.info('-----url %s', url)
        for page in range(2,21):
             url = 'http://kuaixun.stcn.com/index_'+str(page)+'.shtml'
             yield scrapy.Request(url, callback=self.parse_items)

    def parse_items(self, response):
        new_items = response.xpath('//div[@class="mainlist"]/ul/li')
        for new_item in new_items:
            href = new_item.xpath('./p/a[2]/@href').extract()[0]
            title = new_item.xpath('./p/a[2]/text()').extract()[0]
            #log.info('---newurl %s %s',href,title)
            yield scrapy.Request(href,callback=self.parse_detail)


    def parse_detail(self,response):
        item = KuaixunspiderItem()
        respnse_content = response.xpath('//div[@class="kx_left"]')
        if respnse_content:
           response_content = respnse_content
        else:
           respnse_content = response.xpath('//div[@class="box_left"]')
        title = respnse_content.xpath('./div[@class="intal_tit"]/h2/text()').extract()[0]
        time_and_source = respnse_content.xpath('./div[@class="intal_tit"]/div[@class="info"]/text()').extract()[0]
        content = respnse_content.xpath('./div[@class="txt_con"]/text()').extract()
        # if time_and_source:
        #     time_and_source_str = time_and_source.split()
        #     times = time_and_source_str[0]+":"+time_and_source_str[1]
        #     source = time_and_source_str[2]

       # source = time_and_source_str[1]
        item['url']=response.url
        item['content']=content
        item['title']=title
        item['pubshTime']=time_and_source
        log.info('parse_detail %s %s %s %s ',response.url,title,time_and_source,content)
        yield item


