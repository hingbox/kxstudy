# kxstudy
这是一个采集数据的demo
CrawlSpider
爬取的步骤 ：
    1.需要爬取的内容 定义一个对象item ,这个对象中添加属性，存入管道文件
    2.需要爬取的url地址，建立spider进行采集，这个是主要文件，
        格式如下：
        首先定义一个name 爬虫的名字name="test"
        allowed_domains=["test.com"]#要爬取的内容
        start_urls=["http://www.test.com"]#第一次爬取要用的地址
        rules = (
                 Rule(LinkExtractor(allow=r'type=4&page=\d+'),follow=True),
                 Rule(LinkExtractor(allow=r'/html/question/\d+/\d+.shtml'), callback='parsedongguan'),
                )

         def deal_links(self,links):
        for link in links:
            link.url = link.url.replace("?","&").replace("Type&","Type?")
            #print link.url
        #返回 修改完的links链接列表
        return links

    def parsedongguan(self, response):
        print(response.url)

        item = DongGuanItem()
        item['title'] = response.xpath('//div[@class="pagecenter p3"]//strong/text()').extract()[0]
        item['num'] = item['title'].split(' ')[-1].split(":")[-1]
        item['content'] = response.xpath('//div[@class="c1 text14_2"]/text()').extract()[0]
        item['url'] = response.url
        yield item
    3.定义管道文件存储内容
        def __init__(self):
        #下面两个都可以
        #创建一个文件
        #self.filename = codecs.open("dongguan.json","w",encoding="utf-8")
        self.filename = open('dongguan.json','w')

        def process_item(self,item,spider):
            #中文默认使用ascii码来存储，禁用后默认为unicode字符串  encode 把unicode转换为指定的编码格式
            text = json.dumps(dict(item),ensure_ascii=False)+",\n"
            self.filename.write(text.encode("utf-8"))
            return item

        def close_spider(self,spider):
            self.filename.close()
        4.设置管道文件 setting.py
            # 设置处理返回数据的类及执行优先级
            ITEM_PIPELINES = {
                #'study.pipelines.StudyPipeline': 100,
               # 'study.pipelines.XiaoHuaPipeline': 100,
                'study.pipelines.DongGuanPipeline':99,
            }
主要使用了CrawlSpider
    from scrapy.linkextractors import LinkExtractor#主要是提取链接
    from scrapy.spider import CrawlSpider,Rule#提取规则
    使用提取

#可以打印日志到文件
    在setting.py中设置
    LOG_FILE ="dongguan.log"
    保存日志级别，低于或等于此等级的信息都会被保存下来
    LOG_LEVEL = "DEBUG"
    几种错误的级别  CRITICAL(严重错误),ERROR(错误),WARNING(警告),INFO(一般信息),DEBUG(调试信息)


#将list转换为string类型
list= ['aaaaaaaaaa','bbbbbbbbbbb',ccccccccccccc]
string = "".join(list)
去掉首位的空白字符  string.strip()
如果要替换内容 string.replace("a","b") 将字符串中的a替换为b
去掉左边空白字符  string.lstrip()
去掉右边空白字符  string.rstrip()



#Spider



#通常防止爬虫被反主要有几种策略
1.动态设置User-Agent（随机切换User-Agent，模拟不同用户浏览器信息）
2.禁用Cookies（也就是不启用cookies middleware,不想server发送cookies，有些网站通过cookie的使用发现爬虫行为）
    可以通过COOKIES_ENABLED控制CookiesMiddleware开启或关闭
3.设置延迟下载(防止访问过于频繁，设置为2秒或者更高)
4.Google Cache和Baidu Cache：如果可能的话，使用谷歌/百度等搜索引擎服务器页面缓存页面数据
5.使用IP地址池:VPN和代理IP,现在大部分网站都是根据IP来ban的
5.使用Crawlear（专用于爬虫的代理软件）,正确配置和设置下载中间件后，项目所有的request都是通过crawlear发出
    DOWNLOADER_MIDDLEWARES={
    scrapy_crawlera.CrawleraMiddleware'=600
    }






