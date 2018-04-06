# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spider import CrawlSpider,Rule
from study.items import PatentItem
from study.financeitems import YiCaiFinanceItem
from study.financeitems import SinaFinanceItem
from scrapy import Spider,Request
#新浪财经
class SinaFinanceSpider(scrapy.Spider):
    name = "sinaFinance"
    allowed_domains = ["finance.sina.com.cn/"]
    start_urls = ['http://www.meijutt.com/new100.html']
    def parse(self, response):
        movies = response.xpath('//ul[@class="top-list  fn-clear"]/li')
        for each_move in movies:
            item = SinaFinanceItem()
            item['name'] = each_move.xpath('./h5/a/@title').extract()[0]
            #item['status'] = each_move.xpath('//span[@class="state1  new100state1"]/font/text()').extract()[0]
            item['place'] = each_move.xpath('./span[@class="mjtv"]/text()').extract()[0]
            yield item
#第一财经
class yiCaiFinanceSpider(scrapy.Spider):
    name = "yiCaiFinance"
    allowed_domains = ["www.yicai.com/"]
    start_urls = ['http://www.yicai.com/news/']

    def parse(self, response):
        dlItems = response.xpath('//div[@class="m-list8"]/dl')
        for dl in dlItems:
            item = YiCaiFinanceItem()
            url=dl.xpath('./dd/h3/a/@href').extract()[0]
            yield scrapy.FormRequest(
                url=url,
                meta={'url' : url,
                      'oldUrl':dl.xpath('./dd/h3/a/@href').extract()[0],
                      'title':dl.xpath('./dd/h3/a/text()').extract()[0],
                      'desc':dl.xpath('./dd/p/text()').extract()[0],
                      'pushTime':dl.xpath('./dd/h4/text()').extract()[0]
                                 },
                method='GET',
                dont_filter=True,
                callback=self.parseDetail)



    def parseDetail(self,response):
        print response.meta['url']
        item = YiCaiFinanceItem()
        item['url']=response.meta['oldUrl']
        item['title']=response.meta['title']
        item['desc'] = response.meta['desc']
        item['pushTime'] = response.meta['pushTime']
        item['content']= response.xpath('//div[@class="m-text"]/p/text()').extract()
        yield item


    def nextRequest(self,response):
        print '进来了'
        yield scrapy.FormRequest(url='http://www.yicai.com/api/ajax/NsList/6/77',
                                 method='POST',
                                 formdata={
                                     'news_List': "news_List",
                                 },
                                 dont_filter=True,
                                 callback=self.parse
                                 )
