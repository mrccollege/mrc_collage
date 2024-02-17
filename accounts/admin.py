from django.contrib import admin
from .models import UserQuery, OtpVerify, UserProfile


# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'mobile', 'get_username')
    list_filter = ('user',)
    search_fields = ('user__username', 'mobile')

    def get_username(self, obj):
        return obj.user.username


class UserQueryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'created_at')


class OtpVerifyAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'otp', 'created_at')


admin.site.register(UserQuery, UserQueryAdmin)
admin.site.register(OtpVerify, OtpVerifyAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
