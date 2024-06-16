from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.is_service_available, name='is_service_available'),
    path('quotes/', include('quotes.urls')),
    # add more paths here
]
