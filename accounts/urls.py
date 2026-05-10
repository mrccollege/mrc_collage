from django.urls import path
from . import views, views_api

urlpatterns = [
    path('register/', views.register_account, name='register-accounts'),
    path('login/', views.login_account, name='login_account'),
    path('logout/', views.logout_account, name='logout_account'),

    path('forget_password/', views.forget_password, name='forget_password'),
    path('verity_otp/', views.verity_otp, name='verity_otp'),
    path('verity_otp/<str:email>/', views.verity_otp, name='verity_otp'),

    path('term_condition/', views.term_condition, name='term_condition'),
    path('cancel_refund/', views.cancel_refund, name='cancel_refund'),
    path('shiping/', views.shiping, name='shiping'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('contact_us/', views.contact_us, name='contact_us'),

    path('user_login/', views_api.user_login, name='user_login'),
    path('user_logout/', views_api.user_logout, name='user_logout'),
    path('app_register/', views_api.app_register, name='app_register'),
    path('app_login/', views_api.app_login, name='app_login'),
    path('app_me/', views_api.app_me, name='app_me'),
    path('app_logout/', views_api.app_logout, name='app_logout'),	 
    path('app_change_password/', views_api.app_change_password, name='app_change_password'),
    path('app_forgot_password_send_otp/', views_api.app_forgot_password_send_otp, name='app_forgot_password_send_otp'),
    path('app_forgot_password_reset/', views_api.app_forgot_password_reset, name='app_forgot_password_reset'),
	

]
