from django.urls import path, include

urlpatterns = [
    path('blogs/', include('web.blogs_web.urls')),
    # path('login/', include('web.login_web.urls')),
]