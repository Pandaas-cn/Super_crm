# -*- coding: utf-8 -*-
# @Time     :2020/7/2 13:30
# @Author   :12257
# @SoftWare :PyCharm
from django.urls import reverse
from django import template
from django.http.request import QueryDict

register = template.Library()


@register.simple_tag
def resole_url(request, url_name, customer_pk):
    next_url = request.get_full_path()
    # print('next_url==>',next_url)
    reverse_url = reverse(url_name, args=(customer_pk,))
    # print(full_url)
    q = QueryDict(mutable=True)
    q['next'] = next_url
    next_url = q.urlencode()
    full_url = reverse_url + '?' + next_url
    return full_url
