# add by zyu
import os
import string
import random
import smtplib
import logging.handlers
from django.utils.encoding import force_text

from email.mime.text import MIMEText

def init_git(request):
    usrid = request.GET.get('usrid')
    email = request.GET.get('email')
    name  = request.GET.get('name')

 #   if len(usrid) != 32:
 #      return HttpResponse("<p>your id is wrong</p>")

    #the account has existed
    rsa_file = '/var/www/.ssh/id_rsa_' + usrid
    if os.path.isfile(rsa_file):
        return HttpResponse("<p>the account has existed!</p>")

    #header = force_text(request.META.get('HTTP_REFERER', ''), errors='replace')
    #set logging params
    LOG_FILE = '/var/www/gitlab_account_init.log'
    handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024)
    fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)

    logger = logging.getLogger('gitlab_account_init')
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    #generate random passwd
    passwd = string.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a','0','1','2','3','4','5','6','7','8','9'], 8)).replace(' ','')

    logger.info('info generate gitlab account id:' + usrid +' email:' + email + ' name:' + name + ' initial passwd:' +passwd)
    
    #add gitlab account
    os.system("/edx/var/edxapp/staticfiles/xblock-script/initialize_user.sh " + usrid + " " + email + " " + name + " " + passwd)

    #add edx account
    os.system("/edx/var/edxapp/staticfiles/xblock-script/create_edx_user.sh " + email + " " + name + " " + passwd)

    #send passwd to user's email
    mailto_list=[email]
    mail_host="smtp.163.com"
    mail_user="zyu_mooc"
    mail_pass="********"
    mail_postfix="163.com"

    content="<p>this is the initial password of gitlab,please reset it ,the email is the same as the account of mooc. \n password:" + passwd + "</p>" + "\n<a href='http://south.cs.tsinghua.edu.cn/users/sign_in'>click here to jump to gitlab</a>"

    sub="mooc OS:initial password of gitlab"
    msg = MIMEText(content,_subtype='html',_charset='utf-8')
    msg["Accept-Language"]="zh-CN"
    msg["Accept-Charset"]="ISO-8859-1,utf-8"
    msg['Subject'] = sub
    me="hello"+"<"+mail_user+"@"+mail_postfix+">"
    msg['From'] = me
    msg['To'] = ";".join(mailto_list)

    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(me, mailto_list, msg.as_string())
        s.close()
    except Exception, e:
        logger.info(str(e))
        return False

    return HttpResponse("<p>the initial password has been sent to your mooc email,please check</p>" + "<a href = 'http://south.cs.tsinghua.edu.cn/'>click here to log in gitlab</a>")




def codebrowser(request):
    usrid = request.GET.get('usrid')
    name  = request.GET.get('name')
    lab   = request.GET.get('lab')
    #set logging params
    LOG_FILE = '/var/www/gitlab_account_init.log'
    handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024)
    fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)

    logger = logging.getLogger('gitlab_account_init')
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    logger.info('info codebrowser  id:' + usrid + ' name:' + name + 'lab: ' + lab)

    os.system("/edx/var/edxapp/staticfiles/xblock-script/generator.sh " + usrid + " "  + name + " " + lab)
    return HttpResponse("usrid = " + usrid)
