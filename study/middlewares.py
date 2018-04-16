# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
from scrapy import signals
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
from user_agents import agents
import base64
import json

class StudySpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)



class MyUserAgentMiddleware(UserAgentMiddleware):
    '''
    设置User-Agent
    '''

    def __init__(self, user_agent):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user_agent=crawler.settings.get('MY_USER_AGENT')
        )

    def process_request(self, request, spider):
        agent = random.choice(self.user_agent)
        #print "++++++++++++++++++"+agent
        request.headers['User-Agent'] = agent
        #request.headers.setdefault('User-Agent',agent)
#这是另一种写法 需要在settins中配置方可生效
class UserAgentMiddleware(object):
    """ 换User-Agent """

    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent

class RandomProxyMiddleware(object):
    '''
    设置IP_proxy
    '''

    def __init__(self, ip_proxy):
        self.ip_proxy = ip_proxy

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            ip_proxy=crawler.settings.get('IP_PROXIES')
        )

    def process_request(self, request, spider):
        proxy = random.choice(self.ip_proxy)

        #如果没有代理账户验证校验
        if proxy['user_passwd'] is None:
            request.meta['proxy'] = "http://"+proxy['ip_port']
            print proxy['ip_port']
        else:
            base64_userpasswd = base64.b64encode(proxy['user_passwd'])
            request.headers['Proxy-Authorization'] = 'Basic '+base64_userpasswd
            request.meta['proxy']="http://"+proxy['ip_port']

#设置cookies 同样需要在settting配置文件中配置方可生效
class CookiesMiddleware(object):
    """ 换Cookie """
    cookie = {
        'platform': 'pc',
        'ss': '367701188698225489',
        'bs': '%s',
        'RNLBSERVERID': 'ded6699',
        'FastPopSessionRequestNumber': '1',
        'FPSRN': '1',
        'performance_timing': 'home',
        'RNKEY': '40859743*68067497:1190152786:3363277230:1'
    }

    def process_request(self, request, spider):
        bs = ''
        for i in range(32):
            bs += chr(random.randint(97, 122))
        _cookie = json.dumps(self.cookie) % bs
        request.cookies = json.loads(_cookie)