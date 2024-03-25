from django.contrib import admin
from .models import DemoClass, UserDemoClass

admin.site.register(DemoClass)
admin.site.register(UserDemoClass)
