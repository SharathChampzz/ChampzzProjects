from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='users-ui-login'),
    path('logout/', views.logout, name='users-ui-logout'),
]