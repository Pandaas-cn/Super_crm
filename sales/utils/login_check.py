# -*- coding: utf-8 -*-
# @Time     :2020/7/2 16:59
# @Author   :12257
# @SoftWare :PyCharm

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from sales import models


class UserAuth(MiddlewareMixin):

    @staticmethod
    def process_request(request):
        allow_list = [reverse('login'), reverse('register')]
        if request.path in allow_list:
            return
        user_id = request.session.get('user_id')
        if user_id:
            user_obj = models.UserInfo.objects.get(pk=user_id)
            request.user_obj = user_obj
            return
        else:
            return redirect('login')
