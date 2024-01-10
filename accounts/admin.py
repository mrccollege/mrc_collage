from django.contrib import admin
from .models import UserQuery


# Register your models here.
class UserQueryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'created_at')


admin.site.register(UserQuery, UserQueryAdmin)
