# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.db.models import Q

from pure_pagination import Paginator, PageNotAnInteger

from courses.models import Course
from .models import CourseOrg, CityDict, Teacher
from .form import UserAskForm
from operation.models import UserFavourite
import json


# Create your views here.

class OrgView(View):
    """
    课程机构列表功能
    """

    def get(self, request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()
        org_numbers = all_orgs.count()
        # 城市
        all_citys = CityDict.objects.all()

        # 机构搜索
        search_keywords = request.GET.get("keywords", '')
        if search_keywords:
            all_orgs = all_orgs.filter(
                Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))

        hot_orgs = all_orgs.order_by("-click_nums")[:3]

        # 取出筛选城市
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 类别率选
        category = request.GET.get('ct', '')
        if category:
            all_orgs.filter(category=category)

        # 排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students')
            elif sort == 'course':
                all_orgs = all_orgs.order_by('-courses_nums')

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_orgs, 5, request=request)

        orgs = p.page(page)

        return render(request, 'org-list.html', {
            'all_orgs': orgs,
            'all_citys': all_citys,
            'count': all_orgs.count(),
            'city_id': city_id,
            'category': category,
            'hot_orgs': hot_orgs,
            'sort': sort,
        })


class AddUserAskView(View):
    """用户添加咨询"""

    def post(self, request):
        print request.POST.get('name')
        print request.POST.get('mobile')
        print request.POST.get('course_name')
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            userask_form.save(commit=True)
            return HttpResponse(json.dumps("{'status':'success'}"), content_type='application/json')
        else:
            print userask_form.is_valid()
            return JsonResponse({'status': 'fail', 'msg': '提交出错'}, content_type='application/json')


class OrgHomeView(View):
    """机构首页"""

    def get(self, request, org_id):
        current_page = 'home'
        has_fav = False
        if request.user.is_authenticated():
            if UserFavourite.objects.filter(user=request.user, fav_id=org_id, fav_type=2):
                has_fav = True
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        all_courses = course_org.course_set.all()[:3]
        all_teacher = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {'all_courses': all_courses,
                                                            'all_teachers': all_teacher,
                                                            'org_id': org_id,
                                                            'current_page': current_page,
                                                            'has_fav': has_fav})


class OrgCourseView(View):
    """课程首页"""

    def get(self, request, org_id):
        current_page = 'course'
        has_fav = False
        if request.user.is_authenticated():
            if UserFavourite.objects.filter(user=request.user, fav_id=org_id, fav_type=2):
                has_fav = True
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'org_id': org_id,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgDescView(View):
    """机构介绍页"""

    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavourite.objects.filter(user=request.user, fav_id=org_id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            'org_id': org_id,
            'has_fav': has_fav,
        })


class OrgTeacherView(View):
    """机构教师页"""

    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavourite.objects.filter(user=request.user, fav_id=org_id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'course_org': course_org,
            'org_id': org_id,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class AddFavView(View):
    """用户收藏,用户取消收藏"""

    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        # 判断用户登录状态
        if not request.user.is_authenticated():
            return HttpResponse("{'status':'fail','msg':'用户未登录'}", content_type='application/json')

        exist_records = UserFavourite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))

        if exist_records:
            # 如果记录存在，则表示用户取消收藏
            exist_records.delete()
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.favour_number -= 1
                if course.favour_number < 0:
                    course.favour_number = 0
                course.save()
            elif int(fav_type) == 2:
                org = CourseOrg.objects.get(id=int(fav_id))
                org.fav_nums -= 1
                if org.fav_nums < 0:
                    org.fav_nums = 0
                org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()

            return HttpResponse("{'status':'fail','msg':'收藏'}", content_type='application/json')
        else:
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav = UserFavourite.objects.create(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))

                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.favour_number += 1
                    course.save()
                elif int(fav_type) == 2:
                    org = CourseOrg.objects.get(id=int(fav_id))
                    org.fav_nums += 1
                    org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()

                user_fav.save()
                return JsonResponse({'status': 'success', 'msg': '已收藏'}, content_type='application/json')
            else:
                return JsonResponse({'status': 'fail', 'msg': '收藏出错'}, content_type='application/json')


class TeacherListView(View):
    # 课程讲师列表页
    def get(self, request):
        all_teacher = Teacher.objects.all()

        # 教师搜索
        search_keywords = request.GET.get("keywords", '')
        if search_keywords:
            all_teacher = all_teacher.filter(
                Q(name__icontains=search_keywords) | Q(work_company__icontains=search_keywords) | Q(
                    work_position__icontains=search_keywords))

        sort = request.GET.get('sort', '')
        if sort:
            if sort == "hot":
                all_teacher = all_teacher.order_by('-click_nums')

        sorted_teachers = Teacher.objects.all().order_by(('-click_nums'))[:3]

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_teacher, 1, request=request)

        teachers = p.page(page)

        return render(request, 'teachers-list.html', {'all_teacher': teachers,
                                                      'sorted_teachers': sorted_teachers,
                                                      'sort': sort,
                                                      })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()

        all_courses = Course.objects.filter(teacher=teacher)

        has_teacher_fav = False
        has_org_fav = False

        if UserFavourite.objects.filter(user=request.user, fav_type=3, fav_id=int(teacher.id)):
            has_teacher_fav = True

        if UserFavourite.objects.filter(user=request.user, fav_type=2, fav_id=int(teacher.org.id)):
            has_org_fav = True

        # 讲师排行
        sorted_teachers = Teacher.objects.all().order_by(('-click_nums'))[:3]
        return render(request, 'teacher-detail.html', {"teacher": teacher,
                                                       'all_courses': all_courses,
                                                       'sorted_teachers': sorted_teachers,
                                                       'has_teacher_fav': has_teacher_fav,
                                                       'has_org_fav': has_org_fav,
                                                       })
