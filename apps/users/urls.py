# -*- coding:utf-8 -*-
__author__ = 'jianzhihao'
__date__ = '17-3-29 上午10:18'

from django.conf.urls import url

from .views import UserInfoView, UploadImageView, \
    UpdatePWDView, SendEmailCodeView, UpdateEmailView, MyCourseView, MyFavOrgView, MyFavTeachersView, MyFavCourseView, \
    MyMessageView

urlpatterns = [
    # 用户信息
    url(r'^user_info/$', UserInfoView.as_view(), name='user_info'),
    # 用户头像上传
    url(r'^image_upload/$', UploadImageView.as_view(), name='image_upload'),
    # 用户个人中心修改密码
    url(r'^update/pwd/$', UpdatePWDView.as_view(), name='update_pwd'),
    # 发送邮箱验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name='send_email_code'),

    # 修改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),

    # 我的课程
    url(r'^my_course/$', MyCourseView.as_view(), name='my_course'),

    # 我收藏的课程机构
    url(r'^myfav/org/$', MyFavOrgView.as_view(), name='my_fav_org'),

    # 我收藏的授课教师
    url(r'^myfav/teacher/$', MyFavTeachersView.as_view(), name='my_fav_teachers'),

    # 我收藏的课程
    url(r'^myfav/course/$', MyFavCourseView.as_view(), name='my_fav_courses'),

    # 我的消息
    url(r'^mymessage/$', MyMessageView.as_view(), name='my_message'),


]
