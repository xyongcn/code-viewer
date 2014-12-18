由于edx中无法利用file//的形式直接加载服务器本地html文件,此处利用python快速搭建一个测试的web服务器,实现文件共享
======
(例如woboq生成的public_html，即由此方式嵌入edx)

在安装edx时python已安装,无需再安装

进入所需共享的目录

python -m SimpleHTTPServer  portnumber(服务器上使用的是9999)

即可在ip+portnumber访问共享目录
