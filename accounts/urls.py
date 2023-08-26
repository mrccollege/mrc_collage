from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register_account, name='register-accounts'),
    path('login/', views.login_account, name='login_account'),
    path('logout/', views.logout_account, name='logout_account'),

]
