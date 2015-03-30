简介
======

edx-xblock-codebrowser中放置的是在自己的openedx平台安装的xblock,xuetang_connection中放置的是在学堂在线上使用的方案

xblock调用脚本,在用户第一次访问时在gitlab上创建账号,上传公钥,初始化ucore

gitlab初始账号:

用户名: edx邮箱

初始密码: 随机8位密码,发送至邮箱

在每次用户访问时,利用本地的私钥从用户gitlab账户pull 代码,生成woboq 静态代码浏览页面,供iframe使用


gitlab部署及cli使用
======
[gitlab镜像](http://www.turnkeylinux.org/gitlab)

由于镜像版本过低,已重新安装最新版本

cli需ruby版本>=1.9.3,ubuntu12.04自带ruby过低

安装ruby1.9.3

    sudo apt-get install ruby 1.9.3
    cd /etc/alternatives
    sudo ln -sf /usr/bin/ruby1.9.3 ruby

cli安装及配置:

    gem install gitlab
    
    vi .profile
    
    export GITLAB_API_ENDPOINT='http://example.net/api/v3'
    export GITLAB_API_PRIVATE_TOKEN='your private token in admin account'

若安装正确,输入gitlab命令则有命令提示.

[gitlab cli 官方链接](http://narkoz.github.io/gitlab/)

(ps: 不要使用github上的版本,功能较少)

安装完的cli不含为指定用户上传公钥的功能,在此cli上自行添加函数

    vi /var/lib/gems/1.9.1/gems/gitlab-3.3.0/lib/gitlab/client/users.rb
(如果没有使用我给的镜像或者没有用gem安装的话,将其改为自己的gitlab安装的目录)

在文件中添加如下代码

    # Creates a new SSH key to a specified user. Only available to admin users.

    # @example
    #   Gielab.create_user_ssh_key('id','key title','key body')
    #
    # @param  [Integer] id- The ID of a user
    # @param  [String]  title- New SSH key's title
    # @param  [String]  key- New SSH Key
    # @return [Gitlab::ObjectifiedHash] Information about created SSH key.
    def create_user_ssh_key(id, title, key)
      post("/users/#{id}/keys", :body => {:title => title, :key => key})
    end
    
(ps :如果要查询gitlab提供的api接口的话,查看 /home/git/gitlab/lib/api 目录)


在edx服务器与gitlab服务器间建立无需密码的ssh连接(方便exp文件进行远程登录)
======

edx服务器:

切换到edx所用的账号(user :www-data, home: /var/www)

    sudo -u www-data bash
    
生成ssh密钥并将公钥拷贝到gitlab根目录,将私钥添加到ssh-agent

    cd /var/www/.ssh

    ssh-keygen -b 1024 -t rsa
    
    scp .ssh/id_dsa.pub remote_usrname@gitlab server ip:
    
    ssh-add id_rsa
    
如果ssh-add 显示ssh-agent未启动,在.bash_profile或其他配置文件中输入

    eval `ssh-agent -s`
    ssh-add
    
以在www-data用户启动时启动ssh-agent

(在脚本运行过程中也需添加用户gitlab上的私钥,确保ssh-agent运行,另外ssh-agent每次启动其中的私钥都会被清空)

xblock-script中的create.sh运行于gitlab上,会被exp文件远程调用,将其拷贝到gitlab服务器上

    scp xblock-script/create.sh remote_usrname@gitlab server ip:

以root用户登录gitlab:

    mkdir ~/.ssh(if the home dir don't have .ssh)
    
    chmod 700 ~/.ssh
    
    mv id_rsa.pub ~/.ssh
    
    cd ~/.ssh
    
    cat id_rsa.pub >> authorized_keys2
    
    rm -f id_rsa.pub
    
    chmod 600 authorized_keys2
    
现在已经建立了从edx服务器到gitlab服务器的ssh连接了

    ssh root@ip
    
能够无需输入密码即可登录说明配置正确
(ps: 第一次登录时会有提醒,exp文件中未对第一次的交互情况进行判断,所以务必先尝试以确保能够登录)


建立必要的目录
======
woboq codebrowser的编译及使用参考本项目另外的文档,不在此叙述,记得编译前先修改源码以确保点击目录时不报错


切换到www-data建立文件以确保有访问及创建文件的权限

    sudo -u www-data bash
    
    cd .ssh
    
    touch config
    
此config文件内容由脚本自动写入,用于在不同gitlab用户间切换时使用不同的私钥

    cd /edx/var/edxapp
    
拷贝编译完成的woboq codebrowser文件至此目录

    mkdir woboq_codebrowser
   
    cp -r your_woboq_codebrowser_file/* ./woboq_codebrowser/
    
    cd staticfiles
    
    mkdir codebrowser(放置代码浏览页面文件的目录)
    
    mkdir ucore(存放从用户gitlab上pull下来的代码)


主要文件介绍
======

1.codebrowser.py:

标准的xblock模块,利用os.system调用脚本,若脚本位置移动,记得修改此函数的参数并及时更新xblock


添加模块至edx-platform

    sudo -u edxapp /edx/bin/pip.edxapp install /home/zyu/xblock-codebrowser
    
若模块安装完成后修改了static目录中的文件,手动将static拷贝至指定目录并覆盖

    sudo cp -r static/* /edx/app/edxapp/venvs/edxapp/local/lib/python2.7/site-packages/static/
    
若修改了codebrowser.py

    sudo cp ./codebrowser.py /edx/app/edxapp/venvs/edxapp/local/lib/python2.7/site-packages/
    
2.static

static目录中存储了xblock所用的静态文件(js,html,css等)

3.xblock-script

存放了核心的脚本

create.sh :             运行于gitlab服务器上,被initialize_user.exp远程调用,以admin用户创建gitlab用户并做初始化

initialize_user.sh :    生成公钥,私钥,并写入git的配置文件(即上面创建的.ssh/config),调用initialize_user.exp
来上传公钥,初始化ucore项目

initialize_user.exp :   export 脚本,用于远程登录gitlab并调用create.sh

generator.sh :          从gitlab上pull代码,并生成代码浏览页面

make.sh :               ucore的make命令

若你没有按照上述的目录进行部署,需要修改脚本中的目录位置(代码放置目录,页面放置目录等等)

