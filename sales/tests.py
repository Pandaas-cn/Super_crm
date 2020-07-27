import re
from django.test import TestCase
from django.core.exceptions import ValidationError
# Create your tests here.
try:
    raise ValueError("错误的值")
except ValueError as err:
    print(err)
