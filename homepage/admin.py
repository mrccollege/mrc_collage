from django.contrib import admin
from .models import Lookup, CouponCode


# Register your models here.
class CouponAdmin(admin.ModelAdmin):
    list_display = ('id', 'coupon_name', 'coupon_code', 'percent')


admin.site.register(Lookup)
admin.site.register(CouponCode, CouponAdmin)
