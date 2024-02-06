from django.contrib import admin
from .models import Lookup, CouponCode


# Register your models here.
class CouponAdmin(admin.ModelAdmin):
    list_display = ('id', 'coupon_name', 'coupon_code', 'percent', 'coupon_agent_name', 'coupon_agent_mobile', 'coupon_agent_email')


admin.site.register(Lookup)
admin.site.register(CouponCode, CouponAdmin)
