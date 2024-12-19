from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
import openpyxl
from django.http import HttpResponse

from .models import VideoFiles, UserWatch, Course, VideoInstructions, CoursePurchased, FileType, CourseMaster, \
    MonthMoney, ScreenColumn


def export_course_purchases_to_excel(modeladmin, request, queryset):
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )

    # Generate a filename based on the applied filters
    start_date = request.GET.get('start_date__gte')
    end_date = request.GET.get('end_date__lte')
    if start_date and end_date:
        filename = f'course_purchases_{start_date}_to_{end_date}.xlsx'
    else:
        filename = 'course_purchases.xlsx'

    response['Content-Disposition'] = f'attachment; filename={filename}'

    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Course Purchases'

    # Define the header
    headers = [
        'User','Name', 'Course','totalprice', 'Razorpay Order ID', 'Payment Status', 'Coupon Code', 'Month',
        'Start Date', 'End Date'
    ]
    worksheet.append(headers)

    sorted_queryset = queryset.order_by('start_date')

    # Populate the data
    for obj in sorted_queryset:
        row = [
            obj.user.username,  # or obj.user.email if preferred
            obj.user.first_name,  # or obj.user.email if preferred
            obj.course.name,  # assuming the Course model has a name field
            obj.totalprice,  # assuming the Course model has a name field
            obj.razorpay_order_id,
            obj.payment_status,
            obj.coupon_code,
            obj.month,
            obj.start_date.strftime('%Y-%m-%d'),
            obj.end_date.strftime('%Y-%m-%d') if obj.end_date else ''
        ]
        worksheet.append(row)

    workbook.save(response)
    return response


class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('id', 'name')


class ScreenColumnAdmin(admin.ModelAdmin):
    list_display = ('id', 'screen_column')
    list_filter = ('id', 'screen_column')


class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'file', 'code_no', 'qr_code', 'created_at')
    list_filter = ('id', 'course', 'file', 'code_no', 'qr_code', 'created_at')


class MonthMoneyAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'month', 'money')
    list_filter = ('id', 'course', 'month', 'money')


class CoursePurchasedAdmin(admin.ModelAdmin):
    list_display = (
    'user', 'get_first_name', 'course', 'totalprice','razorpay_signature', 'payment_status', 'coupon_code', 'month', 'start_date')
    list_filter = (
    'user', 'course','razorpay_signature', 'payment_status', 'coupon_code', 'month', 'start_date')
    search_fields = ('user__username','user__first_name', 'course__name', 'razorpay_order_id','razorpay_payment_id', 'payment_status')
    actions = [export_course_purchases_to_excel]

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'First Name'


# Register your models here.
admin.site.register(VideoFiles, VideoAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(VideoInstructions)
admin.site.register(CoursePurchased, CoursePurchasedAdmin)
admin.site.register(UserWatch)
admin.site.register(FileType)
admin.site.register(CourseMaster)
admin.site.register(MonthMoney, MonthMoneyAdmin)
admin.site.register(ScreenColumn, ScreenColumnAdmin)
