from flask import Flask, g
from proxypool.db import FileClient

__all__ = ['app']

app=Flask(__name__)

def get_conn():
    if not hasattr(g,'redis'):
        g.redis = FileClient()
    return g.redis

@app.route('/')
def index():
    return '<h2>Welcome to Proxy Pool System Author derek</h2>'

@app.route('/random')
def get_porxy():
    '''获取一个随机代理'''
    conn = get_conn()
    proxy =conn.random()
    if proxy:
        return proxy
    else:
        return 'null'

@app.route('/count')
def get_counts():
    '''get redis connection'''
    conn = get_conn()
    return str(conn.count())

if __name__ == '__main__':
    app.run()
