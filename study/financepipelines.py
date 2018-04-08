# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import urllib2
import os
import json
import pymongo
import MySQLdb
from scrapy.conf import settings
#新浪财经
class SinaFinancePipeline(object):
    # def __init__(self):
    #     #下面两个都可以
    #     #创建一个文件
    #     #self.filename = codecs.open("dongguan.json","w",encoding="utf-8")
    #     self.filename = open('kuaidaili.json','w')
    #
    # def process_item(self,item,spider):
    #     #中文默认使用ascii码来存储，禁用后默认为unicode字符串  encode 把unicode转换为指定的编码格式
    #     text = json.dumps(dict(item),ensure_ascii=False)+",\n"
    #     self.filename.write(text.encode("utf-8"))
    #     return item
    #
    # def close_spider(self,spider):
    #     self.filename.close()
     def __init__(self):
        host = settings['FINANCE_MONGODB_SERVER']
        port = settings['FINANCE_MONGODB_PORT']
        #创建mongodb数据库连接
        client = pymongo.MongoClient(host=host, port=port)
        dbName = settings['FINANCE_MONGODB_DB']
        #指定数据库
        tdb = client[dbName]
        #存放数据的数据表名
        self.post = tdb[settings['FINANCE_MONGODB_SINAFINANCE_COLLECTION']]

     def process_item(self, item, spider):
        sinafinance = dict(item)
        self.post.insert(sinafinance)
        return item


#第一财经
class YiCaiFinancePipeline(object):
    #mongodb
    def __init__(self):
        host = settings['FINANCE_MONGODB_SERVER']
        port = settings['FINANCE_MONGODB_PORT']
        #创建mongodb数据库连接
        client = pymongo.MongoClient(host=host, port=port)
        dbName = settings['FINANCE_MONGODB_DB']
        #指定数据库
        tdb = client[dbName]
        #存放数据的数据表名
        self.post = tdb[settings['FINANCE_MONGODB_YICAIFINANCE_COLLECTION']]

    def process_item(self, item, spider):
        yicaifinance = dict(item)
        self.post.insert(yicaifinance)
        return item


    #mysql
    # def __init__(self):
    #     self.conn = MySQLdb.connect(
    #         host=settings['MYSQL_HOST'],
    #         port=settings['MYSQL_PORT'],
    #         db=settings['MYSQL_DBNAME'],
    #         user=settings['MYSQL_USER'],
    #         passwd=settings['MYSQL_PASSWD'],
    #         charset='utf8',
    #         use_unicode=True, )


#华尔街见闻
class WallStreetPipeline(object):
    #mongodb
    def __init__(self):
        host = settings['WALLSTREET_MONGODB_SERVER']
        port = settings['WALLSTREET_MONGODB_PORT']
        #创建mongodb数据库连接
        client = pymongo.MongoClient(host=host, port=port)
        dbName = settings['WALLSTREET_MONGODB_DB']
        #指定数据库
        tdb = client[dbName]
        #存放数据的数据表名
        self.post = tdb[settings['WALLSTREET_MONGODB_DB_COLLECTION']]

    def process_item(self, item, spider):
        wall_street = dict(item)
        self.post.insert(wall_street)
        return item

#中金在线
class CnfolPipeline(object):
    #mongodb
    def __init__(self):
        self.count = 0
        host = settings['CONFOL_MONGODB_SERVER']
        port = settings['CONFOL_MONGODB_PORT']
        #创建mongodb数据库连接
        client = pymongo.MongoClient(host=host, port=port)
        dbName = settings['CONFOL_MONGODB_DB']
        #指定数据库
        tdb = client[dbName]
        #存放数据的数据表名
        self.post = tdb[settings['CONFOL_MONGODB_DB_COLLECTION']]

    def process_item(self, item, spider):
        self.count =self.count+1
        print('+++++insert:+++++'+str(self.count))
        cnfol = dict(item)# 把item转化成字典形式
        self.post.insert(cnfol) # 向数据库插入一条记录
        return item   # 会在控制台输出原item数据，可以选择不写




