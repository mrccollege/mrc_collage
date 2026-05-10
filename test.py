import os
import django
import sys
import requests
from django.db.models import Q
from datetime import datetime, timedelta


# 1. Setup paths
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PROJECT_ROOT)

# 2. Configure Settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_course.settings')

# 3. Initialize Django (This MUST happen before importing models)
django.setup()




from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import UserProfile, UserQuery, OtpVerify, UserSession
from courses.models import Course,CoursePurchased
from homepage.models import CouponCode


print("This is a test to see if the system is reading this file.")
print("Fetching all courses:")

#filter coursepuchased objects where payment status is not successful or do not have written following words  "success" or "succes"  and start date is less than 3 month old   
three_months_ago = timezone.now() - timezone.timedelta(days=90)
purchased_courses = CoursePurchased.objects.exclude(
    Q(payment_status__icontains='success') | 
    Q(payment_status__icontains='succes') |
    Q(payment_status__icontains='renew')
).filter(start_date__gte=three_months_ago)

#now map cousre name to it and print the course name and payment status
# for purchase in purchased_courses:
#     course_name = purchase.course.name if purchase.course else "Unknown Course"
#     print(f"Course: {course_name}, Payment Status: {purchase.payment_status}, Start Date: {purchase.start_date}")       

# #now map user mobile to it using user_id to mobile as join key and print the course name, payment status and user mobile number 
# for purchase in purchased_courses:
#     course_name = purchase.course.name if purchase.course else "Unknown Course"
#     user_profile = UserProfile.objects.filter(user_id=purchase.user_id).first()
#     mobile_number = user_profile.mobile if user_profile else "Unknown Mobile"
#     print(f"Course: {course_name}, User ID: {purchase.user_id}, Payment Status: {purchase.payment_status}, Start Date: {purchase.start_date}, Mobile: {mobile_number}")

# #count empty or blank in mobile number in above result
# empty_mobile_count = purchased_courses.filter(user__userprofile__mobile__isnull=True).count() + purchased_courses.filter(user__userprofile__mobile__exact='').count()
# print(f"Total purchased courses with empty or blank mobile number: {empty_mobile_count}")   




#count empty or blank in mobile number in above result and print user id for those records
#empty_mobile_users = purchased_courses.filter(user__userprofile__mobile__isnull=True).values_list('user_id', flat=True) | purchased_courses.filter(user__userprofile__mobile__exact='').values_list('user_id', flat=True)
#print(f"User IDs with empty or blank mobile number: {list(empty_mobile_users)}")    


# for purchase in purchased_courses:
#     course_name = purchase.course.name if purchase.course else "Unknown Course"
#     user_profile = UserProfile.objects.filter(user_id=purchase.user_id).first()
#     mobile_number = user_profile.mobile if user_profile else "Unknown Mobile"
#     days_since_start = (timezone.now().date() - purchase.start_date.date()).days if purchase.start_date else "Unknown Start Date"
#     if days_since_start in [1, 2, 5, 15, 30, 60]:
#         print(f"Course: {course_name}, User ID: {purchase.user_id}, Payment Status: {purchase.payment_status}, Start Date: {purchase.start_date}, Mobile: {mobile_number}, Days Since Start: {days_since_start}")           

#give me count of each days since start in above result
days_count = {}
for purchase in purchased_courses:
    days_since_start = (timezone.now().date() - purchase.start_date.date()).days if purchase.start_date else "Unknown Start Date"
    if days_since_start in [1, 2, 5, 15, 30, 60]:
        days_count[days_since_start] = days_count.get(days_since_start, 0) + 1            

# count = purchased_courses.count()
# print(f"Total purchased courses with payment ID and start date within last 3 months: {count}")



print("Days Since Start Count:")
for days, count in days_count.items():
    print(f"Days: {days}, Count: {count}")

# get coupon code against id 1,2,3 and print the code and discount percentage
coupon_codes = CouponCode.objects.filter(id__in=[1, 2, 3, 4])
for coupon in coupon_codes:
    print(f"Coupon Code: {coupon.coupon_code}, Discount Percentage: {coupon.percent}")
       
# now for days since start if it is 1, use coupon code with id 1, if it is 2 use coupon code with id 2, if it is 5 use coupon code with id 3 and print the course name, user id, payment status, start date, mobile number and coupon code and discount percentage
for purchase in purchased_courses:
    course_name = purchase.course.name if purchase.course else "Unknown Course"
    user_profile = UserProfile.objects.filter(user_id=purchase.user_id).first()
    mobile_number = user_profile.mobile if user_profile else "Unknown Mobile"
    days_since_start = (timezone.now().date() - purchase.start_date.date()).days if purchase.start_date else "Unknown Start Date"
    
    coupon_code = None
    discount_percentage = None
    
    if days_since_start == 1:
        coupon = CouponCode.objects.filter(id=1).first()
        coupon_code = coupon.coupon_code if coupon else "Unknown Coupon"
        discount_percentage = coupon.percent if coupon else "Unknown Discount"
    elif days_since_start == 2:
        coupon = CouponCode.objects.filter(id=2).first()
        coupon_code = coupon.coupon_code if coupon else "Unknown Coupon"
        discount_percentage = coupon.percent if coupon else "Unknown Discount"
    elif days_since_start == 5:
        coupon = CouponCode.objects.filter(id=2).first()
        coupon_code = coupon.coupon_code if coupon else "Unknown Coupon"
        discount_percentage = coupon.percent if coupon else "Unknown Discount"
    elif days_since_start == 15:
        coupon = CouponCode.objects.filter(id=4).first()
        coupon_code = coupon.coupon_code if coupon else "Unknown Coupon"
        discount_percentage = coupon.percent if coupon else "Unknown Discount"
    elif days_since_start == 30:
        coupon = CouponCode.objects.filter(id=4).first()
        coupon_code = coupon.coupon_code if coupon else "Unknown Coupon"
        discount_percentage = coupon.percent if coupon else "Unknown Discount"
    elif days_since_start == 60:
        coupon = CouponCode.objects.filter(id=4).first()
        coupon_code = coupon.coupon_code if coupon else "Unknown Coupon"
        discount_percentage = coupon.percent if coupon else "Unknown Discount"

    if days_since_start in [1, 2, 5, 15, 30, 60]:
        message_data = {
            'course_name': course_name,
            'user_id': purchase.user_id,
            'payment_status': purchase.payment_status,
            'start_date': purchase.start_date,
            'mobile_number': mobile_number,
            'days_since_start': days_since_start,
            'coupon_code': coupon_code,
            'discount_percentage': discount_percentage
        }
        if days_since_start == 1:
            print(f"Message Data for Day 1: {message_data}\n")
            
        elif days_since_start == 2:
            print(f"Message Data for Day 2: {message_data}\n")
        elif days_since_start == 5:
            print(f"Message Data for Day 5: {message_data}\n")
        elif days_since_start == 15:
            print(f"Message Data for Day 15: {message_data}\n")
        elif days_since_start == 30:
            print(f"Message Data for Day 30: {message_data}\n")
        elif days_since_start == 60:
            print(f"Message Data for Day 60: {message_data}\n")   

