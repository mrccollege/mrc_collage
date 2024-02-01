from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class UserQuery(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    message = models.TextField(null=True)
    status = models.CharField(max_length=10, null=True, default='pending')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(null=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'user_query'


class OtpVerify(models.Model):
    email = models.EmailField(null=True, unique=True)
    otp = models.CharField(max_length=10, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(null=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'otp_verify'
