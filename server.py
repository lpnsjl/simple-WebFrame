# -*- coding: UTF-8 -*-
from socket import *
import re
from threading import Thread
import sys


HOST_ROOT_DIR = './html'
WSGI_WEB_DIR = './WSGIweb'
class HTTPServer(object):
    def __init__(self, application):
        """
        初始化服务器
        """
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        # 使端口可重复使用
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.app = application

    def bind(self, host, port):
        """
        绑定主机与端口并开始监听
        """
        self.server_socket.bind((host, port))
        self.server_socket.listen(128)

    def start(self):
        """
        启动服务器
        """
        while True:
            # print (1)
            client_socket, client_addr = self.server_socket.accept()
            print(1)
            print (str(client_addr) + '已连接')

            handle_client_thread = Thread(target=self.handle_request, args=(client_socket,))
            handle_client_thread.start()

    def start_response(self, status, headers):
        response_headers = 'HTTP/1.1' + status + '\n'
        for header in headers:
            response_headers += header[0] + ':' + header[1] + '\n'
        self.response_headers = response_headers

    def handle_request(self,client_socket):
        """
        处理客户端请求
        """
        recv_data = client_socket.recv(1024).decode('utf-8')
        request_lines = recv_data.splitlines()
        # print(request_lines)
        request_start_lines = request_lines[0]
        filename = re.findall(r'\w +(.*?) +HTTP', request_start_lines)[0]
        print(filename)

        env = {
            'PYTHON_PATH': filename
                }

        response_body = self.app(env, self.start_response)
        response = self.response_headers + '\n' + response_body

        client_socket.send(response.encode('utf-8'))
        client_socket.close()

def main():
    sys.path.insert(0,WSGI_WEB_DIR)
    http_server = HTTPServer()
    http_server.bind('127.0.0.1', 7788)
    http_server.start()

if __name__ == '__main__':
    main()

