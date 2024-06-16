from django.urls import path, include

urlpatterns = [
    path('blogs/', include('web.blogs_web.urls')),
]