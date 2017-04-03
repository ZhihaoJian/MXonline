# -*- coding:utf-8 -*-
"""MXonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.static import serve
import xadmin

from MXonline.settings import MEDIA_ROOT
from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView, \
    UserCenterView, LogoutView, IndexView

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='user_active_view'),
    url(r'^forget_password/$', ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'^reset/(?P<reset_code>.*)/$', ResetView.as_view(), name='reset_pwd'),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name='modify_pwd'),
    url(r'^usercenter/$', UserCenterView.as_view(), name='usercenter-info'),

    # 课程机构url配置
    url(r'^org/', include('organization.urls', namespace='org')),

    # 课程相关URL配置
    url(r'^course/', include('courses.urls', namespace='course')),

    # 课程相关URL配置
    url(r'^users/', include('users.urls', namespace='users')),

    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    # 配置上传路径的访问地址
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

    # 富文本插件
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    # url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
]
# 全局404页面配置
handler404 = 'users.views.page_not_found'
# 全局500页面配置
handler500 = 'users.views.page_error'
