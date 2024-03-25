from django.contrib import admin
from .models import DemoCourseCategory, DemoCourse, DemoClass, UserDemoCourse, UserDemoClass

# Register your models here.

admin.site.register(DemoCourseCategory)
admin.site.register(DemoCourse)
admin.site.register(DemoClass)

admin.site.register(UserDemoCourse)
admin.site.register(UserDemoClass)
