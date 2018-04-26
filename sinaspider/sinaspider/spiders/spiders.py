#!/usr/bin/env python
# -*- coding:utf-8 -*-
#encoding=utf-8
'''
@描述：新浪新闻
@作者：hingbox
@邮箱：hingbox@163.com
@版本：V1.0
@文件名称 : spiders.py
@创建时间：2018/4/25 21:21
'''
import scrapy
import json
from sinaspider.items import SinaspiderItem
import time
from sinaspider.dateutils import DateUtils
from sinaspider.SinaNewsspiderPipeline import MysqldemospiderPipeline
#此处定义 是为了解决返回不规则的json
_jsonp_begin = r'try{jQuery31101310337504093675_1524665582034('
_jsonp_end = r');}catch(e){};'
class SinaNewsSpider(scrapy.Spider):
    name="sinanews"
    start_urls=['http://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&k=&num=50&page=2&r=0.5262880694647982&callback=jQuery31101310337504093675_1524665582034&_=1524665582035']
    def parse(self,response):
        jsonp_str = response.body.strip()
        if not jsonp_str.startswith(_jsonp_begin) or \
                not jsonp_str.endswith(_jsonp_end):
            raise ValueError('Invalid JSONP')
        strJsons = json.loads(jsonp_str[len(_jsonp_begin):-len(_jsonp_end)])
        data = strJsons['result']['data']
        for d in data:
            item = SinaspiderItem()
            item['pubdate']=d['ctime']
            item['title']=d['title']#标题
            url = d['url']#url
            item['orgurl']=url
            item['source']=d['media_name']#来源
            item['summary']=d['summary']#
            item['type']='1'
            item['writer']=d['author']
            print ('strJsons', d['title'],d['url'],d['media_name'],d['ctime'])
            request =scrapy.Request(url,callback=self.parse_item)
            request.meta['item']=item
            yield request
    def parse_item(self,response):
        item = response.meta['item']
        content= response.xpath('//div[@id="artibody"]/p/text()').extract()
        item['content']="".join(content)
        yield item
        #strJsonss = strJsons['newsinfo']
    #start_urls=['http://news.sina.com.cn/roll/#pageid=153&lid=2509&k=&num=50&page=1']
    # def parse(self,response):
    #     resp_items = response.xpath('//div[@class="d_list_txt"]/ul/li')
    #     for resp_item in resp_items:
    #         item = SinaspiderItem()
    #         item['summary']= resp_item.xpath('./span[@class="c_chl"]/text()').extract_first()
    #         item['title']= resp_item.xpath('./span[@class="c_tit"]/a/text()').extract_first()
    #         orgurl = resp_item.xpath('./span[@class="c_tit"]/a/@href').extract_first()
    #         item['pubdate']= resp_item.xpath('./span[@class="c_time"]/text()').extract_first()
    #         item['orgurl']= orgurl
    #         request = scrapy.Request(orgurl,callback=self.parse_item)
    #         request.meta['item']= item
    #         yield request
    #
    # def parse_item(self,response):
    #     item = response.meta['item']
    #     item['content']=response.xpath('//div[@id="artibody"]/p/text()').extract()
    #     item['source']=response.xpath('//div[@class="date-source"]/a/text()').extract_first()
    #     return item


class SinaNewSpider(scrapy.Spider):
    name="test"
    #start_urls=['http://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&k=&num=50&page=2&r=0.5262880694647982&callback=jQuery31101310337504093675_1524665582034&_=1524665582035']

    def start_requests(self):
        pages=[]
        for i in range(10,1176):
            #url='http://www.example.com/?page=%s'%i
            url='http://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&k=&num=50&page='+str(i)+'&r=0.5262880694647982&callback=jQuery31101310337504093675_1524665582034&_=1524665582035'
            page=scrapy.Request(url)
            pages.append(page)
        return pages
        print pages

    def parse(self,response):
        jsonp_str = response.body.strip()
        if not jsonp_str.startswith(_jsonp_begin) or \
                not jsonp_str.endswith(_jsonp_end):
            raise ValueError('Invalid JSONP')
        strJsons = json.loads(jsonp_str[len(_jsonp_begin):-len(_jsonp_end)])
        data = strJsons['result']['data']
        for d in data:
            item = SinaspiderItem()

            # unicodestring = u"Hello world"
            # # 将Unicode转化为普通Python字符串："encode"
            # utf8string = unicodestring.encode("utf-8")
            # asciistring = unicodestring.encode("ascii")
            # isostring = unicodestring.encode("ISO-8859-1")
            # utf16string = unicodestring.encode("utf-16")
            # # 将普通Python字符串转化为Unicode："decode"
            # plainstring1 = unicode(utf8string, "utf-8")
            # plainstring2 = unicode(asciistring, "ascii")
            # plainstring3 = unicode(isostring, "ISO-8859-1")
            # plainstring4 = unicode(utf16string, "utf-16")
            # assert plainstring1 == plainstring2 == plainstring3 == plainstring4
            item['title']=d['title']#标题
            item['type']=None#暂无类型
            item['writer']=d['author']#作者
            item['source']=d['media_name']#来源
            url = d['url']#url
            item['orgurl']=url#原始url
            item['summary']=d['summary']#摘要
             # 将Unicode转化为普通Python字符串："encode"
            utf8string = d['ctime'].encode("utf-8")
            # print type(utf8string)
            # print utf8string
            #item['pubdate']= self.timestamp_to_date(float(utf8string))
            timeArray = time.localtime(float(utf8string))
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)#将时间戳转换为日期格式
            item['pubdate'] =otherStyleTime#发布日期

            #print ('strJsons', d['title'],d['url'],d['media_name'],d['ctime'])
            request =scrapy.Request(url,callback=self.parse_item)
            request.meta['item']=item
            yield request
    def parse_item(self,response):
        item = response.meta['item']
        #item['content']=None
        #返回一个列表，做判断，如果不为空，将list转换为string,如果为空，则直接复制None
        content= response.xpath('//div[@id="artibody"]/p/text()').extract()
        if content:
            #utf8string = str(content).encode("utf-8")
            #item['content']=str(utf8string)
            item['content']="".join(content)
        else:
            content = response.xpath('//div[@id="article"]/p/text()').extract()
            item['content'] ="".json(content)
        yield item
    # name="test"
    # start_urls = ['https://www.baidu.com/']
    # def parse(self, response):
    #     res_items = response.xpath('//a')
    #     for res_item in res_items:
    #         item = SinaspiderItem()
    #         item['orgurl'] = res_item.xpath('./@href').extract_first()
    #         item['title'] = res_item.xpath('./text()').extract_first()
    #         item['content']=None
    #         yield  item

class other(scrapy.Spider):
    name="other"
    def start_requests(self):
        pages=[]
        for i in range(1,10):
            #url='http://www.example.com/?page=%s'%i
            url='http://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&k=&num=50&page='+str(i)+'&r=0.5262880694647982&callback=jQuery31101310337504093675_1524665582034&_=1524665582035'
            page=scrapy.Request(url)
            pages.append(page)
        return pages
        print pages

    def parse(self, response):
        jsonp_str = response.body.strip()
        if not jsonp_str.startswith(_jsonp_begin) or \
                not jsonp_str.endswith(_jsonp_end):
            raise ValueError('Invalid JSONP')
        strJsons = json.loads(jsonp_str[len(_jsonp_begin):-len(_jsonp_end)])
        data = strJsons['result']['data']
        for d in data:
            item = SinaspiderItem()

            # unicodestring = u"Hello world"
            # # 将Unicode转化为普通Python字符串："encode"
            # utf8string = unicodestring.encode("utf-8")
            # asciistring = unicodestring.encode("ascii")
            # isostring = unicodestring.encode("ISO-8859-1")
            # utf16string = unicodestring.encode("utf-16")
            # # 将普通Python字符串转化为Unicode："decode"
            # plainstring1 = unicode(utf8string, "utf-8")
            # plainstring2 = unicode(asciistring, "ascii")
            # plainstring3 = unicode(isostring, "ISO-8859-1")
            # plainstring4 = unicode(utf16string, "utf-16")
            # assert plainstring1 == plainstring2 == plainstring3 == plainstring4
            item['title']=d['title']#标题
            item['type']=None
            item['writer']=d['author']
            item['source']=d['media_name']#来源
            url = d['url']#url
            item['orgurl']=url
            item['summary']=d['summary']
             # 将Unicode转化为普通Python字符串："encode"
            utf8string = d['ctime'].encode("utf-8")
            # print type(utf8string)
            # print utf8string
            #item['pubdate']= self.timestamp_to_date(float(utf8string))
            timeArray = time.localtime(float(utf8string))
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            item['pubdate'] =otherStyleTime
            now_time =DateUtils()
            now_date = now_time.get_now_time()
            item['create_date']= now_date#记录创建时间
            item['recorddate']=now_date#记录日期就是创建时间

            #print ('strJsons', d['title'],d['url'],d['media_name'],d['ctime'])
            request =scrapy.Request(url,callback=self.parse_item)
            request.meta['item']=item
            yield request
    def parse_item(self,response):
        item = response.meta['item']
        #item['content']=None
        content= response.xpath('//div[@id="artibody"]/p/text()').extract()
        if content:
            #utf8string = str(content).encode("utf-8")
            #item['content']=str(utf8string)
            item['content']="".join(content)
        else:
            item['content']=None
        yield item