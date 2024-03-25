from django.db import models
from django.contrib.auth.models import User

from courses.models import FileType, Course


class DemoClass(models.Model):
    file_type = models.ForeignKey(FileType, on_delete=models.CASCADE, default=1)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000, null=True)
    demo_file = models.FileField(upload_to='demo_class_files', default='')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.title + ' ' + f"({self.course.name})")


class UserDemoClass(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ForeignKey(DemoClass, on_delete=models.CASCADE)
    watch_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.file.title + ' ' + f"({self.file.course.name})")
