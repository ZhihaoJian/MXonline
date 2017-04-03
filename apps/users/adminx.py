# -*- coding:utf-8 -*-
import xadmin
from xadmin import views
from users.models import EmailVerifyRecord, Banner, UserProfile
from xadmin.plugins.auth import UserAdmin
from django.contrib.auth.models import User

__author__ = 'jianzhihao'
__date__ = '17-3-2 上午10:12'


class UserProfileAdmin(UserAdmin):
    pass

# xadmin.site.register(UserProfile, UserProfileAdmin)
# xadmin.site.unregister(User)



class BaseSetting(object):
    """注册自定义设定"""
    enable_themes = True
    use_bootswatch = True


xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSettings(object):
    """修改注册后台管理系统标题和注脚"""
    site_title = '慕学后台管理系统'
    site_footer = '慕学在线网'
    # 左侧快速折叠栏
    menu_style = 'accordion'


xadmin.site.register(views.CommAdminView, GlobalSettings)


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(Banner, BannerAdmin)
