# -*- coding:utf-8 -*-
__author__ = 'jianzhihao'
__date__ = '17-3-5 下午8:55'
from random import Random
from django.core.mail import send_mail
from MXonline.settings import EMAIL_FROM

from users.models import EmailVerifyRecord


def send_register_email(email, send_type='register'):
    """发送邮箱验证码"""
    email_record = EmailVerifyRecord()
    code = generate_random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ''
    email_body = ''

    if send_type == 'register':
        email_title = '慕学在线网注册激活链接'
        email_body = '点击下面的链接激活你的账号:http://127.0.0.1:8000/active/{0}'.format(code)
        send_status = send_mail(subject=email_title, message=email_body, from_email=EMAIL_FROM, recipient_list=[email])
        if send_status:
            pass
    elif send_type == 'forget':
        email_title = '慕学在线网找回密码链接'
        email_body = '点击下面的链接找回你的密码:http://127.0.0.1:8000/reset/{0}'.format(code)
        print email_body
    elif send_type == 'update_email':
        email_title = '慕学在线网修改验证码'
        email_body = '你的邮箱验证码为:http://127.0.0.1:8000/reset/{0}'.format(code)
        print email_body

def generate_random_str(random_lenth=8):
    """随机产生字符串"""
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz1234567890'
    length = len(chars) - 1
    for i in range(length):
        str += chars[Random().randint(0, length)]

    return str
