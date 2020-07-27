# -*- coding: utf-8 -*-
# @Time     :2020/5/20 15:35
# @Author   :12257
# @SoftWare :PyCharm
import hashlib


def set_md5(values):
    """
    MD5加密
    :param values:需要被加密的数据
    :return:
    """
    secret_key = 'username'.encode('utf-8')
    md5_value = hashlib.md5(secret_key)
    md5_value.update(values.encode('utf-8'))
    return md5_value.hexdigest()


print(set_md5('123123'))
