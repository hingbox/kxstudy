# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.conf import settings
from study.testitems import SouGouItem

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
}
class Topsougou_Spider(scrapy.Spider):
    name = 'sougou'
    def start_requests(self):
        reqs = []
        # 综艺
        for i in range(1, 4):
            url = 'http://v.sogou.com/tvshow/list/page-' + str(i) + '.html'
            req = scrapy.Request(url=url, headers=headers)
            reqs.append(req)
        # 电影
        for i in range(1, 4):
            url = 'http://v.sogou.com/film/list/page-' + str(i) + '.html'
            req = scrapy.Request(url=url, headers=headers)
            reqs.append(req)
        # 电视剧
        for i in range(1, 4):
            url = 'http://v.sogou.com/teleplay/list/page-' + str(i) + '.html'
            req = scrapy.Request(url=url, headers=headers)
            reqs.append(req)
        # 动漫
        for i in range(1, 4):
            url = 'http://v.sogou.com/cartoon/list/page-' + str(i) + '.html'
            req = scrapy.Request(url=url, headers=headers)
            reqs.append(req)
        return reqs

    def parse(self, response):
        item = SouGouItem()
        url = response.url
        print ('sougou', url)

class TopsougouOther_Spider(scrapy.Spider):
    name = 'sougou1'
    def start_requests(self):
        reqs = []
        # 综艺
        for i in range(5, 8):
            url = 'http://v.sogou.com/tvshow/list/page-' + str(i) + '.html'
            req = scrapy.Request(url=url, headers=headers)
            reqs.append(req)
        # 电影
        for i in range(5, 8):
            url = 'http://v.sogou.com/film/list/page-' + str(i) + '.html'
            req = scrapy.Request(url=url, headers=headers)
            reqs.append(req)
        # 电视剧
        for i in range(5, 8):
            url = 'http://v.sogou.com/teleplay/list/page-' + str(i) + '.html'
            req = scrapy.Request(url=url, headers=headers)
            reqs.append(req)
        # 动漫
        for i in range(5, 8):
            url = 'http://v.sogou.com/cartoon/list/page-' + str(i) + '.html'
            req = scrapy.Request(url=url, headers=headers)
            reqs.append(req)
        return reqs

    def parse(self, response):
        item = SouGouItem()
        url = response.url
        print ('sougou1',url)


#process = CrawlerProcess()
#process.crawl(Topsougou_Spider)
#process.crawl(TopsougouOther_Spider)
#process.start() # the script will block here until all crawling jobs are finished