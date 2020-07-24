from django.db import models
from multiselectfield import MultiSelectField
from django.utils.safestring import mark_safe
# Create your models here.

course_choices = (('LinuxL', 'Linux中高级'),
                  ('PythonFullStack', 'Python高级全栈开发'),)

class_type_choices = (('fulltime', '脱产班',),
                      ('online', '网络班'),
                      ('weekend', '周末班',),)

source_type = (('qq', "qq群"),
               ('referral', "内部转介绍"),
               ('website', "官方网站"),
               ('baidu_ads', "百度推广"),
               ('office_direct', "直接上门"),
               ('WoM', "口碑"),
               ('public_class', "公开课"),
               ('website_luffy', "路飞官网"),
               ('others', "其它"),)

enroll_status_choices = (('signed', "已报名"),
                         ('unregistered', "未报名"),
                         ('studying', '学习中'),
                         ('paid_in_full', "学费已交齐"))

seek_status_choices = (('A', '近期无报名计划'), ('B', '1个月内报名'), ('C', '2周内报名'), ('D', '1周内报名'),
                       ('E', '定金'), ('F', '到班'), ('G', '全款'), ('H', '无效'),)
pay_type_choices = (('deposit', "订金/报名费"),
                    ('tuition', "学费"),
                    ('transfer', "转班"),
                    ('dropout', "退学"),
                    ('refund', "退款"),)

attendance_choices = (('checked', "已签到"),
                      ('vacate', "请假"),
                      ('late', "迟到"),
                      ('absence', "缺勤"),
                      ('leave_early', "早退"),)

score_choices = ((100, 'A+'),
                 (90, 'A'),
                 (85, 'B+'),
                 (80, 'B'),
                 (70, 'B-'),
                 (60, 'C+'),
                 (50, 'C'),
                 (40, 'C-'),
                 (0, ' D'),
                 (-1, 'N/A'),
                 (-100, 'COPY'),
                 (-1000, 'FAIL'),)


class UserInfo(models.Model):
    """
    用户表：
    """
    username = models.CharField(max_length=16)
    password = models.CharField(max_length=32)
    email = models.EmailField()
    telephone = models.CharField(max_length=16)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username

class Customer(models.Model):
    """
    客户表（最开始的时候大家都是客户，销售就不停的撩你，你还没交钱就是个客户）
    """
    qq = models.CharField(verbose_name='QQ', max_length=64, unique=True, help_text='QQ号必须唯一')
    qq_name = models.CharField('QQ昵称', max_length=64, blank=True, null=True)  # requierd:False
    name = models.CharField('姓名', max_length=32, blank=True, null=True,
                            help_text='学员报名后，请改为真实姓名')  # 可为空，有些人就不愿意给自己的真实姓名
    sex_type = (('male', '男'), ('female', '女'))  #
    sex = models.CharField("性别", choices=sex_type, max_length=16, default='male', blank=True,
                           null=True)  # 存的是male或者female，字符串
    birthday = models.DateField('出生日期', default=None, help_text="格式yyyy-mm-dd", blank=True, null=True)
    phone = models.BigIntegerField('手机号', blank=True, null=True)  # 手机号改成字符串的，不然不好搜索
    # phone = models.CharField('手机号', blank=True, null=True)
    source = models.CharField('客户来源', max_length=64, choices=source_type, default='qq')

    introduce_from = models.ForeignKey('self', verbose_name="转介绍自学员", blank=True, null=True,
                                       on_delete=models.CASCADE)  # self指的就是自己这个表，和下面写法是一样的效果
    # '''
    # id  name introduce_from
    # 1   dz   None
    # 2   xf   1
    # 3   cg   1
    #
    # '''

    # introduce_from = models.ForeignKey('Customer', verbose_name="转介绍自学员", blank=True, null=True,on_delete=models.CASCADE)
    course = MultiSelectField("咨询课程", choices=course_choices)  # 多选，并且存成一个列表的格式,通过modelform来用的时候，会成为一个多选框

    # course = models.CharField("咨询课程", choices=course_choices) #如果你不想用上面的多选功能，可以使用Charfield来存
    class_type = models.CharField("班级类型", max_length=64, choices=class_type_choices, default='fulltime')
    customer_note = models.TextField("客户备注", blank=True, null=True, )
    status = models.CharField("状态", choices=enroll_status_choices, max_length=64, default="unregistered",
                              help_text="选择客户此时的状态")  # help_text这种参数基本都是针对admin应用里面用的

    date = models.DateTimeField("咨询日期", auto_now_add=True)  # 这个没啥用昂，我问销售，销售说是为了一周年的时候给客户发一个祝福信息啥的
    last_consult_date = models.DateField("最后跟进日期", auto_now_add=True)  # 考核销售的跟进情况，如果多天没有跟进，会影响销售的绩效等
    next_date = models.DateField("预计再次跟进时间", blank=True, null=True)  # 销售自己大概记录一下自己下一次会什么时候跟进，也没啥用

    # 用户表中存放的是自己公司的所有员工。
    consultant = models.ForeignKey('UserInfo', verbose_name="销售", related_name='customers', blank=True, null=True,
                                   on_delete=models.CASCADE)

    # 一个客户可以报多个班，报个脱产班，再报个周末班等，所以是多对多。
    class_list = models.ManyToManyField('ClassList', verbose_name="已报班级", blank=True)

    class Meta:
        ordering = ['id', ]
        verbose_name = '客户信息表'
        verbose_name_plural = '客户信息表'

    def __str__(self):
        return self.name + ":" + self.qq

    enroll_status_choices = (('signed', "已报名"),
                             ('unregistered', "未报名"),
                             ('studying', '学习中'),
                             ('paid_in_full', "学费已交齐"))

    def status_show(self):
        status_color = {
            'paid_in_full': 'lightgreen',
            'unregistered': 'pink',
            'studying': 'lightblue',
            'signed': 'yellow',
        }

        return mark_safe("<span style='background-color:{0}'>{1}</span>".format(status_color[self.status],
                                                                                self.get_status_display()))
    # def get_classlist(self):  #当我们通过self.get_classlist的时候，就拿到了所有的班级信息，前端显示的时候用
    #
    #     l=[]
    #     for cls in self.class_list.all():
    #         l.append(str(cls))
    #     return mark_safe(",".join(l)) #纯文本，不用mark_safe也可以昂


class Campuses(models.Model):
    """
    校区表
    """
    name = models.CharField(verbose_name='校区', max_length=64)
    address = models.CharField(verbose_name='详细地址', max_length=512, blank=True, null=True)

    def __str__(self):
        return self.name


class ClassList(models.Model):
    """
    班级表
    """
    course = models.CharField("课程名称", max_length=64, choices=course_choices)
    semester = models.IntegerField("学期")  # python20期等
    campuses = models.ForeignKey('Campuses', verbose_name="校区", on_delete=models.CASCADE)
    price = models.IntegerField("学费", default=10000)
    memo = models.CharField('说明', blank=True, null=True, max_length=100)
    start_date = models.DateField("开班日期")
    graduate_date = models.DateField("结业日期", blank=True, null=True)  # 不一定什么时候结业，哈哈，所以可为空

    # contract = models.ForeignKey('ContractTemplate', verbose_name="选择合同模版", blank=True, null=True,on_delete=models.CASCADE)
    teachers = models.ManyToManyField('UserInfo',
                                      verbose_name="老师")  # 对了，还有一点，如果你用的django2版本的，那么外键字段都需要自行写上on_delete=models.CASCADE

    class_type = models.CharField(choices=class_type_choices, max_length=64, verbose_name='班额及类型', blank=True,
                                  null=True)

    class Meta:
        unique_together = ("course", "semester", 'campuses')

    def __str__(self):
        return "{}{}({})".format(self.get_course_display(), self.semester, self.campuses)


############################下面的表以后再说#################################

# class ContractTemplate(models.Model):
#     """
#     合同模板表
#     """
#     name = models.CharField("合同名称", max_length=128, unique=True)
#     content = models.TextField("合同内容")
#     date = models.DateField(auto_now=True)
#
#

class ConsultRecord(models.Model):
    """
    跟进记录表
    """
    customer = models.ForeignKey('Customer', verbose_name="所咨询客户",on_delete=models.CASCADE)
    note = models.TextField(verbose_name="跟进内容...")
    status = models.CharField("跟进状态", max_length=8, choices=seek_status_choices, help_text="选择客户此时的状态")
    consultant = models.ForeignKey("UserInfo", verbose_name="跟进人", related_name='records',on_delete=models.CASCADE)
    date = models.DateTimeField("跟进日期", auto_now_add=True)
    delete_status = models.BooleanField(verbose_name='删除状态', default=False)

    def __str__(self):
        return self.customer

class Enrollment(models.Model):
    """
    报名表
    """
    why_us = models.TextField("为什么报名", max_length=1024, default=None, blank=True, null=True)
    your_expectation = models.TextField("学完想达到的具体期望", max_length=1024, blank=True, null=True)
    # contract_agreed = models.BooleanField("我已认真阅读完培训协议并同意全部协议内容", default=False)
    contract_approved = models.BooleanField("审批通过", help_text="在审阅完学员的资料无误后勾选此项,合同即生效", default=False)
    enrolled_date = models.DateTimeField(auto_now_add=True, verbose_name="报名日期")
    memo = models.TextField('备注', blank=True, null=True)
    delete_status = models.BooleanField(verbose_name='删除状态', default=False)
    customer = models.ForeignKey('Customer', verbose_name='客户名称',on_delete=models.CASCADE)
    school = models.ForeignKey('Campuses',on_delete=models.CASCADE)
    enrolment_class = models.ForeignKey("ClassList", verbose_name="所报班级",on_delete=models.CASCADE)

    class Meta:
        unique_together = ('enrolment_class', 'customer')

    def __str__(self):
        return self.customer.name


# class PaymentRecord(models.Model):
#     """
#     缴费记录表
#     """
#     pay_type = models.CharField("费用类型", choices=pay_type_choices, max_length=64, default="deposit")
#     paid_fee = models.IntegerField("费用数额", default=0)
#     note = models.TextField("备注", blank=True, null=True)
#     date = models.DateTimeField("交款日期", auto_now_add=True)
#     course = models.CharField("课程名", choices=course_choices, max_length=64, blank=True, null=True, default='N/A')
#     class_type = models.CharField("班级类型", choices=class_type_choices, max_length=64, blank=True, null=True,
#                                   default='N/A')
#     enrolment_class = models.ForeignKey('ClassList', verbose_name='所报班级', blank=True, null=True)
#     customer = models.ForeignKey('Customer', verbose_name="客户")
#     consultant = models.ForeignKey('UserProfile', verbose_name="销售")
#     delete_status = models.BooleanField(verbose_name='删除状态', default=False)
#
#     status_choices = (
#         (1, '未审核'),
#         (2, '已审核'),
#     )
#     status = models.IntegerField(verbose_name='审核', default=1, choices=status_choices)
#
#     confirm_date = models.DateTimeField(verbose_name="确认日期", null=True, blank=True)
#     confirm_user = models.ForeignKey(verbose_name="确认人", to='UserProfile', related_name='confirms', null=True,
#                                      blank=True)
#
#

# course_record_id   student   考勤   本节成绩   homework_note
# #  1                 74       crm          跟进记录操作   1  迟到    60          写的很好
# #  1                 74       crm          跟进记录操作   2  签到    80          写的非常好
# #
# # id 节次   本节课程标题   本节课程内容
# # 1 74       crm          跟进记录操作


class CourseRecord(models.Model):
    """课程记录表"""
    day_num = models.IntegerField("节次", help_text="此处填写第几节课或第几天课程...,必须为数字")
    date = models.DateField(auto_now_add=True, verbose_name="上课日期")
    course_title = models.CharField('本节课程标题', max_length=64, blank=True, null=True)
    course_memo = models.TextField('本节课程内容', max_length=300, blank=True, null=True)
    has_homework = models.BooleanField(default=True, verbose_name="本节有作业")
    homework_title = models.CharField('本节作业标题', max_length=64, blank=True, null=True)
    homework_memo = models.TextField('作业描述', max_length=500, blank=True, null=True)
    scoring_point = models.TextField('得分点', max_length=300, blank=True, null=True)

    re_class = models.ForeignKey('ClassList', verbose_name="班级",on_delete=models.CASCADE)
    teacher = models.ForeignKey('UserInfo', verbose_name="讲师",on_delete=models.CASCADE)

    class Meta:
        unique_together = ('re_class', 'day_num')


class StudyRecord(models.Model):
    """
    学习记录
    """

    attendance = models.CharField("考勤", choices=attendance_choices, default="checked", max_length=64)
    score = models.IntegerField("本节成绩", choices=score_choices, default=-1)
    homework_note = models.CharField(max_length=255, verbose_name='作业批语', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    note = models.CharField("备注", max_length=255, blank=True, null=True)
    homework = models.FileField(verbose_name='作业文件', blank=True, null=True, default=None)
    course_record = models.ForeignKey('CourseRecord', verbose_name="某节课程",on_delete=models.CASCADE)
    student = models.ForeignKey('Customer', verbose_name="学员",on_delete=models.CASCADE)

    class Meta:
        unique_together = ('course_record', 'student')
