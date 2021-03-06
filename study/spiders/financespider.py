# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spider import CrawlSpider,Rule
from study.items import PatentItem
from study.financeitems import YiCaiFinanceItem
from study.financeitems import SinaFinanceItem
from study.financeitems import WallStreetItem
from study.financeitems import CnfolItem
from study.financeitems import HeXunItem
#导入封装的日志记录模块
from study.logger import Logger
from scrapy import Spider,Request
import json
import sys
import time
import re
reload(sys)
sys.setdefaultencoding('utf8')

#新浪财经
_json_begin = r'var all_1_data = '
_json_end = r';'
class SinaFinanceSpider(scrapy.Spider):
    name = "sinaFinance"
    allowed_domains = ["finance.sina.com.cn/"]
    top_time = "20180404"#日期
    top_show_num = 100#每页显示1000条
    start_urls = ['http://top.finance.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=finance_0_suda&top_time='+top_time+'&top_show_num='+str(top_show_num)+'&top_order=DESC&js_var=all_1_data&get_new=1']
    # for page in range(1,2):
    #     urls = 'http://finance.sina.com.cn/topnews/#'+str(page)
    #     start_urls.append(urls)
    #     print ('start_urls',start_urls)
    def parse(self, response):
        items = SinaFinanceItem()
        jsonp_str = response.body.strip()
        if not jsonp_str.startswith(_json_begin) or \
                not jsonp_str.endswith(_json_end):
            raise ValueError('Invalid JSONP')
        strJsons = json.loads(jsonp_str[len(_json_begin):-len(_json_end)])['data']
        print('strJsons',strJsons)
        for strJson in strJsons:
            # items['url'] = strJson['url']
            # items['title'] = strJson['title']
            # items['pushTime'] = strJson['time']
            #print ('url',strJson['url'])
            yield scrapy.FormRequest(
                url=strJson['url'],
                method='GET',
                #meta={'items': items},
                meta={
                    'url':strJson['url'],
                    'title':strJson['title'],
                    'pushTime':strJson['time']
                },
                dont_filter=True,
                callback=self.parse_detail
            )

    def parse_detail(self,response):
        item = SinaFinanceItem()
        item['url'] = response.meta['url']
        item['title'] = response.meta['title']
        item['pushTime'] = response.meta['pushTime']
        item['content'] = response.xpath('//div[@class="article"]/p/text()').extract()
        yield item
        #item = SinaFinanceItem()

        #print item


#第一财经
class yiCaiFinanceSpider(scrapy.Spider):
    name = "yiCaiFinance"
    allowed_domains = ["www.yicai.com/"]
    start_urls = []
    for page in range(1,5):
        pages = page*3+1
        urls = 'http://www.yicai.com/api/ajax/NsList/'+str(page)+'/77'
        start_urls.append(urls)
        print('start_urls',urls)
    def parse(self, response):
        dlItems = response.xpath('//div[@class="m-list8"]/dl')
        for dl in dlItems:
            item = YiCaiFinanceItem()
            url = dl.xpath('./dd/h3/a/@href').extract()[0]
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


    # def nextRequest(self,response):
    #     print '进来了'
    #     yield scrapy.FormRequest(url='http://www.yicai.com/api/ajax/NsList/6/77',
    #                              method='POST',
    #                              formdata={
    #                                  'news_List': "news_List"
    #                              },
    #                              dont_filter=True,
    #                              callback=self.parse
    #                              )



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
    cursor = "1522598400,1522512000"
    page = 100
    #for page in range(1,3):
    start_urls = ['https://api-prod.wallstreetcn.com/apiv1/content/articles?category=global&limit='+str(page)+'&cursor='+str(cursor)+'&platform=wscn-platform']
    #start_urls = ['https://api-prod.wallstreetcn.com/apiv1/content/articles?platform=wscn-platform&category=us&limit='+str(page)]
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
        #item['pushTime'] = response.xpath('//span[@class="meta-item__text"]/text()').extract()[0]
        yield item


#中金在线(解析页面元素,得到数据,并入库)
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

#此处定义 是为了解决返回的是jsonp
_jsonp_begin = r'callback('
_jsonp_end = r')'
#中金在线(解析jsonp,得到数据,并入库)
class CnfolJsonSpider(scrapy.Spider):
    #logging.basicConfig(level=logging.DEBUG,
                       # format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')  # logging.basicConfig函数对日志的输出格式及方式做相关配置
    def __init__(self):
        self.count = 0
    name = "cnfolJson"
    allowed_domains = ["app.cnfol.com/"]

    num = 50  # 每页50条

    # 10位时间戳
    timestamp = int(time.time())
    # 13位时间错
    millis = int(round(time.time() * 1000))
    start_urls = []
    for page in range(51, 71):#已执行
        for record in range(1,5):
            urls = 'http://app.cnfol.com/qualityarticles/qualityarticles.php?CatId=101&starttime='+str(timestamp)+'&endtime='+str(timestamp)+'&num='+str(num)+'&page='+str(page)+'&record='+str(record)+'&jsoncallback=callback&_='+str(millis)
    #start_urls = ['http://app.cnfol.com/qualityarticles/qualityarticles.php?CatId=101&starttime=1523151906&endtime=1523151906&num=2&page=1&record=1&jsoncallback=callback&=1523151906782']
            start_urls.append(urls)
    #for lis in list:
        #start_urls = [lis,]
            print ('----orgin url------',start_urls)
    def parse(self, response):
        print('responseurl',response.url)
        self.count = self.count+1
        print('count',self.count)
        #for page in range(2,4):
           # init_url = 'http://app.cnfol.com/qualityarticles/qualityarticles.php?CatId=101&starttime='+str(timestamp)+'&endtime='+str(timestamp)+'&num='+str(num)+'&page='+str(page)+'&record='+str(page)+'&jsoncallback=callback&_='+str(millis)
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
        #yield scrapy.Request(init_url,callback=self.parse)
        #print('---执行完回调--', init_url)

    def prase_detail(self, response):
        print response.meta['url']
        item = WallStreetItem()
        item['url'] = response.meta['url']
        item['title'] = response.meta['title']
        item['source'] = response.meta['source']
        item['content'] = response.xpath('//div[@class="Article"]/text()').extract()
        item['pushTime'] = response.meta['pushTime']
        yield item


    def closed(self,response):
        # self.count
        # # 获取logger实例，如果参数为空则返回root logger
        # logger = logging.getLogger("cnfolJson")
        #
        # # 指定logger输出格式
        # formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s -%(filename)s ')
        # # 控制台日志
        # console_handler = logging.StreamHandler(sys.stdout)
        # console_handler.formatter = formatter  # 也可以直接给formatter赋值
        #
        # # 文件日志
        # file_handler = logging.FileHandler("test.log")
        # file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式
        # # 为logger添加的日志处理器
        # logger.addHandler(file_handler)
        # logger.addHandler(console_handler)
        #
        # # 指定日志的最低输出级别，默认为WARN级别
        # logger.setLevel(logging.INFO)

        # 输出不同级别的log
        # logger.debug('this is debug info')
        # logger.info('this is information')
        # logger.warn('this is warning message')
        # logger.error('this is error message')
        # logger.fatal('this is fatal message, it is same as logger.critical')
        # logger.critical('this is critical message')



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



    def getlog(self):
        return self.logger
#和讯网(解析页面元素,得到数据,并入库)

 #创建日志记录对象
log = Logger()
class HeXunSpider(scrapy.Spider):
    name = "hexun"
    allowed_domains = ["news.hexun.com"]
    start_urls = ['http://news.hexun.com/']
    def parse(self, response):
        #获取首页上的标签  新闻/事实;股票/7*24小时快讯;
        div_items = response.xpath('//*[starts-with(@class,"c1")]/div[@class="newsTop"]')
        log.info('----%s',div_items)
        # for div_item in div_items:
        #     link = div_item.xpath('./li/a[1]/@href').extract()[0]
        #     title = div_item.xpath('./li/a[1]/text()').extract()[0]
        #     print ('------link----',link,'-----title------ ',title)
        #     #print url
        #     yield scrapy.FormRequest(
        #         url=link,
        #         meta={
        #             'url': link,
        #             'title': title
        #         },
        #         method='GET',
        #         dont_filter=True,
        #         callback=self.prase_detail
        #     )

    def prase_detail(self, response):
        item = HeXunItem()
        item['url'] = response.meta['url']
        item['title'] = response.meta['title']
        item['content'] = response.xpath('//div[@class="art_context"]/div[@class="art_contextBox"]/p/text()').extract()
        #item['pushTime'] = response.xpath('//div[@class="clearfix"]/div[@class="tip fl"]/span[@class="pr20"]/text()').extract()[0]
        return item

# class HeXunSpider(scrapy.Spider):
#     name = "hexun"
#     allowed_domains = ["news.hexun.com"]
#     start_urls = ['http://news.hexun.com/']
#     def parse(self, response):
#         #从左边开始匹配
#         div_items = response.xpath('//*[starts-with(@class,"m_news")]/ul')
#         for div_item in div_items:
#             link = div_item.xpath('./li/a[1]/@href').extract()[0]
#             title = div_item.xpath('./li/a[1]/text()').extract()[0]
#             print ('------link----',link,'-----title------ ',title)
#             #print url
#             yield scrapy.FormRequest(
#                 url=link,
#                 meta={
#                     'url': link,
#                     'title': title
#                 },
#                 method='GET',
#                 dont_filter=True,
#                 callback=self.prase_detail
#             )
#
#     def prase_detail(self, response):
#         item = HeXunItem()
#         item['url'] = response.meta['url']
#         item['title'] = response.meta['title']
#         item['content'] = response.xpath('//div[@class="art_context"]/div[@class="art_contextBox"]/p/text()').extract()
#         #item['pushTime'] = response.xpath('//div[@class="clearfix"]/div[@class="tip fl"]/span[@class="pr20"]/text()').extract()[0]
#         return item