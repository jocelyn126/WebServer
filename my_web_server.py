"""
author: Jocelyn
email:baccy126@126.com
time:2020-6-21
env:Python3.6
IO多路复用和http训练
"""
import re
from select import select
from socket import *


class WebServer:
    def __init__(self, host="0.0.0.0", port=6007, html=None):
        self.host=host
        self.port=port
        self.html=html
        self.address=(host,port)

        self.__rlist=[]
        self.__wlist=[]
        self.__xlist=[]

        #6创建一个对象，就创建一个TCP套接字
        self.create_socket()
        self.s_sock.setblocking(False)
        self.bind()

    def start(self):
        #2http协议只能用TCP套接字
        #5创建监听队列
        self.s_sock.listen(6)
        #6打印一下服务端的端口，查看服务端是否在线
        print("Listen to the port %d" % self.port)
        #7组织IO复用
        self.__rlist.append(self.s_sock)
        while True:
            rs,ws,xs=select(self.__rlist,self.__wlist,self.__xlist)
            for r in rs:
                if r is self.s_sock:
                    c_sock,addr=r.accept()
                    c_sock.setblocking(False)
                    self.__rlist.append(c_sock)
                else:
                    #8对客户端套接字接收过来的数据进行处理
                    self.handle(r)


    def create_socket(self):
        # 3创建套接字-套接字其他方法也要用，设成实例变量-降低耦合度，提出去作为独立方法
        self.s_sock = socket()

    def bind(self):
        # 4绑定地址-降低耦合度，提出去作为独立方法
        self.s_sock.bind(self.address)

    def handle(self, c_sock):
        data=c_sock.recv(1024*10).decode()
        #8对接收到的HTTP协议进行解读, 先解读请求行
        print(data) #GET / HTTP/1.1
        #此处仅处理GET业务
        content=re.match("[A-Z]+\s+(?P<pattern>/\S*)",data)
        if content:
            ask_html_path = content.group("pattern")
            print("打印请求行:",ask_html_path)
            self.get_html(c_sock,ask_html_path)
        else:
            c_sock.close()
            self.__rlist.remove(c_sock)
            return

    def get_html(self, c_sock, ask_html_path):
        #9用请求的地址匹配本地的地址
        if ask_html_path=="/":
            file_path=self.html+"/index.html"
        else:
            file_path=self.html+ask_html_path
        try:
            #匹配成功或者匹配失败
            fd=open(file_path,"rb")
        except:
            response = """
            HTTP/1.1 404 Not Found
            Content-Type:text/html
            
            <h1>Sorry...We dont have that page.</h1>
            """
            response = response.encode()
        else:
            content=fd.read()
            response="""
            HTTP/1.1 200 OK
            Content-Type:text/html
            
            """
            response=response.encode()+content
            fd.close()
        finally:
            c_sock.send(response)


if __name__ == '__main__':
    #1调用一个类， 可以把自己做的网页让浏览器通过http协议读取
    httpd=WebServer(host="0.0.0.0",port=6009,html="./static")
    httpd.start()