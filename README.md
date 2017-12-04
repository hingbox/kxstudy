# kxstudy
这是一个采集数据的demo

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








