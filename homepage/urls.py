from django.urls import path
from . import views
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('<int:id>/', views.homepage, name='homepage'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('watch-video/<str:type>/<int:course_id>/', views.watch_video, name='watch_video'),
    path('watch-video/<str:pre_next>/<str:type>/<int:course_id>/<int:file_id>/', views.watch_video, name='watch_video'),
    path('count_video/<int:id>/', views.count_video, name='count_video'),


    path('round_view/<int:video_id>/', views.round_view, name='round_view'),

    path('add_course/', views.add_course, name='add_course'),
    path('upload_video/', views.upload_video, name='upload_video'),
    path('video_detail/<int:id>/', views.video_detail, name='video_detail'),

    path('view_list/<int:course_id>/', views.view_list, name='view_list'),
    path('get_kshar_sutra_videos/', views.get_kshar_sutra_videos, name='get_kshar_sutra_videos'),
    path('delete_files/', views.delete_files, name='delete_files'),

    path('buy_course_detail/<int:course_id>/', views.buy_course_detail, name='buy_course_detail'),
    path('buy_course_detail/<int:course_id>/<str:status>/', views.buy_course_detail, name='buy_course_detail'),
    path('get_service_month/', views.get_service_month, name='get_service_month'),
    path('get_service_price/', views.get_service_price, name='get_service_price'),

    path('apply_coupon_code/', views.apply_coupon_code, name='apply_coupon_code'),
    path('gargi/', views.gargi, name='gargi'),
    path('search-therapy/', views.search_therapy, name='search_therapy'),


]
