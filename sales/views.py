import re
# import hashlib
from django import (forms)
from django.shortcuts import (
    render, HttpResponse, redirect
)
from django.core.exceptions import ValidationError
from django.db.models import Q
from sales import models
from sales.utils.hashlib_func import set_md5
from sales.utils.page import MyPagenation


# Create your views here.

def mobile_validate(value):
    mobile_re = re.compile(r'0?(13|14|15|17|18|19)[0-9]{9}')
    if mobile_re.match(value) is None:
        raise ValidationError('手机号码格式有误')


class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=16,
        min_length=6,
        label='用户名',
        widget=forms.widgets.TextInput(attrs={'class': 'username', 'autocomplete': 'off', 'placeholder': '请输入用户名'}),
        error_messages={'required': '请输入用户名',
                        'max_length': '用户名不能大于16位',
                        'min_length': '用户名不能小于6位', })
    password = forms.CharField(
        max_length=32,
        min_length=6,
        label='密码',
        widget=forms.widgets.PasswordInput(
            attrs={'class': 'password', 'oncontextmenu': 'return false', 'onpaste': 'return false',
                   'placeholder': '请输入密码'}),
        error_messages={'required': '请输入密码',
                        'max_length': '密码不能大于32位',
                        'min_length': '密码不能小于6位', })
    r_password = forms.CharField(
        label='确认密码',
        widget=forms.widgets.PasswordInput(
            attrs={'class': 'password', 'oncontextmenu': 'return false', 'onpaste': 'return false',
                   'placeholder': '确认密码'}),
        error_messages={'required': '请再次输入密码'}
    )

    telephone = forms.CharField(
        label='电话号码',
        validators=[mobile_validate, ],
        widget=forms.widgets.TextInput(attrs={'placeholder': '请输入手机号码', 'class': 'phone_number',
                                              'autocomplete': 'off', 'id': 'number'}),
        error_messages={'required': '请输入手机号码'}
    )

    email = forms.EmailField(
        label='邮箱',
        widget=forms.widgets.TextInput(attrs={'placeholder': '请输入邮箱', 'class': 'email', 'type': 'email'}),
        error_messages={
            'required': '请输入邮箱',
            'invalid': '邮箱输入有误'}
        # validators=
    )

    def clean(self):
        values = self.cleaned_data
        password = values.get('password')
        r_password = values.get('r_password')
        if password == r_password:
            return values
        else:
            self.add_error('r_password', '两次密码输入不一致')


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = models.UserInfo.objects.filter(username=username, password=set_md5(password)).first()
        if user_obj is None:
            return render(request, 'login.html', {'error_msg': '用户名或密码错误'})
        else:
            return redirect('customers')


# 注册功能
def register(request):
    """
    注册功能
    :param request:
    :return:
    """
    if request.method == 'GET':
        register_form_obj = RegisterForm()
        return render(request, 'register.html', {'register_form_obj': register_form_obj})
    elif request.method == 'POST':
        register_form_obj = RegisterForm(request.POST)
        if register_form_obj.is_valid():
            # print(register_form_obj.cleaned_data)
            register_form_obj.cleaned_data.pop('r_password')
            password = register_form_obj.cleaned_data.pop('password')
            # 对密码进行加密
            password = set_md5(password)
            register_form_obj.cleaned_data.update({'password': password})
            models.UserInfo.objects.create(**register_form_obj.cleaned_data)
            return redirect('login')
        else:
            return render(request, 'register.html', {'register_form_obj': register_form_obj})


def home(request):
    return render(request, 'salehtml/home.html')


def customers(request, page=1):
    """
    客户信息查看
    :param request:
    :param page: 页码
    :return:
    """
    kw = request.GET.get('keyword')         # 查询关键字
    sf = request.GET.get('search_field')   # 选择查询的字段
    get_data = request.GET.urlencode()
    # print('get_data=', get_data)
    if sf:
        sf = sf + '__contains'
    if kw:
        customer_list = models.Customer.objects.filter(**{sf: kw})
    else:
        customer_list = models.Customer.objects.all()
    customer_count = customer_list.count()
    per_page_num = 10
    per_num_show = 5
    base_url = 'customers'
    mypage = MyPagenation(page, customer_count, per_page_num, per_num_show, base_url,get_data=get_data)
    page_html = mypage.page_html()
    customer_objs = customer_list.reverse()[mypage.start_num_show:mypage.end_num_show]
    context = {
        'customer_objs': customer_objs,
        'page_html': page_html,
        # 'keyword': kw,
    }
    return render(request, 'salehtml/customers.html', context)


class CustomerForm(forms.ModelForm):
    class Meta():
        model = models.Customer
        fields = '__all__'
        ordering = ['id', ]
        error_messages = {
            'qq': {'required': '不能为空'},
            'course': {'required': '不能为空'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from django.forms.fields import DateField
        from multiselectfield.forms.fields import MultiSelectFormField
        for field_name, field in self.fields.items():
            if isinstance(field, DateField):
                field.widget.attrs.update({'type': 'date'})
            if isinstance(field, MultiSelectFormField):  # 如果是多选 不添加form-control 样式 否则显示有问题
                # field.widget.attrs.update({'type': ''})
                pass
            else:
                field.widget.attrs.update({'class': 'form-control'})


# def add_customer(request):
#     if request.method == 'GET':
#         customer_form = CustomerForm()
#         return render(request, 'salehtml/add_customer.html', {'customer_form': customer_form})
#     else:
#         customer_form = CustomerForm(request.POST)
#         if customer_form.is_valid():
#             customer_form.save()
#             return redirect('customers')
#         else:
#             return render(request, 'salehtml/add_customer.html', {'customer_form': customer_form})


# def edit_customer(request, cid):
#     """
#     编辑客户信息
#     :param request:
#     :param cid: 客户记录id
#     :return:
#     """
#
#     customers_obj = models.Customer.objects.filter(pk=cid).first()
#     if request.method == 'GET':
#         customer_model_form = CustomerForm(instance=customers_obj)
#         context = {
#             'customer_form': customer_model_form
#         }
#         return render(request, 'salehtml/edit_customer.html', context)
#     else:
#         customer_form = CustomerForm(request.POST, instance=customers_obj)
#         if customer_form.is_valid():
#             customer_form.save()
#             return redirect('customers')
#         else:
#             context = {
#                 'customer_form': customer_form
#             }
#             return render(request, 'salehtml/edit_customer.html', context)


def add_edit_customer(request, cid=None):
    pagetitle = '编辑客户' if cid else '添加客户'
    customer_obj = models.Customer.objects.filter(pk=cid).first()
    if request.method == 'GET':
        customer_model_form = CustomerForm(instance=customer_obj)
        context = {
            'customer_form': customer_model_form,
            'pagetitle': pagetitle,
        }
        return render(request, 'salehtml/edit_customer.html', context)
    else:
        customer_form = CustomerForm(request.POST, instance=customer_obj)
        if customer_form.is_valid():
            customer_form.save()
            return redirect('customers')
        else:
            context = {
                'customer_form': customer_form,
                'pagetitle': pagetitle,
            }
            return render(request, 'salehtml/edit_customer.html', context)