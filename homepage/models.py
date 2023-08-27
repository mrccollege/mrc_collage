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
