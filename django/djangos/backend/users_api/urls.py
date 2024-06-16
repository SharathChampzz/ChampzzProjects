from django.urls import path
from . import views


# /api/users/*
urlpatterns = [
    path('login', views.login, name='users-login'),
    path('logout', views.logout, name='users-logout'),
    path('', views.create_user, name='users-users'), # GET and POST users
    path('<int:pk>', views.user_detail, name='users-get_user'), # GET, PUT, DELETE user
]