from django.contrib import admin
from .models import UserQuery, OtpVerify, UserProfile


# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'mobile', 'first_name')
    list_filter = ('user', 'mobile', 'user__first_name')
    search_fields = ('user__username', 'mobile', 'user__first_name')

    def first_name(self, obj):
        return obj.user.first_name

# https://www.youtube.com/@mrcayurveda3775
# https://www.youtube.com/@DrAbhishekSharmaMRC

# https://www.facebook.com/mrc.aarogyam
# https://www.facebook.com/profile.php?id=1074279266


class UserQueryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'created_at')


class OtpVerifyAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'otp', 'created_at')


admin.site.register(UserQuery, UserQueryAdmin)
admin.site.register(OtpVerify, OtpVerifyAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
