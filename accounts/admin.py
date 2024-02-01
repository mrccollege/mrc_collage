from django.contrib import admin
from .models import UserQuery, OtpVerify


# Register your models here.
class UserQueryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'created_at')


class OtpVerifyAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'otp', 'created_at')


admin.site.register(UserQuery, UserQueryAdmin)
admin.site.register(OtpVerify, OtpVerifyAdmin)
