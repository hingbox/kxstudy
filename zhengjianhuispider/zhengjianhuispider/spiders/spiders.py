#!/usr/bin/env python
# -*- coding:utf-8 -*-
#encoding=utf-8
'''
@描述：证券会
@作者：hingbox
@版本：V1.0
@文件名称 : spiders.py
@创建时间：2018/4/19 17:37
'''
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spider import CrawlSpider,Rule
from zhengjianhuispider.items import ZhengjianhuispiderItem
from zhengjianhuispider.items import YanghangspiderItem
from zhengjianhuispider.items import YingjianhuispiderItem
from zhengjianhuispider.items import TongjijuspiderItem
from zhengjianhuispider.items import CaizhengxinwenspiderItem
from zhengjianhuispider.items import TonghuashunspiderItem
from zhengjianhuispider.items import ZhongzhengredianspiderItem
from zhengjianhuispider.items import JinrongjiespiderItem
from zhengjianhuispider.logger import Logger
from scrapy import Spider,Request
import json
import sys
import time
import hashlib
import datetime
import re
reload(sys)
sys.setdefaultencoding('utf8')

#创建日志记录对象
log = Logger()
#证监会
class  zjhSpider(scrapy.Spider):
    name = "zhengjianhui"
    allowed_domains = ["csrc.gov.cn"]
    start_urls = []
    #这个urls是拼接的是证监会要闻 --start ----
    # for page in range(1,51):
    #     urls = 'http://www.csrc.gov.cn/pub/newsite/zjhxwfb/xwdd/index_'+str(page)+'.html'
    #     start_urls.append(urls)
    # log.info('start_urls %s',start_urls)
    #这个urls是拼接的是证监会要闻 --end ----

    #这个urls是拼接的是新闻发布会 --start ----
    # for page in range(1,13):
    #     urls = 'http://www.csrc.gov.cn/pub/newsite/zjhxwfb/xwfbh/index_'+str(page)+'.html'
    #     start_urls.append(urls)
    # log.info('start_urls %s',start_urls)
    #这个urls是拼接的新闻发布会 --end ----


    #这个urls是拼接的是时政要闻 这个暂时没用，因为解析格式不一样 --start ----
    # for page in range(1,2):
    #     urls = 'http://www.gov.cn/pushinfo/v150203/'
    #     start_urls.append(urls)
    #
    # log.info('start_urls %s',start_urls)
    #这个urls是拼接时政要闻 这个暂时没用，因为解析格式不一样 --end ----


    #
    def parse(self, response):
        lis = response.xpath('//div[@class="fl_list"]/ul/li')
        for li in lis:
            item = ZhengjianhuispiderItem()
            url = li.xpath('./a/@href').extract()[0]#得到url
            item['title'] = li.xpath('./a/text()').extract()[0]#得到a标签文字
            item['pubsh_time'] = li.xpath('./span/text()').extract()[0]#得到时间
            url_str = url[1:]
            url = "http://www.csrc.gov.cn/pub/newsite/zjhxwfb/xwfbh"+url_str
            log.info('parse---%s %s %s',url,item['title'],item['pubsh_time'])
            if url != None:  # 如果返回了新的url
                request = scrapy.Request(url, callback=self.parse_items)
                request.meta['item'] = item
                yield request
    def parse_items(self,response):
        item = response.meta['item']#获取未完成的item
        item['content'] = response.xpath('//div[@class="Custom_UnionStyle"]/p/span/text()').extract()
        item['source'] = response.xpath('//div[@class="time"]/span[3]/text()').extract()[0]
        item['url']=response.url
        yield item


#央行
class yhSpider(scrapy.Spider):
    name = "yanghang"
    allowed_domains = ["pbc.gov.cn"]
    start_urls = []
    #这个urls是拼接的是证监会要闻 --start ----
    for page in range(1,3):
        urls = 'http://www.pbc.gov.cn/goutongjiaoliu/113456/113469/11040/index'+str(page)+'.html'
        start_urls.append(urls)
    log.info('start_urls %s',start_urls)
    #这个urls是拼接的是证监会要闻 --end ----

    headers = {
      "Host": "www.pbc.gov.cn",
      "User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
      "Accept-Language":"zh-CN,zh;q=0.9",
      "Accept-Encoding":"gzip, deflate",
      "Referer": "http://www.pbc.gov.cn/goutongjiaoliu/113456/113469/11040/index1.html",
      "Cookie":"ccpassport=08c032c6158a6ae80a07b4bc9de384d2; wzwstemplate=MTA=; wzwsconfirm=bd48073f73d6c7fa9c511882cd40d146; wzwsvtime=1524195856; wzwschallenge=V1pXU19DT05GSVJNX1BSRUZJWF9MQUJFTDEwMTY3OTY1",
      "Connection":"keep-alive",
      "Upgrade-Insecure-Requests": "1"
    }

    def parse(self, response):
        yield Request(response.url,headers=self.headers,callback=self.parse_items)

    def parse_items(self,response):
        print ('response',response.body)








    #     with open('xx.html', 'wb') as f:
    #         f.write(response.body)
    #     print response.body
    #     t =response.xpath('//*[@id="11040"]/div[2]/div[1]')
    #     lis = response.xpath('//*[@id="11040"]/div[2]/div[1]/table/tbody/tr[2]/td/table[3]/tbody/tr/td[2]/font/a/text()')
    #     log.info('---a %s %s',lis,t)
    #     return
    #     for li in lis:
    #         item = YanghangspiderItem
    #         url = li.xpath('./a/@href').extract()[0]#得到url
    #         item['title'] = li.xpath('./a/text()').extract()[0]#得到a标签文字
    #         item['pubsh_time'] = li.xpath('./span/text()').extract()[0]#得到时间
    #         url_str = url[1:]
    #         url = "http://www.csrc.gov.cn/pub/newsite/zjhxwfb/xwfbh"+url_str
    #         log.info('parse---%s %s %s',url,item['title'],item['pubsh_time'])
    #         if url != None:  # 如果返回了新的url
    #             request = scrapy.Request(url, callback=self.parse_items)
    #             request.meta['item'] = item
    #             yield request
    # def parse_items(self,response):
    #     item = response.meta['item']#获取未完成的item
    #     item['content'] = response.xpath('//div[@class="Custom_UnionStyle"]/p/span/text()').extract()
    #     item['source'] = response.xpath('//div[@class="time"]/span[3]/text()').extract()[0]
    #     item['url']= response.url
    #     return item


#银监会
class  yjhSpider(scrapy.Spider):
    name = "yingjianhui"
    allowed_domains = ["cbrc.gov.cn"]
    start_urls = []
    #这个urls是拼接的是银监会最新新闻 --start ----
    for page in range(1,2):
        urls = 'http://www.cbrc.gov.cn/chinese/newListDoc/111002/'+str(page)+'.html'
        start_urls.append(urls)
    log.info('start_urls %s',start_urls)
    #这个urls是拼接的是银监会最新新闻 --end ----

    def parse(self, response):
        lis = response.xpath('//tr/td/a')
        for li in lis:
            item = YingjianhuispiderItem()
            url = li.xpath('./@href').extract()[0]#得到url
            item['title'] = li.xpath('./text()').extract()[0]#得到a标签文字
            #item['pubsh_time'] = li.xpath('./td[2]/text()').extract()[0]#得到时间
            url = "http://www.cbrc.gov.cn"+url
            #log.info('parse---%s %s %s',url,item['title'],item['pubsh_time'])
            if url != None:  # 如果返回了新的url
                request = scrapy.Request(url, callback=self.parse_items)
                request.meta['item'] = item
                yield request
    def parse_items(self,response):
        item = response.meta['item']#获取未完成的item
        item['content'] = response.xpath('//div[@class="Section0"]/p/span/text()').extract()#内容
        item['source'] = response.xpath('//div[@id="docTitle"]/div[@valign="top"]/text()').extract()[0]
        item['url'] = response.url
        log.info('-----%s %s %s',item['content'],item['source'],item['url'])
        return item


#统计局
class  tjjSpider(scrapy.Spider):
    name = "tongjiju"
    allowed_domains = ["stats.gov.cn"]
    start_urls = []
    #这个urls是拼接的是统计局最新新闻 --start ----
    for page in range(1,26):
        urls = 'http://www.stats.gov.cn/tjsj/zxfb/index_'+str(page)+'.html'
        start_urls.append(urls)
    log.info('start_urls %s',start_urls)
    #这个urls是拼接的是统计局最新新闻 --end ----

    def parse(self, response):
        lis = response.xpath('//ul[@class="center_list_contlist"]/li')
        for li in lis:
            item = TongjijuspiderItem()
            url = li.xpath('./a/@href')#得到url
            if url:
                url = li.xpath('./a/@href').extract()[0]
                #这个地方需要判断 url前面是否有"." 如果有 则要去掉，
                #url = url.replace('./','/')
                if re.match("\..*?",url):#判断首位是否是"."
                    url = url[1:]
                    str = "http://www.stats.gov.cn/tjsj/zxfb"+url
                else:
                    str = "http://www.stats.gov.cn"+url
                item['title'] = li.xpath('./a/span/font[@class="cont_tit03"]/text()').extract()[0]#得到a标签文字
                item['pubsh_time'] = li.xpath('./a/span/font[@class="cont_tit02"]/text()').extract()[0]#得到时间
                url = str
                log.info('parse---%s %s %s',url,item['title'],item['pubsh_time'])
                #if url != None:  # 如果返回了新的url
                request = scrapy.Request(url, callback=self.parse_items)
                request.meta['item'] = item
                yield request

    def parse_items(self,response):
        item = response.meta['item']#获取未完成的item
        content = response.xpath('//p[@class="MsoNormal"]/span/text()').extract()#内容
        #item['content'] = "".join(content.split())
        #item['content'] = content.replace('\n','')
        item['content']= self.pinjie_content(content)
        item['source'] = response.xpath('//font[@class="xilan_titf"]/font/font/text()').extract()[0]
        item['url'] = response.url
        log.info('-----parse_items %s %s %s',item['content'],item['source'],item['url'])
        yield item

    def pinjie_content(self,list):
        str=[]
        for i in list:
            i = i.strip().replace("\n","")
            str.append(i)
        return str



#外汇管理局
class whSpiders(scrapy.Spider):
    name = "waihuiju"
    allowed_domains = ["safe.gov.cn"]
    start_urls = []
    def parse(self,response):
        pass
    def parse_items(self,response):
        pass


#财政新闻
class czxwSpiders(scrapy.Spider):
    name = "caizhengxinwen"
    allowed_domains = ["mof.gov.cn"]
    start_urls = []
    for page in range(1, 47):
        url = 'http://www.mof.gov.cn/zhengwuxinxi/caizhengxinwen/index_'+str(page)+'.htm'
        start_urls.append(url)
    def parse(self, response):
        resp_items = response.xpath('//td[@class="ZITI"]')#得到所有的td
        for resp_item in resp_items:
            item = CaizhengxinwenspiderItem()
            url = resp_item.xpath('./a/@href').extract_first()#得到超链接
            #url='../../xinwenlianbo/yunnancaizhengxinxilianbo/201803/t20180329_2856656.htm'
            s = re.search("../../(.*)",url)
            if s:
                str= 'http://www.mof.gov.cn'+s.group(1)
            else:
                if re.match('\.(.*?)',url):
                    url = url[2:]
                    str = 'http://www.mof.gov.cn/zhengwuxinxi'+url
                else :
                   str = url
            item['title']= resp_item.xpath('./a/text()').extract_first()#得到超链接的title
            #temp='http://www.mof.gov.cn/xinwenlianbo/guangdongcaizhengxinxilianbo/201801/t20180104_2792894.htm'
            request = scrapy.Request(str,callback=self.parse_items)
            request.meta['item']=item
            yield request

    def parse_items(self, response):
        item = response.meta['item']
        teshu = response.xpath('//div[@class="TRS_Editor"]//td[@id="td_DocContent"]').extract_first()
        if teshu !=None:
            item['source']= response.xpath('//div[@class="TRS_Editor"]//td[@id="td_DocContent"]/p/text()').extract_first()
            item['source']= response.xpath('//div[@class="TRS_Editor"]//td[@id="td_DocContent"]/p/text()').extract()
        else:
            item['source']= response.xpath('//div[@class="TRS_Editor"]/p/text()').extract_first()#得到时间和来源
            item['content']= response.xpath('//div[@class="TRS_Editor"]/p/text()').extract()#得到内容
        item['url']= response.url
        return item




#同花顺
class thsSpiders(scrapy.Spider):
    name = "tonghuashun"
    #allowed_domains = ["stock.10jqka.com.cn"]
    start_urls = ['http://stock.10jqka.com.cn/stocknews_list/']
    # for page in range(1, 2):
    #     url = 'http://stock.10jqka.com.cn/stocknews_list/index_'+str(page)+'.shtml'
    #     start_urls.append(url)
    def parse(self, response):
        yield scrapy.Request(response.url,callback=self.parse_item)

    def parse_item(self,response):
        print ('response',response.body)

#中正热点网
class zzrdwSpiders(scrapy.Spider):
    name = "zhongzhengredian"
    allowed_domains = ["csstock.cn"]
    start_urls = []
    for page in range(1, 308):
        url = 'http://www.csstock.cn/cjyw?page='+str(page)
        start_urls.append(url)
    log.info('----start_url %s',start_urls)
    def parse(self, response):
        response_items = response.xpath('//div[@class="pd-mod-2"]/div[@class="pd-m-title"]')
        for response_item in response_items:
            item = ZhongzhengredianspiderItem()
            url = response_item.xpath('./a/@href').extract_first()
            url ='http://www.csstock.cn'+url
            item['title']= response_item.xpath('./a/text()').extract_first()
            item['url']=url
            request = scrapy.Request(url,callback=self.parse_item)
            request.meta['item']=item
            yield request

    def parse_item(self,response):
        item = response.meta['item']
        item['source']=response.xpath('//p[@class="f12 graycolor"]/text()').extract_first()
        item['content']= response.xpath('//div[@id="zw_bt"]/p/text()').extract()
        log.info('source %s conten %s url %s', item['source'],item['content'],response.url)
        return item

def dateRange(start, end, step=1, format="%Y-%m-%d"):
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    days = (strptime(end, format) - strptime(start, format)).days
    return [strftime(strptime(start, format) + datetime.timedelta(i), format) for i in xrange(0, days, step)]


#此处定义 是为了解决返回不规则的json
_jsonp_begin = r'var newsdata='
_jsonp_end = r';'

#金融界-7*24小时要闻  json
class jrjSpiders(scrapy.Spider):
    def __init__(self):
        self.count = 0
    name = "jinrongjie"
    #allowed_domains = ["finance.jrj.com.cn","stock.jrj.com.cn"]
    #得到财经频道下面 7*24新闻 宏观经济 国际财经 产经新闻 资本市场
    start_urls = []
    #start_urls = ['http://finance.jrj.com.cn/yaowen/','http://finance.jrj.com.cn/list/guoneicj.shtml','http://finance.jrj.com.cn/list/guojicj.shtml','http://finance.jrj.com.cn/list/industrynews.shtml','http://finance.jrj.com.cn/list/zbsc.shtml']

    for date in dateRange("2018-04-01","2018-04-23"):
        #date= datetime.date.today()#生成今天的日期
        url = 'http://stock.jrj.com.cn/share/news/yaowen/'+date+'.js?_=1524454389303'
        start_urls.append(url)
    log.info('----start_url %s',start_urls)
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
        strJsonss = strJsons['newsinfo']
        #print ('-----strJsonss'+str(self.count)+'-----',strJsonss)
        for strJson in strJsonss:
            self.count =self.count+1
            item = JinrongjiespiderItem()
            #print ('kk','infourl',strJson[0]['infourl'],'title',strJson[0]['title'],'source',strJson[0]['clsname'])
            url = strJson[0]['infourl']
            item['title']=strJson[0]['title']
            item['type']=strJson[0]['clsname']
            item['url']=url
            print ('---url ',self.count,url)
            request = scrapy.Request(url,callback=self.prase_detail)
            request.meta['item']=item
            yield request
            # yield scrapy.FormRequest(
            #     url=strJson[0]['infourl'],
            #     meta={
            #         'title':strJson[0]['title'],
            #         'url':strJson[0]['infourl'],
            #         'type':strJson[0]['clsname']
            #     },
            #     dont_filter=True,
            #     method='GET',
            #     callback=self.prase_detail
            # )
        #yield scrapy.Request(init_url,callback=self.parse)
        #print('---执行完回调--', init_url)

    def prase_detail(self, response):
        item = response.meta['item']
        item['content'] = response.xpath('//div[@class="texttit_m1"]/p/text()').extract()
        item['pubsh_time'] = response.xpath('//p[@class="inftop"]/span[1]/text()').extract_first()
        item['source'] = response.xpath('//p[@class="inftop"]/span[2]/text()').extract()
        return item

#金融界 国内财经；国际财经；产经新闻；资本市场
class jrjgnSpiders(scrapy.Spider):
    def __init__(self):
        self.count = 0
    name = "jinrongjiegn"
    start_urls=[]
    #allowed_domains = ["finance.jrj.com.cn"]
    #得到财经频道下面 宏观经济 国际财经 产经新闻 资本市场
    #start_urls = ['http://finance.jrj.com.cn/list/guoneicj.shtml']
    #start_urls = ['http://finance.jrj.com.cn/yaowen/','http://finance.jrj.com.cn/list/guoneicj.shtml','http://finance.jrj.com.cn/list/guojicj.shtml','http://finance.jrj.com.cn/list/industrynews.shtml','http://finance.jrj.com.cn/list/zbsc.shtml']

    for page in range(1,11):
        #url = 'http://finance.jrj.com.cn/list/guoneicj-'+str(page)+'.shtml'#国内财经
        #url = 'http://finance.jrj.com.cn/list/guojicj-'+str(page)+'.shtml'#国际财经
        #url ='http://finance.jrj.com.cn/list/industrynews-'+str(page)+'.shtml'#产经新闻
        url = 'http://finance.jrj.com.cn/list/zbsc-'+str(page)+'.shtml'#资本市场
        start_urls.append(url)
    log.info('----start_url %s',start_urls)
    def parse(self, response):
        response_items = response.xpath('//ul[@class="ullab"]/li')
        if response_items:
            for response_item in response_items:
                item = JinrongjiespiderItem()
                url = response_item.xpath('./label/a/@href').extract_first()
                item['title'] = response_item.xpath('./label/a/text()').extract_first()
                #item['pubsh_time'] = response_item.xpath('./i/text()').extract_first()
                item['url']=url
                item['type']='资本市场'#这个地方修改 国内财经；国际财经;产经新闻；资本市场
                #print('url->{}--title{}'.format(url,item['title']))
                if url !=None:
                    request = scrapy.Request(url,callback=self.parse_items)
                    request.meta['item']=item
                    yield request

        else:
            response_items = response.xpath('//ul[@class="list2"]/li')
            for response_item in response_items:
                item = JinrongjiespiderItem()
                url = response_item.xpath('./a/@href').extract_first()
                item['title'] = response_item.xpath('./a/text()').extract_first()
                #item['pubsh_time'] = response_item.xpath('./i/text()').extract_first()
                item['url']=url
                item['type']='资本市场'#这个地方修改 国内财经；国际财经;产经新闻；资本市场
                #print('url->{}--title{}'.format(url,item['title']))
                if url !=None:
                    request = scrapy.Request(url,callback=self.parse_item)
                    request.meta['item']=item
                    yield request


    def parse_items(self, response):
        item = response.meta['item']
        item['content'] = response.xpath('//div[@id="IDNewsDtail"]/p/text()').extract()
        item['pubsh_time'] = response.xpath('//p[@class="newsource"]/span[1]/text()').extract_first()
        sources = response.xpath('//p[@class="newsource"]/span[2]/text()').extract()
        item['source']=sources[1]
        #print('--content{},pubsh_time{},source{}'.format(item['content'],item['pubsh_time'],item['source']))
        return item

    def parse_item(self, response):
        item = response.meta['item']
        item['content'] = response.xpath('//div[@id="texttit_m1"]/p/text()').extract()
        item['pubsh_time'] = response.xpath('//p[@class="inftop"]/span[1]/text()').extract_first()
        sources = response.xpath('//p[@class="inftop"]/span[2]/text()').extract()
        item['source']=sources[1]
        #print('--content{},pubsh_time{},source{}'.format(item['content'],item['pubsh_time'],item['source']))
        return item