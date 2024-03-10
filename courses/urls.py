from django.urls import path
from . import view_api

urlpatterns = [
    path('course_list/', view_api.course_list, name='course_list'),
    path('course_detail/<int:id>/', view_api.course_detail, name='course_detail'),

]
