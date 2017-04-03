# coding:utf-8

from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField

from organization.models import CourseOrg, Teacher


# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name='课程机构', null=True, blank=True)
    category = models.CharField(max_length=20, verbose_name='课程类别', default='后端开发')
    name = models.CharField(max_length=50, verbose_name=u'课程名称')
    desc = models.CharField(max_length=300, verbose_name=u'课程描述')
    detail = UEditorField(verbose_name=u'课程详情', width=600, height=300, imagePath="course/ueditor/",
                          filePath="course/ueditor/", default='')
    teacher = models.ForeignKey(Teacher, verbose_name='讲师', null=True, blank=True)
    degree = models.CharField(choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')), max_length=2, verbose_name='难度')
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长(分钟数)')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    favour_number = models.IntegerField(default=0, verbose_name=u'收藏')
    image = models.ImageField(upload_to='course/%Y/%m', verbose_name=u'封面图', max_length=100)
    tag = models.CharField(verbose_name='课程标签', max_length=16, default='')
    click_number = models.IntegerField(default=0, verbose_name=u'点击量')
    need_know = models.CharField(max_length=300, verbose_name='课程需知', default='')
    is_banner = models.BooleanField(default=False, verbose_name='是否轮播')
    teacher_tell_you = models.CharField(max_length=300, verbose_name='老师告诉你', default='')

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        # 获取章节数量
        return self.lesson_set.all().count()

    get_zj_nums.short_description = '章节数'

    def get_learn_users(self):
        # 获取学习用户
        return self.usercourse_set.all()[:5]

    def get_course_lessons(self):
        # 获取课程所有章节
        return self.lesson_set.all()


class BannerCourse(Course):
    class Meta:
        verbose_name = '轮播课程'
        verbose_name_plural = verbose_name
        """
        如果不设置proxy为True则默认生成一张表
        """
        proxy = True


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长(分钟数)')
    name = models.CharField(max_length=100, verbose_name=u'章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_lesson_video(self):
        # 获取章节视频
        return self.video_set.all()


class Video(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'视频名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    lesson = models.ForeignKey(Lesson, verbose_name=u'章节')
    url = models.CharField(max_length=200, verbose_name='访问地址', default='')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程名称')
    name = models.CharField(max_length=100, verbose_name=u'资源名称')
    download = models.FileField(upload_to='course/resource/%Y/%m', verbose_name=u'资源文件', max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
