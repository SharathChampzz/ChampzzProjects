from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='summariser-home'),
    path('summarize/', views.summarize, name='summariser-summarize'),
    path('test/', views.test, name='summariser-test'),
]