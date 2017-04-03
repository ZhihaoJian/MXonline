# -*- coding:utf-8 -*-
__author__ = 'jianzhihao'
__date__ = '17-3-2 上午11:09'

import xadmin
from .models import CourseOrg, Teacher, CityDict


class CityAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


xadmin.site.register(CityDict, CityAdmin)


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'image', 'address', 'city', 'add_time', 'click_nums', 'fav_nums']
    search_fields = ['name', 'desc', 'image', 'address', 'city', 'click_nums', 'fav_nums']
    list_filter = ['name', 'desc', 'image', 'address', 'city', 'add_time', 'click_nums', 'fav_nums']
    relfield_style = 'fk-ajax'


xadmin.site.register(CourseOrg, CourseOrgAdmin)


class TeacherAdmin(object):
    list_display = ['name', 'org', 'work_years', 'work_company', 'work_position', 'points', 'click_nums',
                    'fav_nums', 'add_time']
    search_fields = ['name', 'org', 'work_years', 'work_company', 'work_position', 'points', 'click_nums',
                     'fav_nums']
    list_filter = ['name', 'org', 'work_years', 'work_company', 'work_position', 'points', 'click_nums',
                   'fav_nums', 'add_time']


xadmin.site.register(Teacher, TeacherAdmin)
