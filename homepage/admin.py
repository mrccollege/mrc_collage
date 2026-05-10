from django.contrib import admin
from .models import Lookup, CouponCode, HomepageTopMedia,  FeedbackImage


# for homepage media  top

class HomepageTopMediaAdmin(admin.ModelAdmin):
    list_display = ("id", "course", "sort_order", "url")
    search_fields = ("course__name", "url")

admin.site.register(HomepageTopMedia, HomepageTopMediaAdmin)

# Register your models here.
class CouponAdmin(admin.ModelAdmin):
    list_display = ('id', 'coupon_name', 'coupon_code', 'percent', 'coupon_agent_name', 'coupon_agent_mobile', 'coupon_agent_email')


admin.site.register(Lookup)
admin.site.register(CouponCode, CouponAdmin)




class FeedbackImageAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "image", "created_at")
    search_fields = ("title",)

admin.site.register(FeedbackImage, FeedbackImageAdmin)
