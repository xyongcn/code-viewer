简介
======

xblock调用脚本,在用户第一次访问时在gitlab上创建账号,上传公钥,初始化ucore

在每次用户访问时,利用本地的私钥从用户gitlab账户pull 代码,生成woboq 静态代码浏览页面,供iframe使用


gitlab部署及cli使用
======
[gitlab镜像](http://www.turnkeylinux.org/gitlab)

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

    ssh-keygen -b 1024 -t rsa
    
    scp .ssh/id_dsa.pub remote_usrname@gitlab server ip:
    
    ssh-add id_rsa
    
如果ssh-add 显示ssh-agent未启动,在.bashrc,.profile或其他配置文件中输入

    eval `ssh-agent -s`
    
以在www-data用户启动时启动ssh-agent

(在脚本运行过程中也需添加用户gitlab上的私钥,确保ssh-agent运行,另外ssh-agent每次启动其中的私钥都会被清空)

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




