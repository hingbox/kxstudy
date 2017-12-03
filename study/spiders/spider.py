# -*- coding: utf-8 -*-
import scrapy
from study.items import MeiJuItem
from study.items import XiaoHuaItem
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

