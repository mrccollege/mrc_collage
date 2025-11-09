from django.contrib import admin
from .models import UploadDemo, BulkCode, MainUserDemo


class MainUserDemoAdmin(admin.ModelAdmin):
    list_display = ['get_first_name', 'get_email','user', 'code', 'watch_count']
    search_fields = ('user__username', 'user__email', 'user__first_name', 'code')

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'First Name'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

admin.site.register(UploadDemo)
admin.site.register(BulkCode)
admin.site.register(MainUserDemo, MainUserDemoAdmin)
