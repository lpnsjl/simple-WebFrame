# -*- coding: UTF-8 -*-
import time
from server import HTTPServer


HOST_ROOT_DIR = './html'
class Application(object):
    def __init__(self, urls):
        self.urls = urls

    def __call__(self, env, start_response):
        path = env.get('PYTHON_PATH', '/')
        if path.startswith('/static'):
            filename = path[7:]
            try:
                f = open(HOST_ROOT_DIR + filename, 'r')
            except:
                status = '404 Not Found'
                headers = [
                    ('Connection', 'keep-alive')
                ]
                start_response(status, headers)
                return 'page not found'
            else:
                file_data = f.read()
                f.close()
                status = '200 ok'
                headers = [
                    ('Connection', 'keep-alive')
                ]
                start_response(status, headers)
                return file_data

        for url, handler in self.urls:
            if url == path:
                return handler(env, start_response)

        status = '404 Not Found'
        headers = [
            ('Connection', 'keep-alive')
        ]
        start_response(status, headers)
        return 'page not found'

def show_time(env, start_response):
    status = '200 ok'
    headers = [
        ('Connection', 'keep-alive')
    ]
    start_response(status, headers)
    return time.ctime()

def say_hello(env, start_response):
    status = '200 ok'
    headers = [
        ('Connection', 'keep-alive')
    ]
    start_response(status, headers)
    return 'Hi, I am gougou'

if __name__ == '__main__':
    urls = [
        ('/ctime', show_time),
        ('/say_hello', say_hello),
        ('/', show_time)
    ]

    app = Application(urls)
    http_server = HTTPServer(app)
    http_server.bind('127.0.0.1', 7788)
    http_server.start()
