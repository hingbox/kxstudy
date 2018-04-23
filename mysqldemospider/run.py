#!/usr/bin/env python
# -*- coding:utf-8 -*-
#encoding=utf-8
'''
@描述：PyCharm
@作者：hingbox
@邮箱：hingbox@163.com
@版本：V1.0
@文件名称 : run.py
@创建时间：2018/4/23 21:38
'''
from scrapy import cmdline
cmdline.execute("scrapy crawl mysqldemo".split())