from django.urls import path
from . import views

urlpatterns = [
    path('', views.quotes, name='quotes-quotes'),
    path('<int:pk>', views.quote, name='quotes-quote'),
    
    path('home/', views.home, name='quotes-home'),
]
