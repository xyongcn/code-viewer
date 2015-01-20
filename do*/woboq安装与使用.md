woboq是一款开源的在线代码浏览器,在服务器上部署后,只需提供项目所在的目录,即可生成静态的文件目录,在浏览器
打开后即可访问。
======
[官方网站部署流程](https://github.com/woboq/woboq_codebrowser)

woboq需要先安装clang以及gcc,cmake,此处选择clang-3.3

clang-3.3安装
======
(部署时直接使用apt-get install获取的clang,在woboq generator生成时报错policy CMP0004,此处改用官方预编译的release版)

    wget http://llvm.org/releases/3.3/clang+llvm-3.3-amd64-Ubuntu-12.04.2.tar.gz

创建目录并解压
    mkdir /usr/local/clang3.3

    tar -xzvf clang+llvm-3.3-amd64-Ubuntu-12.04.2.tar.gz  -C  /usr/local/

更改环境配置
    echo 'export PATH=/usr/local/clang+llvm-3.3-amd64-Ubuntu-12.04.2/bin:$PATH'>>/etc/profile

    export PATH=/usr/local/clang+llvm-3.3-amd64-Ubuntu-12.04.2/bin:$PATH

编译生成器
======
下载源码
    git clone https://github.com/woboq/woboq_codebrowser

cd woboq*

1)由于直接使用woboq官方版在edx浏览代码时会出现点击目录时报错的情况(404 not found),在编译前对源码做如下调整

(若已编译完则需重新编译)

将目录的链接从指向direc/改成指向direc/index.html

    cd indexgenerator
    vi indexr.cpp

63,69行 parent+ "'>" 改成 parent+ "index.html'>"

89行 href='../'改成  '../index.html'

96行 name << "/" 改成 name << "/index.html"

97行将 name << "/" 改成 name << "/index.html"


接着对data目录下的js文件做修改(无需重新编译即可生效)
    cd data
    vi codebrowser.js
将765行 bread+= "'>" 改成 bread+= "index.html'>"
    vi indexscript.js
将182行 name + "/"  改成 name + "/index.html'>"


 2)

    cmake . -DLLVM_CONFIG_EXECUTABLE=/usr/local/clang+llvm-3.3-amd64-Ubuntu-12.04.2/bin/llvm-config 
    -DCMAKE_CXX_COMPILER=/usr/local/clang+llvm-3.3-amd64-Ubuntu-12.04.2/bin/clang++ 
    -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_BUILD_TYPE=Release
    (若你直接使用apt-get install 可成功安装或使用其他方式则更改路径即可)

3)

    make

4)

    ln -s /usr/local/clang+llvm-3.3-amd64-Ubuntu-12.04.2/lib/ .

编译完成

使用生成器
======

    cmake . -DCMAKE_EXPORT_COMPILE_COMMANDS=ON

创建代码html文件

    codebrowser_generator -a -o <output_dir> -b <buld_dir> -p <projectname>:<source_dir>[:<revision>] [-d <data_url>] [-e <remote_path>:<source_dir>:<remote_url>]
(例如，将当前目录作为生成对象:

    ./generator/codebrowser_generator -b $PWD -a -o ~/public_html/codebrowser -p codebrowser:$PWD:`git describe --always --tags`)

生成索引html文件

    ./indexgenerator/codebrowser_indexgenerator ~/public_html/codebrowser

    ln -s ./data ~/public_html/

生成完毕,public_html目录下即为可浏览的代码页面。

