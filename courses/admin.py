from django.contrib import admin

from .models import VideoFiles, AudioFiles, Course, UserWatch, VideoInstructions, AudioInstructions, CoursePurchased

# Register your models here.
admin.site.register(VideoFiles)
admin.site.register(AudioFiles)
admin.site.register(Course)
admin.site.register(VideoInstructions)
admin.site.register(AudioInstructions)
admin.site.register(CoursePurchased)
admin.site.register(UserWatch)
