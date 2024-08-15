from django.urls import path
from . import view_api

urlpatterns = [
    path('course_list/', view_api.course_list, name='course_list'),
    path('course_detail/', view_api.course_detail, name='course_detail'),
    path('my_courses/', view_api.my_courses, name='my_courses'),

]
