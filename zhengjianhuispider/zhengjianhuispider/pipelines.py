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
from zhengjianhuispider.items import ZhengjianhuispiderItem
from zhengjianhuispider.items import YanghangspiderItem
from zhengjianhuispider.items import YingjianhuispiderItem
from zhengjianhuispider.items import TongjijuspiderItem
from zhengjianhuispider.items import CaizhengxinwenspiderItem
from zhengjianhuispider.items import ZhongzhengredianspiderItem
from zhengjianhuispider.items import JinrongjiespiderItem
class ZhengjianhuispiderPipeline(object):
   def __init__(self):
        self.count = 0
        host = settings['MONGODB_SERVER']
        port = settings['MONGODB_PORT']
        #创建mongodb数据库连接
        client = pymongo.MongoClient(host=host, port=port)
        # 数据库登录需要帐号密码的话
        # self.client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])
        dbName = settings['MONGODB_DB']  # 获得数据库的句柄
        #指定数据库
        self.tdb = client[dbName]

   def process_item(self, item, spider):
       if isinstance(item, ZhengjianhuispiderItem):
         #存放数据的数据表名
         self.post = self.tdb[settings['MONGODB_ZHENGJIANHUI_COLLECTION']]  # 获得collection的句柄
         self.count = self.count + 1
         print('+++++insert:+++++' + str(self.count))
         zhengjianhui = dict(item) # 把item转化成字典形式
         self.post.insert(zhengjianhui) # 向数据库插入一条记录
         #return item # 会在控制台输出原item数据，可以选择不写
       elif isinstance(item, YanghangspiderItem):
         #存放数据的数据表名
         self.post = self.tdb[settings['MONGODB_YANGHANG_COLLECTION']]  # 获得collection的句柄
         self.count = self.count + 1
         print('+++++insert:+++++' + str(self.count))
         yanghang = dict(item) # 把item转化成字典形式
         self.post.insert(yanghang) # 向数据库插入一条记录
        # return item # 会在控制台输出原item数据，可以选择不写
       elif isinstance(item,YingjianhuispiderItem):
        #存放数据的数据表名
         self.post = self.tdb[settings['MONGODB_YINGJIANHUI_COLLECTION']]  # 获得collection的句柄
         self.count = self.count + 1
         print('+++++insert:+++++' + str(self.count))
         yanghang = dict(item) # 把item转化成字典形式
         self.post.insert(yanghang) # 向数据库插入一条记录
        #return item # 会在控制台输出原item数据，可以选择不写
        #统计局
       elif isinstance(item,TongjijuspiderItem):
        #存放数据的数据表名
         self.post = self.tdb[settings['MONGODB_TONGJIJU_COLLECTION']]  # 获得collection的句柄
         self.count = self.count + 1
         print('+++++insert:+++++' + str(self.count))
         yanghang = dict(item) # 把item转化成字典形式
         self.post.insert(yanghang) # 向数据库插入一条记录
        # return item # 会在控制台输出原item数据，可以选择不写
       elif isinstance(item,CaizhengxinwenspiderItem):
        #存放数据的数据表名
         self.post = self.tdb[settings['MONGODB_CAIZHENGXINWEN_COLLECTION']]  # 获得collection的句柄
         self.count = self.count + 1
         print('+++++insert:+++++' + str(self.count))
         caizhengxinwen = dict(item)# 把item转化成字典形式
         self.post.insert(caizhengxinwen) # 向数据库插入一条记录
        # return item # 会在控制台输出原item数据，可以选择不写
       elif isinstance(item,ZhongzhengredianspiderItem):
        #存放数据的数据表名
         self.post = self.tdb[settings['MONGODB_ZHONGZHENGREDIAN_COLLECTION']]  # 获得collection的句柄
         self.count = self.count + 1
         print('+++++insert:+++++' + str(self.count))
         zhongzhengredianwang = dict(item)# 把item转化成字典形式
         self.post.insert(zhongzhengredianwang) # 向数据库插入一条记录
        # return item # 会在控制台输出原item数据，可以选择不写

       elif isinstance(item,JinrongjiespiderItem):
        #存放数据的数据表名
         self.post = self.tdb[settings['MONGODB_JINRONGJIE_COLLECTION']]  # 获得collection的句柄
         self.count = self.count + 1
         print('+++++insert:+++++' + str(self.count))
         jinrongjie = dict(item)# 把item转化成字典形式
         self.post.insert(jinrongjie) # 向数据库插入一条记录
        # return item # 会在控制台输出原item数据，可以选择不写