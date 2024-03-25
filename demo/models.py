from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from courses.models import Course, FileType


class DemoCourseCategory(models.Model):
    category_name = models.CharField(max_length=1000, null=True)
    category_description = models.TextField(null=True, blank=True)
    category_image = models.ImageField(upload_to='demo_course_cat_image/', null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.category_name)


class DemoCourse(models.Model):
    category = models.ForeignKey(DemoCourseCategory, on_delete=models.PROTECT, null=True)
    course_name = models.CharField(max_length=1000, null=True)
    course_image = models.ImageField(upload_to='demo_course_images/', null=True, blank=True)
    course_video = models.FileField(upload_to='demo_course_video', null=True, blank=True)
    course_instructor = models.CharField(max_length=1000, null=True, blank=True)
    course_description = models.TextField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.course_name)


class DemoClass(models.Model):
    course = models.ForeignKey(DemoCourse, on_delete=models.CASCADE)
    file_formate = models.ForeignKey(FileType, on_delete=models.CASCADE)
    class_file_title = models.CharField(max_length=1000, null=True)
    class_file = models.FileField(upload_to='demo_class_files', default='')
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.class_file_title + '  ' + f'({self.course.course_name})')


class UserDemoCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(DemoCourse, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.user.email)


class UserDemoClass(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(UserDemoCourse, on_delete=models.CASCADE)
    course_class = models.ForeignKey(DemoClass, on_delete=models.CASCADE)
    watch_count = models.IntegerField(default=0)
    status = models.CharField(max_length=25, default='pending')
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.user.course_class.class_file_title)
