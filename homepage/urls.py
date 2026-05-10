from django.urls import path
from . import views, views_app_api

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('<int:id>/', views.homepage, name='homepage'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('my-courses/<str:merchant_reference_id>/', views.my_courses, name='my_courses'),
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

    path('app_get_service_month/', views_app_api.app_get_service_month, name='app_get_service_month'),
    path('app_get_service_price/', views_app_api.app_get_service_price, name='app_get_service_price'),
    path('app_apply_coupon_code/', views_app_api.app_apply_coupon_code, name='app_apply_coupon_code'),
    path('app_buy_course_detail/<int:course_id>/', views_app_api.app_buy_course_detail, name='app_buy_course_detail'),
    path('app_payment_status/', views_app_api.app_payment_status, name='app_payment_status'),
    path('app_payment_confirm/', views_app_api.app_payment_confirm, name='app_payment_confirm'),
    path('app-payment-return/<str:merchant_reference_id>/', views_app_api.app_payment_return, name='app_payment_return'),

    path('gargi/', views.gargi, name='gargi'),
    path('search-therapy/', views.search_therapy, name='search_therapy'),
    path('final_pay/', views.final_pay, name='final_pay'),
    path("start/", views.initiate_payment, name="start_payment"),
    path("payment_callback/", views.payment_callback, name="payment_callback"),
    path('app_home_top_media/', views_app_api.app_home_top_media, name='app_home_top_media'),
    path("app_upload_feedback_image/", views_app_api.app_upload_feedback_image, name="app_upload_feedback_image"),
    path("app_get_feedback_images/", views_app_api.app_get_feedback_images, name="app_get_feedback_images"),
    path("app_delete_feedback_image/", views_app_api.app_delete_feedback_image, name="app_delete_feedback_image"),
    path("app_edit_feedback_image/", views_app_api.app_edit_feedback_image, name="app_edit_feedback_image"),
 # New Master Course Management Paths
    path("app_get_courses/", views_app_api.app_get_courses, name="app_get_courses"),
    path("update_master_bulk/", views_app_api.update_master_bulk, name="update_master_bulk"),
 
    


]

