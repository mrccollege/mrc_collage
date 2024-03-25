from django.urls import path
from . import views

urlpatterns = [
    path('demo-therapy/', views.demo_list, name='demo_list'),
    path('demo-details/<int:course_id>/', views.demo_details, name='demo_details'),
    path('count_video_play/', views.count_video_play, name='count_video_play'),

]
