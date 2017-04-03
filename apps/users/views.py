# -*- coding:utf-8 -*-
import json

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from pure_pagination import Paginator, PageNotAnInteger

# Create your views here.
from courses.models import Course
from operation.models import UserCourse, UserFavourite, UserMessage
from users.models import UserProfile, EmailVerifyRecord, Banner
from .forms import LoginForm, RegisterForm, ForgetForm, ResetForm, UploadImageForm, UserInfoForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin

from organization.models import CourseOrg, Teacher


class CustomBackend(ModelBackend):
    """重载authenticate,实现自定义后台账密验证,须在setting.py中添加"""

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # Q是or关系
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    """继承View方法，改写get和post方法"""

    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):

        # HTML表单预处理

        login_form = LoginForm(request.POST)
        # import pdb
        # pdb.set_trace()
        # 如果表单提交字段合法则验证账密
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=user_name, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': '用户未激活'})
            else:
                return render(request, 'login.html', {'msg': '用户名或者密码错误!'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户已经存在'})
            password = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(password=password)
            user_profile.save()

            # 发送注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = '欢迎注册慕学在线网'
            user_message.save()

            send_register_email(email=user_name, send_type='register')
            return render(request, 'login.html', {})
        else:
            return render(request, 'register.html', {'register_form': register_form})


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for records in all_records:
                email = records.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_field.html')
        return render(request, 'login.html')


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email=email, send_type='forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    def get(self, request, reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for records in all_records:
                email = records.email
                return render(request, 'password_reset.html', {"email": email})
        else:
            return render(request, 'active_field.html')
        return render(request, 'login.html')


class ModifyPwdView(View):
    """
    修改用户密码
    """

    def post(self, request):
        resete_form = ResetForm(request.POST)
        if resete_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'msg': '密码不一致', 'email': email})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(password=pwd1)
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get('password2', '')
            return render(request, 'password_reset.html', {'resete_form': resete_form})


class UserCenterView(View):
    def get(self, request):
        return render(request, 'usercenter-info.html')


class UserInfoView(LoginRequiredMixin, View):
    """
    用户个人信息
    """

    def get(self, request):
        return render(request, 'usercenter-info.html', {})

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return JsonResponse({'status': 'success'}, content_type='application/json')
        else:
            return JsonResponse(user_info_form.errors, content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    """
    用户修改头像
    """

    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return JsonResponse({'status': 'success'}, content_type='application/json')
        else:
            return JsonResponse({'status': 'fail'}, content_type='application/json')


class UpdatePWDView(View):
    """
    修改用户密码
    """

    def post(self, request):
        resete_form = ResetForm(request.POST)
        if resete_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'msg': '密码不一致'})
            user = request.user
            user.password = make_password(password=pwd1)
            user.save()
            return JsonResponse({'status': 'success'}, content_type='application/json')
        else:
            return JsonResponse(json.dumps(resete_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    """
    发送邮箱验证码
    """

    def get(self, reqeust):
        # import pdb
        # pdb.set_trace()
        email = reqeust.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return JsonResponse({'email': '邮箱已经存在'}, content_type='application/json')
        send_register_email(email=email, send_type='update_email')
        return JsonResponse({'status': 'success'}, content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    """
    修改个人邮箱
    """

    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        existed_record = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if existed_record:
            user = request.user
            user.email = email
            user.save()
            return JsonResponse({'email': '修改成功'}, content_type='application/json')
        else:
            return JsonResponse({'email': '验证码出错'}, content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    """
    我的课程
    """

    def get(self, request):
        all_course = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {'all_course': all_course,
                                                            })


class MyFavOrgView(LoginRequiredMixin, View):
    """
    我收藏的课程机构
    """

    def get(self, request):
        org_list = []
        all_fav_orgs = UserFavourite.objects.filter(user=request.user, fav_type=2)
        for fav_org in all_fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {'all_fav_orgs': all_fav_orgs,
                                                           'org_list': org_list,
                                                           })


class MyFavTeachersView(LoginRequiredMixin, View):
    """
    我收藏的授课教师
    """

    def get(self, request):
        org_teacher_list = []
        all_fav_teachers = UserFavourite.objects.filter(user=request.user, fav_type=3)
        for fav_org in all_fav_teachers:
            teacher_id = fav_org.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            org_teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {'all_fav_teachers': all_fav_teachers,
                                                               'org_teacher_list': org_teacher_list,
                                                               })


class MyFavCourseView(LoginRequiredMixin, View):
    """
    我收藏的课程
    """

    def get(self, request):
        course_list = []
        all_courses = UserFavourite.objects.filter(user=request.user, fav_type=1)
        for fav_org in all_courses:
            course_id = fav_org.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {'course_list': course_list, })


class MyMessageView(LoginRequiredMixin, View):
    """
    我的消息
    """

    def get(self, request):
        # import pdb
        # pdb.set_trace()
        all_messages = UserMessage.objects.filter(user=request.user.id)

        # 用户进入个人消息后清空个人消息
        all_unread_message = UserMessage.objects.filter(has_read=False, user=request.user.id)
        for unread_message in all_messages:
            unread_message.has_read = True
            unread_message.save()

        # 对个人消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_messages, 5, request=request)

        messages = p.page(page)

        return render(request, 'usercenter-message.html', {'all_messages': messages,
                                                           })


class LogoutView(View):
    """
    用户登出
    """

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class IndexView(View):
    """
    慕学在线网首页
    """

    def get(self, request):
        # 取出轮播图
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {'all_banners': all_banners,
                                              'courses': courses,
                                              'banner_courses': banner_courses,
                                              'course_org': course_orgs,
                                              })


def page_not_found(request):
    """
    全局404函数
    :param request: 
    :return: 
    """
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    """
    全局500函数
    :param request: 
    :return: 
    """
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
