# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
from twisted.enterprise import adbapi
import MySQLdb.cursors
class MysqldemospiderPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool("MySQLdb",
                                           db = "scrapy",        # 数据库名
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
        tb.execute("insert into demo (title, url) values (%s, %s)",\
                   (item["title"], item["url"]))

         # tb.execute("insert into douban (name, author, press, date, page, price, score, ISBN, author_profile,\
         #           content_description, link) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",\
         #           (item["name"], item["author"], item["press"], item["date"],\
         #           item["page"], item["price"], item["score"], item["ISBN"],\
         #           item["author_profile"], item["content_description"], item["link"]))
        #log.msg("Item data in db: %s" % item, level=log.DEBUG)

    def handle_error(self, e):
       pass
