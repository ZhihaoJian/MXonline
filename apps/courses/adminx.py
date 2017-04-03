# -*- coding:utf-8 -*-
import xadmin

__author__ = 'jianzhihao'
__date__ = '17-3-2 上午10:50'

from .models import Course, Lesson, Video, CourseResource, BannerCourse


class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    model = CourseResource
    extra = 0


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'learn_times', 'students', 'favour_number', 'image', 'click_number',
                    'add_time', 'degree', 'get_zj_nums']
    search_fields = ['name', 'desc', 'detail', 'learn_times', 'students', 'favour_number', 'image', 'click_number',
                     'degree']
    list_filter = ['name', 'desc', 'detail', 'learn_times', 'students', 'favour_number', 'image', 'click_number',
                   'add_time', 'degree']
    ordering = ['-click_number']
    list_editable = ['degree', 'name']
    readonly_fields = ['click_number', 'favour_number']
    inlines = [LessonInline, CourseResourceInline]
    style_fields = {'detail': 'ueditor'}

    def queryset(self):
        """
        重载该方法获取非轮播课程数据
        :return: 
        """
        return super(CourseAdmin, self).queryset().filter(is_banner=False)

    def save_models(self):
        """
        在保存课程的时候统计课程机构的课程数量
        :return: 
        """
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.courses_nums = Course.objects.filter(course_org=course_org)
            course_org.save()


xadmin.site.register(Course, CourseAdmin)


class CourseBannerAdmin(object):
    list_display = ['name', 'desc', 'detail', 'learn_times', 'students', 'favour_number', 'image', 'click_number',
                    'add_time', 'degree']
    search_fields = ['name', 'desc', 'detail', 'learn_times', 'students', 'favour_number', 'image', 'click_number',
                     'degree']
    list_filter = ['name', 'desc', 'detail', 'learn_times', 'students', 'favour_number', 'image', 'click_number',
                   'add_time', 'degree']
    ordering = ['-click_number']
    readonly_fields = ['click_number', 'favour_number']
    inlines = [LessonInline, CourseResourceInline]

    def queryset(self):
        """
        重载该方法获取轮播课程数据
        :return: 
        """
        return super(CourseBannerAdmin, self).queryset().filter(is_banner=True)


xadmin.site.register(BannerCourse, CourseBannerAdmin)


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


xadmin.site.register(Lesson, LessonAdmin)


class VideoAdmin(object):
    list_display = ['name', 'add_time', 'lesson']
    search_fields = ['name', 'lesson']
    list_filters = ['name', 'add_time', 'lesson']


xadmin.site.register(Video, VideoAdmin)


class CourseResourceAdmin(object):
    list_display = ['name', 'course', 'download', 'add_time']
    list_filter = ['name', 'course__name', 'download', 'add_time']
    search_fields = ['name', 'course', 'download']


xadmin.site.register(CourseResource, CourseResourceAdmin)
