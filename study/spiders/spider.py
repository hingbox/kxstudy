# -*- coding: utf-8 -*-
import scrapy
from study.items import MeiJuItem
from study.items import XiaoHuaItem
from study.items import DongGuanItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spider import CrawlSpider,Rule
class MeijuSpider(scrapy.Spider):
    name="meiju"
    allowed_domains=["meijutt.com"]
    start_urls = ['http://www.meijutt.com/new100.html']
    def parse(self, response):
        movies = response.xpath('//ul[@class="top-list  fn-clear"]/li')
        for each_move in movies:
            item = MeiJuItem()
            item['name'] = each_move.xpath('./h5/a/@title').extract()[0]
            #item['status'] = each_move.xpath('//span[@class="state1  new100state1"]/font/text()').extract()[0]
            item['place'] = each_move.xpath('./span[@class="mjtv"]/text()').extract()[0]
            yield item


class XiaoHauSpider(scrapy.Spider):
    name="xiaohua"
    allowed_domains=["xiaohuar.com"]
    start_urls = ['http://www.xiaohuar.com/list-1-1.html']
    def parse(self, response):
        all_pics = response.xpath('div[@class="img"]/a')
        for pic in all_pics:
            #分别处理每个图片 得到每个图片的url以及图片
            item = XiaoHuaItem()
            name = pic.xpath('./img/@alt').extract()[0]
            address = pic.xpath('./img/@src').extract()[0]
            item["name"] = name
            item["address"] = "http://www.xiaohuar.com"+address
            yield item



#采集东莞阳光网
#http://wz.sun0769.com/index.php/question/questionType?type=4&page=0
class DongGuanSpider(CrawlSpider):
    name = "dongguan"
    allowed_domains = ["wz.sun0769.com"]
    start_urls = ['http://wz.sun0769.com/index.php/question/questionType?type=4&page=0']
    rules = (
            Rule(LinkExtractor(allow=r'type=4&page=\d+')),
            Rule(LinkExtractor(allow=r'/html/question/\d+/\d+.shtml'), callback='parsedongguan'),
    )

    def parsedongguan(self, response):
        item = DongGuanItem()
        item['title'] = response.xpath('//div[@class="pagecenter p3"]//strong/text()').extract()[0]
        item['num'] = item['title'].split(' ')[-1].split(":")[-1]
        item['content'] = response.xpath('//div[@class="c1 text14_2"]/text()').extract()[0]
        item['url'] = response.url
        yield item



