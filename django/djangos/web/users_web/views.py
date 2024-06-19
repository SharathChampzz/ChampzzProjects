from django.shortcuts import render

# Create your views here.


def login(request):
    return render(request, 'users_web/login.html')

def logout(request):
    return render(request, 'users_web/logout.html')