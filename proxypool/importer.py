from proxypool.db import FileClient

conn = FileClient()

def set(proxy):
    result = conn.add(proxy)
    print('录入成功' if result else '录入失败')


def scan():
    print('请输入代理 (127.0.0.1:2321),输入exit则退出')
    while True:
        proxy = input()
        if proxy == 'exit':
            break
        set(proxy)

if __name__ == '__main__':
    scan()