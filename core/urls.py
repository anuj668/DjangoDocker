from django.urls import path
from .views import landing_view,login_view,dashbord_view

urlpatterns = [
    path('', landing_view, name='landing'),
    path('login', login_view, name='login'),
    path('dashboard', dashbord_view, name='dashboard'),
  ]