from django.urls import path
from .views import landing_view, login_view, dashbord_view, register_view, logout_view, users_view

urlpatterns = [
    path('', landing_view, name='landing'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashbord_view, name='dashboard'),
    path('users/', users_view, name='users'),
  ]