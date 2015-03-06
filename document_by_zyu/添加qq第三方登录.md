添加QQ第三方登录
======
Open edX 的第三方登录使用了django-social-auth,django-social-auth,

[python-social-auth的github库](https://github.com/omab/python-social-auth/)

准备工作
======
1)在[QQ互联](http://connect.qq.com)上进行注册,获取开发者ID与密钥,要注册成功,
必须让QQ服务器能够访问到使用qq登录的页面.

验证时需修改edx首页,目录为/edx/app/edxapp/edx-platform/lms/templates/main.html

2)edx的django-social-auth默认库中没有对qq的支持,

从[github库](https://github.com/omab/python-social-auth/tree/master/social/backends)

中获取qq.py,将其拷贝至/edx/app/edxapp/venvs/edxapp/lib/python2.7/site-packages/social/backends/目录下

进入到edx环境
======
    sudo -u edxapp bash

    source /edx/app/edxapp/edxapp_env

    cd /edx/app/edxapp/edx-platform/

编写QQ Provider
======
    vi common/djangoapps/third_party_auth/provider.py

在from social.backends import google, linkedin, facebook
改为from social.backends import google, linkedin, facebook,qq

并在该文件中添加下述代码

    class QQOauth2(BaseProvider):
    """Provider for Wibo's Oauth2 auth system."""
    BACKEND_CLASS = qq.QQOAuth2
    ICON_CLASS = 'icon-qq-plus'
    NAME = 'QQ'
    SETTINGS = {
        'SOCIAL_AUTH_QQ_KEY': None,
        'SOCIAL_AUTH_QQ_SECRET': None,

    }

    @classmethod
    def get_email(cls, provider_details):
       return provider_details.get('email')



    @classmethod
    def get_name(cls, provider_details):
        return provider_details.get('fullname')
        

配置并测试provider
======
vi lms/envs/devstack.py

添加下述代码

    FEATURES['ENABLE_THIRD_PARTY_AUTH'] = True

    THIRD_PARTY_AUTH = {

    "Weibo": {

        "SOCIAL_AUTH_WEIBO_KEY": "your key",

        "SOCIAL_AUTH_WEIBO_SECRET": "your secret"

        }
    }
    
将your key, your secret用自己的id与密钥代替

进行测试
    ./manage.py lms --settings devstack syncdb --migrate
    paver devstack lms

若上述步骤皆正确，可在8000端口访问登录时看到qq登录
    
(注:以上为devstack环境下修改,若要在默认80端口看到第三方登录,则修改devstack.py需变为相应的lms.auth.json与lms.env.json,修改方式相同)


