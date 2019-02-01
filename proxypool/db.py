import re
from proxypool.setting import *
import threading
import time
from proxypool.error import PoolEmptyError

threadLock = threading.Lock()

proxy_list = []
def readProxy():
    try:
        threadLock.acquire()
        readfile = open(LOCAL_FILE_PATH, 'r', encoding='UTF-8')
        for line in readfile:
            proxy_list.append(line.replace('\n',''))
    finally:
        threadLock.release()
    print('init proxy ok')



def persistproxy(sleeptime):
    while True:
        time.sleep(sleeptime)
        try:
            threadLock.acquire()
            writefile = open(LOCAL_FILE_PATH, 'w', encoding='utf-8')
            #hello
            for item in proxy_list:
                writefile.write(item+'\n')
        finally:
            threadLock.release()
        print('save proxy finshed')


readProxy()
t1 = threading.Thread(target=persistproxy,args=(10,))
t1.start()

class FileClient(object):

    def __init__(self):
        pass

    def add(self,proxy):
        '''porxy invalid'''
        if self.exist(proxy):
            print('代理已经存在%s 丢弃' %proxy)
            return False
        if not re.match('\d+\.\d+\.\d+\.\d+\:\d+',proxy):
            print('代理格式不规范,%s丢弃' %proxy);
            return False

        try:
            threadLock.acquire()
            proxy_list.append(proxy)
            return True
        finally:
            threadLock.release()

    def exist(self,proxy):
        return proxy_list.count(proxy)

    def count(self):
        return len(proxy_list)

    def empty(self):
        return len(proxy_list) == 0

    '''从头部取出并放入尾部'''
    def random(self):
        try:
            threadLock.acquire()
            if len(proxy_list):
                proxy = proxy_list.pop(0)
                proxy_list.append(proxy)
                return proxy
            else:
                raise PoolEmptyError
        finally:
            threadLock.release()

    @staticmethod
    def delete(proxy):
        try:
            threadLock.acquire()
            proxy_list.remove(proxy)
        finally:
            threadLock.release()


    '''头部取出不放入尾部'''
    def batch(self,size):
        try:
            threadLock.acquire()
            list = []
            for i in range(1,size):
                if not self.empty():
                    list.append(proxy_list.pop(0))
            return list
        finally:
            threadLock.release()


if __name__ == '__main__':
    client = FileClient()
    print(client.random())



