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



#采集东莞阳光网(CrawlSpider)
#http://wz.sun0769.com/index.php/question/questionType?type=4&page=0
class DongGuanCrawlSpider(CrawlSpider):
    name = "dongguan"
    allowed_domains = ["wz.sun0769.com"]
    start_urls = ['http://wz.sun0769.com/index.php/question/questionType?type=4&page=0']
    rules = (
             Rule(LinkExtractor(allow=r'type=4&page=\d+'),follow=True),
             Rule(LinkExtractor(allow=r'/html/question/\d+/\d+.shtml'), callback='parsedongguan'),
    )
    #process_links="deal_links",
    #处理当前页面url
    def deal_links(self,links):
        for link in links:
            link.url = link.url.replace("?","&").replace("Type&","Type?")
            #print link.url
        #返回 修改完的links链接列表
        return links

    def parsedongguan(self, response):
        print(response.url)

        item = DongGuanItem()
        item['title'] = response.xpath('//div[@class,"pagecenter p3"]//strong/text()').extract()[0]
        #另一种写法
        #item['title'] = response.xpath('//div[contains(@class="pagecenter p3")]//strong/text()').extract()[0]
        item['num'] = item['title'].split(' ')[-1].split(":")[-1]
        # 内容，先取出图片 情况下的匹配规则，如果有内容返回所有的内容列表，如果没有内容，则返回返回空列表
        content = response.xpath('//div[@class="contentext"]/text()').extract()
        #如果没有内容，则返回空列表，则使用无图片情况下匹配规则
        if len(content) == 0:
            content = response.xpath('//div[@class="c1 text14_2"]/text()').extract()#去掉[0]得到所有的
            item['content'] = "".join(content).strip()
        else:
            item['content'] = "".join(content).strip()
            #连接
            item['url'] = response.url
        yield item





from scrapy import Spider,Request
#采集东莞阳光网(Spider)
class DongGuanSpider(scrapy.Spider):
    name = "dongguanspider"
    allowed_domains = ["wz.sun0769.com"]
    #每页页面中所有的链接
    url = 'http://wz.sun0769.com/index.php/question/questionType?type=4&page=0'
    offset = 0
    start_urls =[url + str(offset)]

    def parse(self,response):
        links = response.xpath('//div[@class="greyframe"]/table//td/a[@class="news14"]/@href').extract()
        for link in links:
            #获取每个页面中的链接  发送请求调用parse_item来处理
            yield scrapy.Request(link,callback =self.parse_item)
        #页码终止条件成立前，会一直自增offset的值，并发送新的页面请求，调用parse方法处理
        if self.offset <= 71160:
            self.offset += 30
            #发送请求，放到请求队列李parse
            yield scrapy.Request(self.url+str(self.offset),callback=self.parse)

    def parse_item(self, response):
        print(response.url)

        item = DongGuanItem()
        item['title'] = response.xpath('//div[@class="pagecenter p3"]//strong/text()').extract()[0]
        # 另一种写法
        # item['title'] = response.xpath('//div[contains(@class=,pagecenter p3")]//strong/text()').extract()[0]
        item['num'] = item['title'].split(' ')[-1].split(":")[-1]
        # 内容，先取出图片 情况下的匹配规则，如果有内容返回所有的内容列表，如果没有内容，则返回返回空列表
        content = response.xpath('//div[@class="contentext"]/text()').extract()
        # 如果没有内容，则返回空列表，则使用无图片情况下匹配规则
        if len(content) == 0:
            content = response.xpath('//div[@class="c1 text14_2"]/text()').extract()  # 去掉[0]得到所有的
            item['content'] = "".join(content).strip()
        else:
            item['content'] = "".join(content).strip()
            # 链接
            item['url'] = response.url
            #交给管道
        yield item





