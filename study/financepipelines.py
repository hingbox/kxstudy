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
        movie_info = dict(item)
        self.post.insert(movie_info)
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
        movie_info = dict(item)
        self.post.insert(movie_info)
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


#专利
class PatentPipeline(object):
    def __init__(self):
        #下面两个都可以
        #创建一个文件
        #self.filename = codecs.open("dongguan.json","w",encoding="utf-8")
        self.filename = open('patent.json','w')

    def process_item(self,item,spider):
        #中文默认使用ascii码来存储，禁用后默认为unicode字符串  encode 把unicode转换为指定的编码格式
        text = json.dumps(dict(item),ensure_ascii=False)+",\n"
        self.filename.write(text.encode("utf-8"))
        return item

    def close_spider(self,spider):
        self.filename.close()

#糗事百科
class QiuShiBaiKePipeline(object):
    # def __init__(self):
    #     #下面两个都可以
    #     #创建一个文件
    #     #self.filename = codecs.open("dongguan.json","w",encoding="utf-8")
    #     self.filename = open('qiushibaike.json','w')
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
        host = settings['MONGODB_HOST_QIUSHIBAIKE']
        port = settings['MONGODB_PORT_QIUSHIBAIKE']
        # 创建mongodb数据库连接
        client = pymongo.MongoClient(host=host, port=port)
        dbName = settings['MONGODB_DB_QIUSHIBAIKE']
        # 指定数据库
        tdb = client[dbName]
        # 存放数据的数据表名
        self.post = tdb[settings['MONGODB_COLLECTION_QIUSHIBAIKE']]

    def process_item(self, item, spider):
        qiushibaike = dict(item)
        self.post.insert(qiushibaike)
        return item



