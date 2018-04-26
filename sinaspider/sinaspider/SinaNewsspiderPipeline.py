#!/usr/bin/env python
# -*- coding:utf-8 -*-
#encoding=utf-8
'''
@描述：PyCharm
@作者：hingbox
@邮箱：hingbox@163.com
@版本：V1.0
@文件名称 : SinaNewsspiderPipeline.py
@创建时间：2018/4/26 9:07
'''

import MySQLdb
from twisted.enterprise import adbapi
import MySQLdb.cursors
class MysqldemospiderPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool("MySQLdb",
                                           db = "finance",        # 数据库名
                                           user = "root",       # 数据库用户名
                                           passwd = "root",     # 密码
                                           cursorclass = MySQLdb.cursors.DictCursor,
                                           charset = "utf8",
                                           use_unicode = False
                                           )
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
        return item

    def _conditional_insert(self, tb, item):
        tb.execute("insert into sinanews (title, orgurl) values (%s, %s)",\
                   (item["title"], item["orgurl"]))

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
