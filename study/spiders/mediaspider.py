# -*- coding: utf-8 -*-
import scrapy
#证监会

# class ZhengQuanHuiSpider(scrapy.Spider):
#     name ="zhengquanhui"
#     allowed_domains = ["http://www.csrc.gov.cn"]
#     start_url =["http://www.csrc.gov.cn/pub/newsite/zjhxwfb/"]
#     def parse(self,response):
#         links = response.xpath('//ul[@id="myul"]/li/a/@href')
#         for link in links:
#             print link.extract()

#央行
# class YangHangSpider(object):
#     pass
#银监会
# class YingJianHuiSpider(object):
#     pass

#保监会
# class BaoJianHui(object):
#     pass
#统计局
# class TongJiJuSpider(object):
#     pass
#外汇管理局
# class WaiHuiJuSpider(object):
#     pass
#财政部
# class CaiZhengBuSpider(object):
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
class ZhongJiWeiSpider(scrapy.Spider):
    name = "zhongjiwei"
    allowed_domains = ["www.ccdi.gov.cn"]
    start_urls = "http://www.ccdi.gov.cn/was5/web/search?channelid=202789&page=1"
    #offset = 0
   # start_urls = [url+str(offset)]
    #分页url
    def parse(self, response):
        links = response.xpath('//div[@id="wcmpagehtml"]/ul//li/a/@href').extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_item)

    def parse_item(self, response):
        print response.xpath('//div[@class="Article_61"]//h2[@class="tit"]/text()').extract()[0]
#环保总局
#国家电力监管委员会
#能源局
