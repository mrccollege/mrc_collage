from django.urls import path
from . import view_api

urlpatterns = [
    path('course_list/', view_api.course_list, name='course_list'),
]
