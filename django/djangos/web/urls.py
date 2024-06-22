from django.urls import path, include

urlpatterns = [
    path('', include('web.home.urls')),
    path('blogs/', include('web.blogs_web.urls')),
    path('users/', include('web.users_web.urls')),
]