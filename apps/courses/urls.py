# -*- coding:utf-8 -*-
__author__ = 'jianzhihao'
__date__ = '17-3-25 下午3:28'

from django.conf.urls import url, include

from .views import CourseListView, CourseDetailView, CourseInfoView, CourseCommentView, AddCommentView,VideoPlayView

urlpatterns = [

    # 课程列表页V
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    # 课程详情页
    url(r'^detail/(?P<course_id>.*)/$', CourseDetailView.as_view(), name='detail'),
    url(r'^info/(?P<course_id>.*)/$', CourseInfoView.as_view(), name='course_info'),
    # 课程评论
    url(r'^commment/(?P<course_id>.*)/$', CourseCommentView.as_view(), name='course_commment'),
    # 添加课程评论
    url(r'^add_comment/$', AddCommentView.as_view(), name='add_comment'),

    url(r'^video/(?P<video_id>.*)/$', VideoPlayView.as_view(), name='video_play'),
]
