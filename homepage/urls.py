from django.urls import path,include
from . import views
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('<int:id>/', views.homepage, name='homepage'),
    path('cart-page/<int:id>/', views.cart_page, name='cart_page'),
    path('success/', views.success, name='success'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('watch-video/<str:type>/<int:course_id>/', views.watch_video, name='watch_video'),
    path('watch-video/<str:pre_next>/<str:type>/<int:course_id>/<int:file_id>/', views.watch_video, name='watch_video'),
    path('count_video/<int:id>/', views.count_video, name='count_video'),


    path('round_view/<int:video_id>/', views.round_view, name='round_view')

]
