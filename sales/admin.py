from django.contrib import admin
from sales import models
# Register your models here.

admin.site.register(models.Customer)
admin.site.register(models.ClassList)
admin.site.register(models.UserInfo)
admin.site.register(models.Campuses)
