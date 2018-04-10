#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
class Test(object):
    def add(x):
        print('---',x)
        return x+1
        return x+2

    print (add(6))

    def a(self):
        data = [{"id": "1979254",
                 "title": "\\u524d\\u5546\\u52a1\\u90e8\\u5b98\\u5458:\\u8fd9\\u662f40\\u5e74\\u6765\\u7b2c\\u4e00\\u573a\\u771f\\u6b63\\u7684\\u4e2d\\u7f8e\\u8d38\\u6613\\u6218",
                 "media": "\\u65f6\\u4ee3\\u5468\\u62a5", "author": "", "comment_url": "",
                 "url": "http:\\/\\/finance.sina.com.cn\\/china\\/gncj\\/2018-04-10\\/doc-ifyvtmxe7692217.shtml",
                 "create_date": "2018-04-10", "create_time": "04:00:15", "cat_name": "finance_0_suda",
                 "top_time": "20180410", "top_num": "35,109", "ext1": "", "ext2": "",
                 "ext3": "http:\\/\\/n.sinaimg.cn\\/news\\/crawl\\/72\\/w550h322\\/20180410\\/BDjJ-fyvtmxe7482560.jpg",
                 "ext4": "fyvtmxe7692217", "ext5": "", "time": "Tue, 10 Apr 2018 04:00:15 +0800"}]
        cc = data.replace('\\\\','\\')
        return cc
    print ('-----------',a())

if __name__ == '__main__':
    #这是第一财经分页的参数
    #遍历1-100 从0开始 每次遍历*3+1
    #for x in range(1,101):
        #print (x*3)+1

    #for y in range(2,4):
       # print ('yyy',y)

    # 10位时间戳
    timestamp = int(time.time())
    print (timestamp)
    # 13位时间错
    millis = int(round(time.time() * 1000))
    print (millis)


