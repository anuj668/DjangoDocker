from django.shortcuts import render

# Create your views here.

def landing_view(request):
    return render(request, 'landing/index.html')

def login_view(request):
    return render(request, 'login/index.html')

def dashbord_view(request):
    return render(request, 'vendor/dashboard.html')