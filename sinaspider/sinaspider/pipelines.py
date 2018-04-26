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
from twisted.enterprise import adbapi
from MySQLdb.cursors import DictCursor
import MySQLdb
# 新浪新闻
class SinaspiderPipeline(object):
     def __init__(self):
        self.count=0
        self.dbpool = adbapi.ConnectionPool("MySQLdb",
                                           db = "finance",        # 数据库名
                                           user = "root",       # 数据库用户名
                                           passwd = "root",     # 密码
                                           cursorclass = MySQLdb.cursors.DictCursor,
                                           charset = "utf8",
                                           use_unicode = False
                                           )
     def process_item(self, item, spider):
         self.count = self.count + 1
         print ('-----insert---',str(self.count))
         query = self.dbpool.runInteraction(self._conditional_insert, item)
         query.addErrback(self.handle_error)
         return item

     def _conditional_insert(self, tb, item):
          tb.execute("insert into sinanews (title,type,content,writer,source,orgurl,summary,pubdate) values (%s,%s,%s,%s,%s,%s,%s,%s)",\
                   (item["title"],item["type"],item["content"],\
                    item["writer"],item["source"],item["orgurl"],item['summary'],item['pubdate']))
          #将sql语句提交到数据库执行
          #tb.conn.commint()
     def handle_error(self, e):
        pass
         # tb.execute("insert into douban (name, author, press, date, page, price, score, ISBN, author_profile,\
         #           content_description, link) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",\
         #           (item["name"], item["author"], item["press"], item["date"],\
         #           item["page"], item["price"], item["score"], item["ISBN"],\
         #           item["author_profile"], item["content_description"], item["link"]))
        #log.msg("Item data in db: %s" % item, level=log.DEBUG)

     # def handle_error(self, failure, item, spider):
     #    #出来异步插入异常
     #    print(failure)
    # '''
    #   异步机制将数据写入到mysql数据库中
    # '''
    #创建初始化函数，当通过此类创建对象时首先被调用的方法

    #引入操作数据库模块
#import MySQLdb

#class MysqlPipeline(object):
    # '''
    # 同步机制实现mysql写入操作
    # '''
    #
    # #定义初始化函数，当类被使用时自动调用这个函数，我们让他初始化时就连接上数据库
    # def __init__(self):
    #     self.count=0
    #     #取个变量名，连接数据库,依次是: host,user,password,dbname
    #     self.conn = MySQLdb.connect("127.0.0.1","root","root","finance")
    #     #通过cursor()的方法获取游标
    #     self.cursor = self.conn.cursor()
    #
    # #自定义的管道必须有此方法
    # def process_item(self,item,spider):
    #     self.count = self.count + 1
    #     print ('-----insert---',str(self.count))
    #     #要执行的插入sql语句
    #     insert_sql = """
    #         insert into sinanews(title,type,content,writer,source,orgurl,summary,pubdate
    #              )
    #           VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
    #     """





        #执行sql语句,注意后面是元组，将Item中的数据格式化填充到插入语句中
        # self.cursor.execute(insert_sql,(item["title"],item["creat_date"],item["url"],
        #     item["url_object_id"],item["front_image_url2"],item["front_image_path"],
        #     item["tags"],item["comment_num"],item["fav_num"],item["like_num"],item["content"]))
        # self.cursor.execute(insert_sql,(item["title"],item["type"],item["content"],
        #  item["writer"],item["source"],item["orgurl"],item['summary'],item['pubdate']))
        #
        # #将sql语句提交到数据库执行
        # self.conn.commint()
    # def __init__(self,dbpool):
    #     self.dbpool = dbpool
    #     self.count=0
    # #创建一个静态方法,静态方法的加载内存优先级高于init方法，java的static方法类似，
    # #在创建这个类的对之前就已将加载到了内存中，所以init这个方法可以调用这个方法产生的对象
    # @classmethod
    # #名称固定的
    # def from_settings(cls,settings):
    #     #先将setting中连接数据库所需内容取出，构造一个地点
    #     dbparms = dict(
    #         host= settings["MYSQL_HOST"],
    #         db = settings["MYSQL_DBNAME"],
    #         user = settings["MYSQL_USER"],
    #         passwd = settings["MYSQL_PASSWORD"],
    #         charset = "utf-8",
    #         #游标设置
    #         #cursorclass = MySQLdb.cursors.DictCursor,
    #         cursorclass=DictCursor,
    #         #设置编码是否使用Unicode
    #         use_unicode = True,
    #         port=settings['MYSQL_PORT']
    #     )
    #     #通过Twisted框架提供的容器连接数据库,MySQLdb是数据库模块名
    #     dbpool = adbapi.ConnectionPool("MySQLdb",dbparms)
    #     return cls(dbpool)
    #
    # def process_item(self,item,spider):
    #     #使用Twisted异步的将Item数据插入数据库
    #     query = self.dbpool.runInteraction(self.do_insert,item)
    #     query.addErrback(self.handle_error,item,spider)#这里不往下传入item,spider，handle_error则不需接受,item,spider)
    #
    # def do_insert(self,cursor,item):
    #     self.count = self.count + 1
    #     print ('-----insert---',str(self.count))
    #     #执行具体的插入语句,不需要commit操作,Twisted会自动进行
    #     insert_sql = """
    #          insert into sinanews(title,type,content,writer,source,orgurl,summary,pubdate
    #              )
    #          VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
    #     """
    #     cursor.execute(insert_sql,(item["title"],item["type"],item["content"],
    #         item["writer"],item["source"],item["orgurl"],item['summary'],item['pubdate']))
    #
    # def handle_error(self, failure, item, spider):
    #     #出来异步插入异常
    #     print(failure)


class MysqldemospiderPipeline(object):
    def __init__(self):
        self.count=1
        self.dbpool = adbapi.ConnectionPool("MySQLdb",
                                           db = "finance",        # 数据库名
                                           user = "root",       # 数据库用户名
                                           passwd = "root",     # 密码
                                           cursorclass = MySQLdb.cursors.DictCursor,
                                           charset = "utf8",
                                           #use_unicode = False,
                                           use_unicode=True,
                                           )
    def process_item(self, item, spider):
        self.count = self.count + 1
        print ('-----insert---',str(self.count))
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
        return item

    def _conditional_insert(self, tb, item):
         # tb.execute("insert into sinanews (title,type) values (%s,%s)",\
         #           (item["title"],item['type']))
          tb.execute("insert into sinanews (title,type,writer,source,orgurl,summary,pubdate,create_date,recorddate,content) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",\
                   (item["title"],item["type"],\
                    item["writer"],item["source"],item["orgurl"],item['summary'],item['pubdate'],item['create_date'],item['recorddate'],item['content']))
        # tb.execute("insert into sinanews (title,type,content,writer,source,orgurl,summary,pubdate) values (%s,%s,%s,%s,%s,%s,%s,%s)",\
        #            (item["title"],item["type"],item["content"],\
        #             item["writer"],item["source"],item["orgurl"],item['summary'],item['pubdate']))

         # tb.execute("insert into douban (name, author, press, date, page, price, score, ISBN, author_profile,\
         #           content_description, link) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",\
         #           (item["name"], item["author"], item["press"], item["date"],\
         #           item["page"], item["price"], item["score"], item["ISBN"],\
         #           item["author_profile"], item["content_description"], item["link"]))
        #log.msg("Item data in db: %s" % item, level=log.DEBUG)

    def handle_error(self, e):
       pass

    def _conditional_search(self):
        conn=MySQLdb.connect(host="127.0.0.1",user="root",passwd="root",db="scrapy")
        cursor = conn.cursor()
        n = cursor.execute("select count(*) from demo")
        for row in cursor.fetchall():
            for r in row:
                print r

# Python时间，日期，时间戳之间转换
# 1.将字符串的时间转换为时间戳
#     方法:
#         a = "2013-10-10 23:40:00"
#         将其转换为时间数组
#         import time
#         timeArray = time.strptime(a, "%Y-%m-%d %H:%M:%S")
#     转换为时间戳:
#     timeStamp = int(time.mktime(timeArray))
#     timeStamp == 1381419600
# 2.字符串格式更改
#     如a = "2013-10-10 23:40:00",想改为 a = "2013/10/10 23:40:00"
#     方法:先转换为时间数组,然后转换为其他格式
#     timeArray = time.strptime(a, "%Y-%m-%d %H:%M:%S")
#     otherStyleTime = time.strftime("%Y/%m/%d %H:%M:%S", timeArray)
#
#
# 3.时间戳转换为指定格式日期:
#     方法一:
#         利用localtime()转换为时间数组,然后格式化为需要的格式,如
#         timeStamp = 1381419600
#         timeArray = time.localtime(timeStamp)
#         otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
#         otherStyletime == "2013-10-10 23:40:00"
#
#     方法二:
#         import datetime
#         timeStamp = 1381419600
#         dateArray = datetime.datetime.utcfromtimestamp(timeStamp)
#         otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")
#         otherStyletime == "2013-10-10 23:40:00"
#
# 4.获取当前时间并转换为指定日期格式
#     方法一:
#         import time
#         获得当前时间时间戳
#         now = int(time.time())  ->这是时间戳
#         转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
#         timeArray = time.localtime(timeStamp)
#         otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
#
#     方法二:
#         import datetime
#         获得当前时间
#         now = datetime.datetime.now()  ->这是时间数组格式
#         转换为指定的格式:
#         otherStyleTime = now.strftime("%Y-%m-%d %H:%M:%S")
#
# 5.获得三天前的时间
#     方法:
#         import time
#         import datetime
#         先获得时间数组格式的日期
#         threeDayAgo = (datetime.datetime.now() - datetime.timedelta(days = 3))
#         转换为时间戳:
#             timeStamp = int(time.mktime(threeDayAgo.timetuple()))
#         转换为其他字符串格式:
#             otherStyleTime = threeDayAgo.strftime("%Y-%m-%d %H:%M:%S")
#     注:timedelta()的参数有:days,hours,seconds,microseconds
#
# 6.给定时间戳,计算该时间的几天前时间:
#     timeStamp = 1381419600
#     先转换为datetime
#     import datetime
#     import time
#     dateArray = datetime.datetime.utcfromtimestamp(timeStamp)
#     threeDayAgo = dateArray - datetime.timedelta(days = 3)
#     参考5,可以转换为其他的任意格式了