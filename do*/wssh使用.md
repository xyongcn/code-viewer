wssh可以通过http来远程调用一个shell
======
只要服务器端安装了wssh，就可以通过浏览器来访问终端

1) 安装一些必要的软件

sudo apt-get install git gcc python libevent-dev python-dev python-pip

2) 安装 wssh 需要的各种 Python 库：

sudo pip install gevent gevent-websocket paramiko flask

3) 下载并安装wssh

git clone https://github.com/aluzzardi/wssh.git

$ cd wssh

$ sudo python setup.py install

4) 运行

wsshd

默认5000端口
