from django.db import models


# Create your models here.
class Lookup(models.Model):
    code = models.CharField(max_length=50, null=True)
    title = models.CharField(max_length=50, null=True)
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

