from django.urls import path
from . import views

urlpatterns = [
    path('', views.blogs, name='blogs-blogs'),
    path('/<int:pk>', views.blog, name='blogs-blog'),
]