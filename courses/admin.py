from django.contrib import admin

from .models import VideoFiles, UserWatch, Course, VideoInstructions, CoursePurchased, FileType, CourseMaster, \
    MonthMoney


class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('id', 'name')


class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'file', 'code_no', 'qr_code', 'created_at')
    list_filter = ('id', 'course', 'file', 'code_no', 'qr_code', 'created_at')


class MonthMoneyAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'month', 'money')
    list_filter = ('id', 'course', 'month', 'money')


class CoursePurchasedAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'razorpay_order_id', 'payment_status', 'coupon_code', 'month', 'start_date', 'end_date')
    list_filter = ('user', 'course', 'razorpay_order_id', 'payment_status', 'coupon_code', 'month', 'start_date', 'end_date')
    search_fields = ('user__username', 'course__title', 'razorpay_order_id', 'payment_status')



# Register your models here.
admin.site.register(VideoFiles, VideoAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(VideoInstructions)
admin.site.register(CoursePurchased, CoursePurchasedAdmin)
admin.site.register(UserWatch)
admin.site.register(FileType)
admin.site.register(CourseMaster)
admin.site.register(MonthMoney, MonthMoneyAdmin)
