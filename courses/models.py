from django.contrib.auth.models import User
from django.db import models
# Create your models here.
class FileType(models.Model):
    file_type = models.CharField(max_length=20, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(null=True)
    def __str__(self):
        return self.file_type

class CourseMaster(models.Model):
    name = models.CharField(max_length=1000, null=True)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to='course_images/', null=True, default='', blank=True)
    def __str__(self):
        return

class Course(models.Model):
    course_master = models.ForeignKey(CourseMaster, on_delete=models.PROTECT, default=1)
    name = models.CharField(max_length=1000, null=True)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.CharField(max_length=10, default=0, blank=True)
    totalprice = models.DecimalField(max_digits=10, decimal_places=2)
    course_image = models.ImageField(upload_to='course_images/', null=True, default='', blank=True)
    demo_video = models.FileField(upload_to='course_demo', null=True, default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    validate_for = models.IntegerField(default=1, null=True, blank=True)
    course_lang = models.CharField(max_length=100, null=True, default='Hindi', blank=True)
    type = models.CharField(max_length=50, null=True, default='common', blank=True)
    attr1 = models.CharField(max_length=100, null=True, blank=True)
    attr2 = models.CharField(max_length=100, null=True, blank=True)
    attr3 = models.CharField(max_length=100, null=True, blank=True)

    attr4 = models.IntegerField(null=True, blank=True)
    attr5 = models.IntegerField(null=True, blank=True)
    attr6 = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class VideoFiles(models.Model):
    file_type = models.ForeignKey(FileType, on_delete=models.CASCADE, default=1)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    day = models.IntegerField(null=True)
    file = models.FileField(upload_to='course_files', default='')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(null=True)


class VideoInstructions(models.Model):
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    instruction = models.TextField(null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.instruction


class CoursePurchased(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    discount = models.CharField(max_length=10, null=True, default=0)
    totalprice = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    quantity = models.PositiveIntegerField(default=1, null=True)

    razorpay_payment_id = models.CharField(max_length=100, null=True)
    razorpay_order_id = models.CharField(max_length=100, null=True)
    razorpay_signature = models.CharField(max_length=100, null=True)
    payment_status = models.CharField(max_length=100, null=True)

    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True)

    attr1 = models.CharField(max_length=100, null=True)
    attr2 = models.CharField(max_length=100, null=True)
    attr3 = models.CharField(max_length=100, null=True)

    attr4 = models.IntegerField(null=True)
    attr5 = models.IntegerField(null=True)
    attr6 = models.IntegerField(null=True)


class UserWatch(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    videofile = models.ForeignKey(VideoFiles, on_delete=models.PROTECT)
    whatch_count = models.IntegerField(default=0)
    status = models.CharField(max_length=25, default='incomplete')
