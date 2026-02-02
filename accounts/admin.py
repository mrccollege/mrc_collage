from django.contrib import admin
from .models import UserQuery, OtpVerify, UserProfile


# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_first_name', 'get_address', 'created_at')
    list_filter = ('user', 'mobile', 'user__first_name', 'created_at')
    search_fields = ('user__username', 'mobile', 'user__first_name', 'created_at')

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'First Name'

    def get_address(self, obj):
        return obj.address
    get_address.short_description = 'Address'

    # def get_address(self, obj):
    #     return obj.address
    # get_address.short_description = 'Address'

# https://www.youtube.com/@mrcayurveda3775
# https://www.youtube.com/@DrAbhishekSharmaMRC

# https://www.facebook.com/mrc.aarogyam
# https://www.facebook.com/profile.php?id=1074279266


class UserQueryAdmin(admin.ModelAdmin):
    list_display = ('name', 'whatsapp', 'message', 'email', 'created_at', 'id')
    search_fields = ('name', 'whatsapp', 'message', 'email', 'created_at', 'id')


class OtpVerifyAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'otp', 'created_at')


admin.site.register(UserQuery, UserQueryAdmin)
admin.site.register(OtpVerify, OtpVerifyAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
