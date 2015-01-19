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





