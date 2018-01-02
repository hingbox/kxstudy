# -*- coding: utf-8 -*-
from scrapy import Spider,Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spider import CrawlSpider,Rule
#证监会

class ZhengQuanHuiSpider(Spider):
    name = "zhengquanhui"
    allowed_domains = ["www.csrc.gov.cn"]
    start_urls = ("http://www.csrc.gov.cn/pub/newsite/zjhxwfb/xwfbh/",)

    def parse(self, response):
        links = response.xpath('//ul[@id="myul"]/li/a/@href')
        for link in links:
            print link.extract()
#央行
class YangHangSpider(Spider):
    name = "yanghang"
    allowed_domains = ["www.pbc.gov.cn"]
    start_urls =("http://www.pbc.gov.cn/goutongjiaoliu/113456/113469/index.html",)

    def parse(self,response):
        print (response.text)
        links = response.xpath('//font[@class="newslist_style"]/a/@href')
        for link in links:
            print link


#银监会
class YingJianHuiSpider(Spider):
    name ="yingjianhui"
    allowed_domains = ["www.cbrc.gov.cn"]
    start_urls =["http://www.cbrc.gov.cn/chinese/home/docViewPage/114.html"]
    def parse(self,response):
        for link in response.xpath('//tbody//tr//td[1]/a/@href').extract():
            print link.extract()

#保监会
class BaoJianHui(Spider):
    name ="baojianhui"
    allowed_domains = ["www.circ.gov.cn"]
    start_urls = ["http://www.circ.gov.cn/web/site0/tab5207/"]
    def parse(self,response):
        linkss = response.xpath('//td[@class="hui14"]/a/@href').extract()
        for link in linkss:
            url = "http://www.circ.gov.cn"+link
            yield Request(url,callback=self.parse_item)

    def parse_item(self,response):
        print response.xpath('//tbody//tr//span[@id="zoom"]/text()').extract()
#统计局
# class TongJiJuSpider(scrapy.Spider):
#     pass
#外汇管理局
# class WaiHuiJuSpider(scrapy.Spider):
#     pass
#财政部
# class CaiZhengBuSpider(scrapy.Spider):
#     pass
#发改委
#工信部
#国土部
#海关总署
#交通部
#商务部
#水利部
#中国政府网
#住建部
#中央纪委监察部
#环保总局
#国家电力监管委员会
#能源局



# #3.主流财经媒体
# #财经国家新闻网
# class CaiJingSpider(CrawlSpider):
#     name = "caijingguojiaxinwenwang"
#     allowed_domains = ["http://www.prcfe.com"]
#     start_urls = ["http://www.prcfe.com/news/index_2.htm"]
#     # response中提取 链接的匹配规则，得出是符合的链接
#     pagelink =LinkExtractor(allow=('index_=\d+'))
#     print (pagelink)
#     # rules = (
#     #     Rule(LinkExtractor(allow=r'_\d+'), follow=True, callback="parse_item"),
#     # )
#     # def parse_item(self,respone):
#     #     print respone
