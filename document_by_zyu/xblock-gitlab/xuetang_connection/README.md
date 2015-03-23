与学堂在线的连接方案
======

1.由于学堂在线上无法在服务器上安装xblock,所以只能在自己的服务器上进行处理,向外提供一个服务借口

student_view.html是学堂在线前台的html文件,访问edx服务器的一个特定url,并向url传递参数:{用户id,邮箱,用户名}

edx服务器使用django架构,在urls.py文件中添加对如下url的处理

    cd /edx/app/edxapp/edx-platform/lms
    vi urls.py
    #url匹配中添加如下代码
    #add by zyu,call the script to create gitlab account
    url(r'^codebrowser$', 'student.views.codebrowser'),
    //url(r'^init_git$', 'student.views.init_git'),
    
然后在/edx/app/edxapp/edx-platform/common/djangoapps/student/views.py中添加处理函数，内容如django_views.py所示

create_edx_user.sh添加一个edx用户

其余脚本由于传递的参数与xblock有所不同,并且所使用的实验代码不同(ucore_lab中包含lab1~lab8)

代码内容略有不同,见本目录的其余脚本,generator.sh.old为自己提供创建账号接口时使用的脚本,现已使用郭旭提供的接口,generator.sh为当前使用的脚本

2.gitlab由于以前使用的版本过老,已更新至最新版本,gitlab cli中创建用户的命令不可用,所以自写了一个ruby脚本用于访问api,见create_user.rb


api中users.rb修改如下代码以跳过用户的邮件激活

    #add by zyu
        user.skip_confirmation!
        if user.save
          present user, with: Entities::UserFull
