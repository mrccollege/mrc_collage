from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register_account, name='register-accounts'),
    path('login/', views.login_account, name='login_account'),
    path('logout/', views.logout_account, name='logout_account'),

    path('term_condition/', views.term_condition, name='term_condition'),
    path('cancel_refund/', views.cancel_refund, name='cancel_refund'),
    path('shiping/', views.shiping, name='shiping'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),

]
