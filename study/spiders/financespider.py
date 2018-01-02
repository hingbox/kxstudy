# -*- coding: utf-8 -*-
#coding=utf-8
import scrapy
from study.items import CaiJingXinWenItem
class TenecntSpider(scrapy.Spider):
    name = 'tencent1'
    # 可选，加上会有一个爬去的范围
    allowed_domains = ['www.prcfe.com']
    start_urls = ['http://www.prcfe.com/news/index_2.htm']
    def parse(self,response):
        links = response.xpath('//div[@class="tab-text"]/p/a/@href').extract()
        for link in links:
            nurl = "http://www.prcfe.com"+link
            print ('nurl-----', nurl)
            yield scrapy.Request(nurl, callback=self.parse_item)

    def parse_item(self, response):

        item = CaiJingXinWenItem()
        item['link'] = response.url
        item['title'] = response.xpath('//div[@class="main"]/div[@class="top-line"]/h1/span/text()').extract()[0]
        item['content'] = response.xpath('//div[@class="main-left-article"]/p/text()').extract()
        yield item

