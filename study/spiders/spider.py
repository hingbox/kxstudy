# -*- coding: utf-8 -*-
import scrapy
from study.items import MeiJuItem
from study.items import XiaoHuaItem
from study.items import DongGuanItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spider import CrawlSpider,Rule
from study.items import KuaiDaiLiItem
from study.items import PatentItem
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



#模拟登陆 首先发送登陆页面的get请求，获取到页面里的登录必须参数
#然后账户密码 一起post到服务器 登录成功
class RenRen1Spider(Spider):
    name ="renren1"
    allowed_domains = ["renren.com"]
    start_urls =('http://www.renren.com/PLogin.do',)

    def parse(self,response):
        yield scrapy.FormRequest.form_response(
            response,
            formdata={},
            callback=self.parse_page
        )
    def parse_page(self,response):
        print "==========1=========="+response.url


#只要是需要提供post数据，可以用这种方法
class RenRen2Spider(Spider):
    name = "renren1"
    allowed_domains = ["renren.com"]
    #start_urls = ('http://www.renren.com',)
    def start_requests(self):
        url = 'http://www.renren.com/PLogin.do'
        yield scrapy.FormRequest(
            url=url,
            formdata={"email":"mr_mao_hacker@163.com","password":"alarmchime"},
            callback=self.parse_page
        )
    def parse_page(self,response):
        with open('hao.html','w')as filename:
            filename.write(response.body)



from study.items import DouBanItem
#豆瓣网电影top250
class DouBanSpider(Spider):
    name = "douban"
    allowed_domains = ["douban.com"]
    offset = 0
    url = "https://movie.douban.com/top250?start="+str(offset)
    start_urls = (url,)

    def parse(self,response):
        '''
        item = DouBanItem()
        movies = response.xpath('//div[@class="info"]')
        for each in movies:
            #标题
             item['title'] = each.xpath('.//span[@class="title"][1]/text()').extract()
            #信息
             item['bd'] = each.xpath('.//div[@class="bd"]/p/text()').extract()
            #频分
             item['star'] = each.xpath('.//div[@class="star"]/span[@class="rating_num"]/text()').extract()
            #介绍
             quote = each.xpath('.//p[@class="quote"]/span/text()').extract()
             if len(quote) !=0:
              item['quote']= quote[0]
             yield item
            '''
        if self.offset <= 225:
            self.offset += 25
            yield scrapy.Request(self.url+str(self.offset),callback=self.parse)


class KuaiDaiLiSpider(Spider):
    name = "kuaidaili"
    allowed_domains = ["kuaidaili.com"]
    offset=0
    url = "http://www.kuaidaili.com/free/inha/"+str(offset)
    start_urls =(url,)

    def parse(self, response):
        item = KuaiDaiLiItem()
        dailis = response.xpath('//tbody/tr')
        for each in dailis:
                item['ip'] = each.xpath('./td/text()').extract()[0]
                item['port'] = each.xpath('./td/text()').extract()[1]
                item['position'] = each.xpath('./td/text()').extract()[4]
                yield item
        if self.offset <= 10:
            self.offset += 1
            yield Request(self.url+str(self.offset),callback=self.parse)



#采集专利信息
class PatentSpider(Spider):
      name = "patent"
      allowed_domains = ["soopat.com"]
      start_urls = ("http://www.soopat.com/IPC/Index",)
      def parse(self,response):
          item = PatentItem()
          hrefs = response.xpath('//ul[@class="body"]/li/a/@href')
          for href in hrefs:
              item['href'] = "http://www.soopat.com"+href.extract()
              #yield item

            #yield Request(item,callback=self.parse);

              #hrefs = each.xpath('./@href').extract()
              #for  href in hrefs:#得到首页链接
                 # print "http://www.soopat.com"+href
         # item['href'] = "http://www.soopat.com"+hrefs
          #yield item