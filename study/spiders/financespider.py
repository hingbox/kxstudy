# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spider import CrawlSpider,Rule
from study.items import PatentItem
from study.financeitems import YiCaiFinanceItem
from study.financeitems import SinaFinanceItem
from study.financeitems import WallStreetItem
from study.financeitems import CnfolItem
from scrapy import Spider,Request
import logging
import json
import sys
import time
import re
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
        item['url'] = response.meta['oldUrl']
        item['title'] = response.meta['title']
        item['desc'] = response.meta['desc']
        item['pushTime'] = response.meta['pushTime']
        item['content'] = response.xpath('//div[@class="m-text"]/p/text()').extract()
        yield item


    def nextRequest(self,response):
        print '进来了'
        yield scrapy.FormRequest(url='http://www.yicai.com/api/ajax/NsList/6/77',
                                 method='POST',
                                 formdata={
                                     'news_List': "news_List"
                                 },
                                 dont_filter=True,
                                 callback=self.parse
                                 )



#华尔街见闻
class WallStreetSpider(scrapy.Spider):
    name = "wallStreet"
    allowed_domains = ["wallstreetcn.com"]
    start_urls = ['https://wallstreetcn.com/news/global?from=home']
    def parse(self, response):
        div_items = response.xpath('//div[@class="news-item__main"]')
        for div_item in div_items:
            url = "https://wallstreetcn.com" + div_item.xpath('./a[@class="news-item__main__title"]/@href').extract()[0]
            #print url
            yield scrapy.FormRequest(
                url=url,
                meta={
                    'oldUrl': "https://wallstreetcn.com" + div_item.xpath('./a[@class="news-item__main__title"]/@href').extract()[0],
                    'title': div_item.xpath('./a[@class="news-item__main__title"]/text()').extract()[0],
                    'desc': div_item.xpath('./a[@class="news-item__main__summary"]/text()').extract()[0]
                },
                method='GET',
                dont_filter=True,
                callback=self.prase_detail)

    def prase_detail(self, response):
        print response.meta['oldUrl']
        item = WallStreetItem()
        item['url'] = response.meta['oldUrl']
        item['desc'] = response.meta['desc']
        item['title'] = response.meta['title']
        item['content'] = response.xpath('//div[@class="node-article-content"]/p/text()').extract()
        item['pushTime'] = response.xpath('//span[@class="meta-item__text"]/text()').extract()[0]
        yield item


#华尔街见闻 分页解析json
class WallStreetJsonSpider(scrapy.Spider):
    name = "wallStreetJson"
    allowed_domains = ["wallstreetcn.com"]
    page =1000
    #for page in range(1,3):
    start_urls = ['https://api-prod.wallstreetcn.com/apiv1/content/articles?platform=wscn-platform&category=us&limit='+str(page)]
    print ('orgin url',start_urls)
    def parse(self, response):
        js = json.loads(response.body_as_unicode())['data']['items']
        for item in js:
            #print ('--item',item['uri'])
            yield scrapy.FormRequest(
                url=item['uri'],
                method='GET',
                meta={
                    'url':item['uri'],
                    'title':item['title'],
                    'desc':item['content_short']
                },
                dont_filter=True,
                callback=self.prase_detail
               )

    def prase_detail(self, response):
        print response.meta['url']
        item = WallStreetItem()
        item['url'] = response.meta['url']
        item['desc'] = response.meta['desc']
        item['title'] = response.meta['title']
        item['content'] = response.xpath('//div[@class="node-article-content"]/p/text()').extract()
        item['pushTime'] = response.xpath('//span[@class="meta-item__text"]/text()').extract()[0]
        yield item


#中金在线
class CnfolSpider(scrapy.Spider):
    name = "cnfol"
    allowed_domains = ["news.cnfol.com/"]
    start_urls = ['http://news.cnfol.com/']
    def parse(self, response):
        #从左边开始匹配
        div_items = response.xpath('//*[starts-with(@class,"artBlock")]')
        for div_item in div_items:
            link = div_item.xpath('./a[1]/@href').extract()[0]
            title = div_item.xpath('./a[1]/text()').extract()[0]

            #判断如果是空的换行
            if title.strip() == "":
                link = div_item.xpath('./a[@class="h3"]/@href').extract()[0]
                title = div_item.xpath('./a[@class="h3"]/text()').extract()[0]
                source = div_item.xpath('./h3/a[1]/text()').extract()[0]
                pushTime = div_item.xpath('./h3/span/text()').extract()[0]
            else:
                title = title
                link = link
                source = '无'
                pushTime = '无'
            print ('link',link,'title',title,'source',source,'pushTime',pushTime)
            #print url
            # yield scrapy.FormRequest(
            #     url='',
            #     meta={
            #         'oldUrl': "https://wallstreetcn.com" + div_item.xpath('./a[@class="news-item__main__title"]/@href').extract()[0],
            #         'title': div_item.xpath('./a[@class="news-item__main__title"]/text()').extract()[0],
            #         'desc': div_item.xpath('./a[@class="news-item__main__summary"]/text()').extract()[0]
            #     },
            #     method='GET',
            #     dont_filter=True,
            #     callback=self.prase_detail)

    def prase_detail(self, response):
        print response.meta['oldUrl']
        item = CnfolItem()
        item['url'] = response.meta['oldUrl']
        item['desc'] = response.meta['desc']
        item['title'] = response.meta['title']
        item['content'] = response.xpath('//div[@class="node-article-content"]/p/text()').extract()
        item['pushTime'] = response.xpath('//span[@class="meta-item__text"]/text()').extract()[0]
        return item

_jsonp_begin = r'callback('
_jsonp_end = r')'
#中金在线
logger = logging.getLogger("CnfolJsonSpider")

num = 2#每页100条

# 10位时间戳
timestamp =int(time.time())
# 13位时间错
millis = int(round(time.time() * 1000))
class CnfolJsonSpider(scrapy.Spider):
    def __init__(self):
        self.count = 0
    name = "cnfolJson"
    allowed_domains = ["app.cnfol.com/"]
    list = []
    page =1
    #for page in range(5, 6):
    start_urls = ['http://app.cnfol.com/qualityarticles/qualityarticles.php?CatId=101&starttime='+str(timestamp)+'&endtime='+str(timestamp)+'&num='+str(num)+'&page='+str(page)+'&record='+str(page)+'&jsoncallback=callback&_='+str(millis)]
        #list.append(url)
    #for lis in list:
        #start_urls = [lis,]
    print ('----orgin url------',start_urls)
    def parse(self, response):
        print('responseurl',response.url)
        self.count = self.count+1
        print('count',self.count)
        for page in range(2,4):
            init_url = 'http://app.cnfol.com/qualityarticles/qualityarticles.php?CatId=101&starttime='+str(timestamp)+'&endtime='+str(timestamp)+'&num='+str(num)+'&page='+str(page)+'&record='+str(page)+'&jsoncallback=callback&_='+str(millis)
            jsonp_str = response.body.strip()
            if not jsonp_str.startswith(_jsonp_begin) or \
                    not jsonp_str.endswith(_jsonp_end):
                raise ValueError('Invalid JSONP')
            strJsons = json.loads(jsonp_str[len(_jsonp_begin):-len(_jsonp_end)])
            strJsonss = strJsons['list']
            print ('-----strJsonss'+str(self.count)+'-----',strJsonss)
            for strJson in strJsonss:
                print ('title',strJson['Title'],'Url',strJson['Url'],'CreatedTime',strJson['CreatedTime'],'cateName',strJson['cateName'])
                yield scrapy.FormRequest(
                    url=strJson['Url'],
                    meta={
                        'title':strJson['Title'],
                        'url':strJson['Url'],
                        'pushTime':strJson['CreatedTime'],
                        'source':strJson['cateName']
                    },
                    dont_filter=True,
                    method='GET',
                    callback=self.prase_detail
                )
            yield scrapy.Request(init_url,callback=self.parse)
            print('---orgin url 1--', init_url)

    def prase_detail(self, response):
        print response.meta['url']
        item = WallStreetItem()
        item['url'] = response.meta['url']
        item['title'] = response.meta['title']
        item['source'] = response.meta['source']
        item['content'] = response.xpath('//div[@class="Article"]/text()').extract()
        item['pushTime'] = response.meta['pushTime']
        print item


    def closed(self,response):
        self.count
        # 获取logger实例，如果参数为空则返回root logger
        logger = logging.getLogger("AppName")

        # 指定logger输出格式
        formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
        # 控制台日志
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.formatter = formatter  # 也可以直接给formatter赋值

        # 文件日志
        file_handler = logging.FileHandler("test.log")
        file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式
        # 为logger添加的日志处理器
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        # 指定日志的最低输出级别，默认为WARN级别
        logger.setLevel(logging.INFO)

        # 输出不同级别的log
        logger.debug('this is debug info')
        logger.info('this is information')
        logger.warn('this is warning message')
        logger.error('this is error message')
        logger.fatal('this is fatal message, it is same as logger.critical')
        logger.critical('this is critical message')



        #jsonp 转化为json
        def parse_jsonp(jsonp_str):
            try:
                return re.search('^[^(]*?\((.*)\)[^)]*$', jsonp_str).group(1)
            except:
                raise ValueError('Invalid JSONP')

        #jsonp转化为json
        def loads_jsonp(_jsonp):
            try:
                return json.loads(re.match(".*?({.*}).*", _jsonp, re.S).group(1))
            except:
                raise ValueError('Invalid Input')

        def jsonp_to_json(self,json_str):
            j = json.loads(re.findall(r'^\w+\((.*)\)$', json_str)[0])
            return j
            #print(type(j),j)