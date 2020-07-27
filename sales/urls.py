# -*- coding: utf-8 -*-
# @Time     :2020/7/6 12:01
# @Author   :12257
# @SoftWare :PyCharm

from django.contrib import admin
from django.urls import path
from sales import views
urlpatterns = [
    path('', views.login),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('home/',views.home,name='home'),
    #所有客户信息展示
    path('customers/', views.CustomerView.as_view(), name='customers'),
    path('mycustomers/', views.CustomerView.as_view(), name='mycustomers'),  # 私户客户信息
    path('mycustomers/<int:page>/', views.CustomerView.as_view(), name='mycustomers'),  # 私户客户信息
    path('customers/<int:page>/', views.CustomerView.as_view(), name='customers'),
    path('add_customer/', views.add_edit_customer, name='add_customer'),
    #编辑客户
    path('edit_customer/<int:cid>/', views.add_edit_customer, name='edit_customer'),
    # 跟进记录
    path('consult_record/', views.ConsultRecord.as_view(), name='consult_record'),
    path('consult_record/<int:page>/', views.ConsultRecord.as_view(), name='consult_record'),
    # 添加跟进记录
    path('add_consult_record/', views.AddEditConsultView.as_view(), name='add_consult'),
    path('edit_consult_record/<int:cid>/', views.AddEditConsultView.as_view(), name='edit_consult'),
    path('delete_consult_record/<int:cid>/', views.DeleteConsultRecord.as_view(), name='delete_consult'),
    path('enrollment/', views.Enrollment.as_view(), name='enrollment'),
    path('enrollment_add/', views.AddEditEnrollView.as_view(), name='enrollment_add'),
    path('enrollment_edit/<int:cid>', views.AddEditEnrollView.as_view(), name='enrollment_edit'),
    path('course_record/', views.CourseRecordView.as_view(), name='course_record'),
    path('study_record/', views.StudyRecordView.as_view(), name='study_record'),
    path('study_record/<int:course_record_id>', views.StudyRecordView.as_view(), name='study_record')

]
