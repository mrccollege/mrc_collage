from django.contrib import admin

from .models import VideoFiles, UserWatch, Course, VideoInstructions, CoursePurchased, FileType, CourseMaster, \
    MonthMoney


class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'file', 'code_no', 'qr_code', 'created_at')


class CoursePurchasedAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'payment_status', 'price', 'coupon_code', 'discount', 'totalprice', 'month', 'start_date', 'end_date')
    list_filter = ('id', 'user', 'course', 'payment_status', 'price', 'coupon_code', 'discount', 'totalprice', 'month', 'start_date', 'end_date')


# Register your models here.
admin.site.register(VideoFiles, VideoAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(VideoInstructions)
admin.site.register(CoursePurchased, CoursePurchasedAdmin)
admin.site.register(UserWatch)
admin.site.register(FileType)
admin.site.register(CourseMaster)
admin.site.register(MonthMoney)
