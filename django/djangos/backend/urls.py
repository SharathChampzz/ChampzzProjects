from django.urls import path, include

urlpatterns = [
    path('blogs/', include('backend.blogs_api.urls')),
]