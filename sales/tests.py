import re
from django.test import TestCase
from django.core.exceptions import ValidationError

# Create your tests here.
#
#
# def mobile_validate(value):
#     mobile_re = re.compile(r'0?(13|14|15|17|18|19)[0-9]{9}')
#     if mobile_re.match(value) is None:
#         raise ValidationError('手机号码格式有误')
#     else:
#         return 'ok'
#
#
# ret = mobile_validate('1836092357')
# print(ret)

# vars = input('请一次性输入三边长，以空格分隔').split()
# vars = [int(var) for var in vars]
# s = sum(vars) / 2
# print('三角形面积为：', (s * (s - vars[0]) * (s - vars[1]) * (s - vars[2])) ** 0.5)

import requests
import random
import time
user_agent_list = ["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/61.0",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",]
url = 'http://f15hdocgd.xtwvane.cn/ajax.php'
haeders = {
    'User-Agent' : random.choice(user_agent_list),
    'Connection' : 'close'
}
proxies = {'http':'223.243.5.79:4216','http':'223.241.6.185:4216'}
for i in range(10000):
    # res = requests.get('http://psb3mchc.1r6q1imo.notebook.f3322.net:678/cdcd.php?wf0mcu.xml')
    # print(res.cookies)
    print(haeders)
    data = {
        'u' : f'1335896{i}',
        'p' : f'wew22{i}'
    }
    requests.DEFAULT_RETRIES = 5
    res = requests.post(url=url,headers=haeders,data=data,proxies=proxies)
    print(res.status_code)
    # time.sleep(5)