# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import urllib2
import os
import json
class StudyPipeline(object):
     def process_item(self, item, spider):
       with open("my_meiju.txt","a")as fp:
           fp.write(item["name"].encode("utf-8")+item["status"].encode("utf-8")+item["place"].encode("utf-8")+'\n')

class XiaoHuaPipeline(object):
    def process_item(self,item,spider):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'}
        req = urllib2.Request(url=item['address'],headers=headers)
        res = urllib2.urlopen(req)
        file_name = os.path.join(r'D:\my\down_pic',item['name']+'.jpg')
        with open(file_name,'wb') as fp:
            fp.write(res.read())
import codecs
class DongGuanPipeline(object):
    def __init__(self):
        #下面两个都可以
        #创建一个文件
        #self.filename = codecs.open("dongguan.json","w",encoding="utf-8")
        self.filename = open('dongguanspider.json','w')

    def process_item(self,item,spider):
        #中文默认使用ascii码来存储，禁用后默认为unicode字符串  encode 把unicode转换为指定的编码格式
        text = json.dumps(dict(item),ensure_ascii=False)+",\n"
        self.filename.write(text.encode("utf-8"))
        return item

    def close_spider(self,spider):
        self.filename.close()
