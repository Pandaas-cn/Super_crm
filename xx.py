# -*- coding: utf-8 -*-
# @Time     :2020/5/22 17:45
# @Author   :12257
# @SoftWare :PyCharm
"""
插入数据测试-外部文件使用Django-Models
"""
import os
import random

source_type = (('qq', "qq群"),
               ('referral', "内部转介绍"),
               ('website', "官方网站"),
               ('baidu_ads', "百度推广"),
               ('office_direct', "直接上门"),
               ('WoM', "口碑"),
               ('public_class', "公开课"),
               ('website_luffy', "路飞官网"),
               ('others', "其它"),)

course_choices = (('LinuxL', 'Linux中高级'),
                  ('PythonFullStack', 'Python高级全栈开发'),)

if __name__ == '__main__':
    # global source_type
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "supercrm.settings")
    import django

    django.setup()
    from sales import models
    obj_list = []
    for i in range(251):
        d = {
            'qq': str(11111 + i),
            'name': f'dz技师{i}号',
            'source': source_type[random.randint(0, 8)][0],
            'course': course_choices[random.randint(0,1)][0],
        }
        obj = models.Customer(**d)
        obj_list.append(obj)
    models.Customer.objects.bulk_create(obj_list)