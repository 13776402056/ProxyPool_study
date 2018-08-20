from proxypool.setting import *
from proxypool.getter import Getter
import time
from proxypool.api import app
import threading

class Scheduler():
    def schedule_getter(self,cycle=GETTER_CYCLE):
        getter = Getter()
        while True:
            print('开始抓取代理')
            getter.run()
            time.sleep(cycle)

    def schedule_api(self):
        app.run()

    #IP POOL启动主类
    def run(self):
        if GETTER_ENABLED:
            tester_thread = threading.Thread(target=self.schedule_getter)
            tester_thread.start()
        if API_ENABLED:
            api_thread = threading.Thread(target=self.schedule_api)
            api_thread.start()



