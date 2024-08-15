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

]
