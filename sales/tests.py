import re
from django.test import TestCase
from django.core.exceptions import ValidationError
# Create your tests here.
"""
作业：用两种方法创建字典，用来存放本小组织成员的通讯录
示例：b['李白']＝13401218989，并遍历输出
"""

mdict = dict(张浩然=110,张浩然2=120)
mdcit2 = {"张浩然3": "1101", "张浩然4": "2222"}
print(mdict)
print(mdcit2)
for item in mdict.items():
    print(item)