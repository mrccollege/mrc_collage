from django.contrib import admin

from .models import VideoFiles,UserWatch, Course, VideoInstructions, CoursePurchased, FileType

# Register your models here.
admin.site.register(VideoFiles)
admin.site.register(Course)
admin.site.register(VideoInstructions)
admin.site.register(CoursePurchased)
admin.site.register(UserWatch)
admin.site.register(FileType)
