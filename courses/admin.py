from django.contrib import admin

from .models import VideoFiles, UserWatch, Course, VideoInstructions, CoursePurchased, FileType, CourseMaster, \
    MonthMoney


class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'file', 'code_no', 'qr_code')


# Register your models here.
admin.site.register(VideoFiles, VideoAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(VideoInstructions)
admin.site.register(CoursePurchased)
admin.site.register(UserWatch)
admin.site.register(FileType)
admin.site.register(CourseMaster)
admin.site.register(MonthMoney)
