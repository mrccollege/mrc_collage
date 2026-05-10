from django.db import models
from courses.models import Course

# for homepage media

class HomepageTopMedia(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.TextField(default="", blank=True, db_column="url")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, db_column="course_id")
    sort_order = models.IntegerField(default=0, db_column="sort_order")

    class Meta:
        db_table = "homepage_top_media"
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.course.name} ({self.sort_order})"




# Create your models here.
class Lookup(models.Model):
    code = models.CharField(max_length=50, null=True)
    title = models.CharField(max_length=50, null=True)
    desc = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='files', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=False,blank=True, null=True)

    def __str__(self):
        return self.title


class CouponCode(models.Model):
    coupon_agent_name = models.CharField(max_length=100, null=True, default='admin')
    coupon_agent_mobile = models.CharField(max_length=15, null=True, default='9267678888')
    coupon_agent_address = models.TextField(null=True, blank=True)
    coupon_agent_email = models.EmailField(unique=True, null=True, blank=True)
    coupon_name = models.CharField(max_length=100, null=True)
    coupon_code = models.IntegerField(null=True)
    percent = models.IntegerField(null=True)

    def __str__(self):
        return str(self.coupon_code)

from django.db import models
from courses.models import Course


# Create your models here.
class Lookup(models.Model):
    code = models.CharField(max_length=50, null=True)
    title = models.CharField(max_length=50, null=True)
    desc = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='files', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=False,blank=True, null=True)

    def __str__(self):
        return self.title


class CouponCode(models.Model):
    coupon_agent_name = models.CharField(max_length=100, null=True, default='admin')
    coupon_agent_mobile = models.CharField(max_length=15, null=True, default='9267678888')
    coupon_agent_address = models.TextField(null=True, blank=True)
    coupon_agent_email = models.EmailField(unique=True, null=True, blank=True)
    coupon_name = models.CharField(max_length=100, null=True)
    coupon_code = models.IntegerField(null=True)
    percent = models.IntegerField(null=True)

    def __str__(self):
        return str(self.coupon_code)


class HomepageTopMedia(models.Model):
    url = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "homepage_top_media"
        ordering = ["sort_order", "id"]

    def __str__(self):
        course_name = self.course.name if self.course_id else "No course"
        return f"{course_name} ({self.sort_order})"

class FeedbackImage(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='feedback_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "feedback_images"

    def __str__(self):
        return self.title or f"Feedback Image {self.id}"
