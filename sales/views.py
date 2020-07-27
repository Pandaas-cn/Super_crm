import re
# import hashlib
from django.urls import reverse
from django import (forms)
from django.shortcuts import (
    render, HttpResponse, redirect
)
from django.views import View
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
            # 用户信息写入到Session
            request.session['user_id'] = user_obj.id
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


# 公私户信息查看
class CustomerView(View):

    def get(self, request, page=1):
        """
        客户信息查看
        :param request:
        :param page: 页码
        :return:
        """
        current_request_path = request.path

        user_id = request.session.get('user_id')
        if current_request_path.find(reverse('mycustomers')) == -1:
            customer_list = models.Customer.objects.filter(consultant__isnull=True)
            base_url = 'crm/customers'
            tag = '1'
        else:  # mycustomers 私户请求
            customer_list = models.Customer.objects.filter(consultant=request.user_obj)
            base_url = 'crm/mycustomers'
            tag = '2'
        kw = request.GET.get('keyword')  # 查询关键字
        sf = request.GET.get('search_field')  # 选择查询的字段
        get_data = request.GET.urlencode()
        # print('get_data=', get_data)
        if sf:
            sf = sf + '__contains'
        if kw:
            kw = kw.strip()
            customer_list = customer_list.filter(**{sf: kw})
        else:
            customer_list = customer_list
        customer_count = customer_list.count()
        per_page_num = 10
        per_num_show = 5
        mypage = MyPagenation(page, customer_count, per_page_num, per_num_show, base_url, get_data=get_data)
        page_html = mypage.page_html()
        try:
            customer_objs = customer_list.reverse()[mypage.start_num_show:mypage.end_num_show]
        except AssertionError as e:
            customer_objs = None
        context = {
            'customer_objs': customer_objs,
            'page_html': page_html,
            'tag': tag,
            # 'keyword': kw,
        }
        return render(request, 'salehtml/customers.html', context)

    def post(self, request, page=None):
        action = request.POST.get('action')
        if hasattr(self, action):
            res = getattr(self, action)(request, )
        if res is None:
            res = redirect(request.path)
        return res

    @staticmethod
    def reverse_gs(request, ):
        cids = request.POST.getlist('cids')
        # import --->>> django.db.transaction
        from django.db import transaction  # 导入事务
        with transaction.atomic():
            customers = models.Customer.objects.filter(pk__in=cids, consultant__isnull=True).select_for_update()
        if customers.count() != len(cids):
            return HttpResponse("手速不够-智商来凑-你猜猜这是什么意思？")
        customers.update(consultant_id=request.session.get('user_id'))

    @staticmethod
    def reverse_sg(request):
        cids = request.POST.getlist('cids')
        customers = models.Customer.objects.filter(pk__in=cids)
        customers.update(consultant_id=None)


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


def mycustomers(request):
    pass


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
            next_url = request.GET.get('next')
            if request.GET.get('next') is None:
                next_url = reverse('customers')
            return redirect(next_url)
        else:
            context = {
                'customer_form': customer_form,
                'pagetitle': pagetitle,
            }
            return render(request, 'salehtml/edit_customer.html', context)


class ConsultRecord(View):

    def get(self, request, page=1):

        cid = request.GET.get('cid')
        base_url = 'crm/consult_record'
        # 单条记录查询-单个客户跟进记录查看
        if cid:
            consult_list = models.ConsultRecord.objects.filter(consultant=request.user_obj, customer__id=cid,
                                                               delete_status=False).order_by('date')
        # 当前登录客户，未删除状态的记录
        else:
            consult_list = models.ConsultRecord.objects.filter(consultant=request.user_obj,
                                                               delete_status=False).order_by('date')

        kw = request.GET.get('keyword')  # 查询关键字
        sf = request.GET.get('search_field')  # 选择查询的字段
        get_data = request.GET.urlencode()
        # print('get_data=', get_data)
        if sf:
            sf = sf + '__contains'
        if kw:
            kw = kw.strip()
            customer_list = consult_list.filter(**{sf: kw})
        else:
            customer_list = consult_list
        customer_count = customer_list.count()
        per_page_num = 10
        per_num_show = 5
        mypage = MyPagenation(page, customer_count, per_page_num, per_num_show, base_url, get_data=get_data)
        page_html = mypage.page_html()
        try:
            consult_list = customer_list.reverse()[mypage.start_num_show:mypage.end_num_show]
        except AssertionError as e:
            consult_list = None
        context = {
            'consult_list': consult_list,
            'page_html': page_html,
            # 'keyword': kw,
        }
        # return render(request, 'salehtml/customers.html', context)

        return render(request, 'salehtml/consult_record.html', context)

    def post(self, request, page=1):
        action = request.POST.get('action')
        cids = request.POST.getlist('cids')
        if hasattr(self, action):
            consults = models.ConsultRecord.objects.filter(pk__in=cids)
            getattr(self, action)(request, consults)
            return redirect(request.path)

    def bulk_delete(self, request, consults):
        consults.update(delete_status=True)


class ConsultRecordForm(forms.ModelForm):
    class Meta:
        model = models.ConsultRecord
        fields = '__all__'
        exclude = ['delete_status']

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from django.forms.fields import DateField
        from multiselectfield.forms.fields import MultiSelectFormField
        for field_name, field in self.fields.items():
            if isinstance(field, DateField):
                field.widget.attrs.update({'type': 'date'})
            if isinstance(field, MultiSelectFormField):  # 如果是多选 不添加form-control 样式 否则显示有问题
                pass
            if field_name == 'customer':
                field.queryset = models.Customer.objects.filter(consultant=request.user_obj)
                field.widget.attrs.update({'class': 'form-control'})
            if field_name == 'consultant':
                field.queryset = models.UserInfo.objects.filter(pk=request.user_obj.pk)
                field.widget.attrs.update({'class': 'form-control'})
            else:
                field.widget.attrs.update({'class': 'form-control'})


class AddEditConsultView(View):

    def get(self, request, cid=None):
        pagetitle = '编辑客户' if cid else '添加客户'
        consult_obj = models.ConsultRecord.objects.filter(pk=cid).first()
        if request.method == 'GET':
            customer_model_form = ConsultRecordForm(request, instance=consult_obj)
            context = {
                'consult_form': customer_model_form,
                'pagetitle': pagetitle,
            }
            return render(request, 'salehtml/add_edit_consults.html', context)

    def post(self, request, cid=None):
        pagetitle = '编辑客户' if cid else '添加客户'
        consult_obj = models.ConsultRecord.objects.filter(pk=cid).first()
        consult_form = ConsultRecordForm(request, request.POST, instance=consult_obj)
        if consult_form.is_valid():
            consult_form.save()
            next_url = request.GET.get('next')
            if not next_url:
                next_url = reverse('consult_record')
            return redirect(next_url)
        else:
            context = {
                'consult_form': consult_form,
                'pagetitle': pagetitle,
            }
            return render(request, 'salehtml/add_edit_consults.html', context)


class DeleteConsultRecord(View):

    @staticmethod
    def get(request, cid=None):
        consults = models.ConsultRecord.objects.filter(pk=cid)
        consults.update(delete_status=True)
        next_url = request.GET.get('next')
        if not next_url:
            next_url = reverse('consult_record')
        return redirect(next_url)


class Enrollment(View):

    def get(self, request):
        enroll_objs = models.Enrollment.objects.filter(customer__consultant=request.user_obj, delete_status=False)
        context = {
            'enroll_objs': enroll_objs,
        }
        return render(request, 'salehtml/enrollment_record.html', context)


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = models.Enrollment
        fields = '__all__'
        exclude = ['delete_status']

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from django.forms.fields import DateField
        from multiselectfield.forms.fields import MultiSelectFormField
        for field_name, field in self.fields.items():
            if isinstance(field, DateField):
                field.widget.attrs.update({'type': 'date'})
            if isinstance(field, MultiSelectFormField):  # 如果是多选 不添加form-control 样式 否则显示有问题
                pass
            if field_name == 'customer':
                field.queryset = models.Customer.objects.filter(consultant=request.user_obj)
                field.widget.attrs.update({'class': 'form-control'})
            if field_name == 'consultant':
                field.queryset = models.UserInfo.objects.filter(pk=request.user_obj.pk)
                field.widget.attrs.update({'class': 'form-control'})
            else:
                field.widget.attrs.update({'class': 'form-control'})


class AddEditEnrollView(View):

    def get(self, request, cid=None):
        pagetitle = '编辑' if cid else '添加'
        enroll_obj = models.Enrollment.objects.filter(pk=cid).first()
        print(enroll_obj)
        if request.method == 'GET':
            customer_model_form = EnrollmentForm(request, instance=enroll_obj)
            context = {
                'consult_form': customer_model_form,
                'pagetitle': pagetitle,
            }
            return render(request, 'salehtml/add_edit_consults.html', context)

    def post(self, request, cid=None):
        pagetitle = '编辑客户' if cid else '添加客户'
        enroll_obj = models.Enrollment.objects.filter(pk=cid).first()
        consult_form = EnrollmentForm(request, request.POST, instance=enroll_obj)
        if consult_form.is_valid():
            consult_form.save()
            next_url = request.GET.get('next')
            if not next_url:
                next_url = reverse('enrollment')
            print(next_url)
            return redirect(next_url)
        else:
            print('consult_form is not vaild')
            context = {
                'consult_form': consult_form,
                'pagetitle': pagetitle,
            }
            return render(request, 'salehtml/add_edit_consults.html', context)


class CourseRecordView(View):

    def get(self, request):
        objs = models.CourseRecord.objects.all()
        context = {
            'course_objs': objs,
        }

        return render(request, 'salehtml/course_record.html', context)

    def post(self, request):
        action = request.POST.get('action')
        cids = request.POST.getlist('cids')
        print('action', action)
        print('cids', cids)
        if hasattr(self, action):
            getattr(self, action)(request, cids)
        return redirect(reverse('course_record'))

    def bulk_create_record(self, request, cids):  # 批量生成记录
        for cid in cids:
            course_record_obj = models.CourseRecord.objects.filter(pk=cid).first()
            print('course_record_obj', course_record_obj)
            students = course_record_obj.re_class.customer_set.filter(status='studying')
            objs_list = []
            for student in students:
                obj = models.StudyRecord(
                    course_record_id=cid,
                    student=student,
                )
                objs_list.append(obj)
            models.StudyRecord.objects.bulk_create(objs_list)

            # for student in students:
            #     models.StudyRecord.objects.create(
            #         course_record_id=cid,
            #         student=student,
            #     )



from django.forms import modelformset_factory


class StudyRecordModelForm(forms.ModelForm):
    class Meta:
        model = models.StudyRecord
        fields = '__all__'


class StudyRecordView(View):

    def get(self, request, course_record_id):
        query_set = models.StudyRecord.objects.filter(course_record_id=course_record_id)
        formset = modelformset_factory(model=models.StudyRecord, form=StudyRecordModelForm)
        formset = formset(queryset=query_set)
        context = {
            'formset': formset
        }

        return render(request, 'salehtml/study_record.html', context)