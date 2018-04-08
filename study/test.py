#!/usr/bin/python
# -*- coding: utf-8 -*-
import getopt
import sys
import time
if __name__ == '__main__':
    #这是第一财经分页的参数
    #遍历1-100 从0开始 每次遍历*3+1
    for x in range(1,101):
        print (x*3)+1

    for y in range(2,4):
        print ('yyy',y)

    # 10位时间戳
    timestamp = int(time.time())
    print (timestamp)
    # 13位时间错
    millis = int(round(time.time() * 1000))
    print (millis)
