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
class CailianspiderPipeline(object):
    def __init__(self):
        self.count = 0
        host = settings['MONGODB_SERVER']
        port = settings['MONGODB_PORT']
        #创建mongodb数据库连接
        client = pymongo.MongoClient(host=host, port=port)
        dbName = settings['MONGODB_DB']
        #指定数据库
        tdb = client[dbName]
        #存放数据的数据表名
        self.post = tdb[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
         self.count = self.count + 1
         print('+++++insert:+++++' + str(self.count))
         sinafinance = dict(item)
         self.post.insert(sinafinance)
         return item
