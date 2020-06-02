"""supercrm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from sales import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('home/',views.home,name='home'),
    #所有客户信息展示
    path('customers/', views.customers, name='customers'),
    path('customers/<int:page>/', views.customers, name='customers'),
    path('add_customer', views.add_edit_customer, name='add_customer'),
    #编辑客户
    path('edit_customer/<int:cid>/', views.add_edit_customer, name='edit_customer')
]