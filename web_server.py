"""
web server 程序
完成一个类，提供给使用者
使用可通过这个类可以快速搭建web 后端服务，用于展示自己的网页

IO多路复用和http训练
"""
from socket import *
from select import select

class WebServer:
    def __init__(self,host="0.0.0.0",port=6007,html=None):
        self.host = host
        self.port = port
        self.html = html
        self.address = (host,port)
        # 创建套接字
        self.create_socket()
        self.bind()

    # 创建套接字
    def create_socket(self):
        self.sock = socket()
        self.sock.setblocking(False)

    # 绑定地址
    def bind(self):
        self.sock.bind((self.host,self.port))

    # 启动函数，启动整个服务 --> 客户端可以发起链接
    def start(self):
        self.sock.listen(5)
        print("Listen to the port %d"%self.port)
        # IO 多路复用



if __name__ == '__main__':
    # 使用者应该怎么用我这个类

    # 什么东西应该是用户确定的，通过参数传入
    # 地址  要展示什么网页

    httpd = WebServer(host="0.0.0.0",port=8000,html="./static")
    httpd.start()