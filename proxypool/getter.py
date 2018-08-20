from proxypool.db import FileClient
from proxypool.crawler import Crawler
from proxypool.setting import *
class Getter():
    def __init__(self):
        self.redis = FileClient()
        self.crawler = Crawler()

    def is_over_flow(self):
        '''判断是否达到代理池限制'''
        if self.redis.count() >= POOL_UPPER_FLOW:
            return True
        return False

    def run(self):
        print('获取器开始执行')
        if not self.is_over_flow():
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]
                proxies = self.crawler.get_proxies(callback)
                for proxy in proxies:
                    self.redis.add(proxy)
        else:
            print('代理池数量已够',str(self.redis.count()))


# if __name__ == '__main__':
#     getter = Getter()
#     getter.run()