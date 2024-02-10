from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class UserQuery(models.Model):
    name = models.CharField(max_length=100, null=True)
    whatsapp = models.CharField(max_length=15, null=True, blank=True)
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


class UserSession(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=255)
    login_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.session_id}"
