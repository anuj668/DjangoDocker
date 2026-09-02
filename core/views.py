from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.db import IntegrityError
from .models import UserProfile

def landing_view(request):
    return render(request, 'landing/index.html')

def register_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        studio = request.POST.get('studio')
        role_name = request.POST.get('role')
        movies_per_year = request.POST.get('movies_per_year')
        country = request.POST.get('country')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, "Email and password are required.")
            return redirect('/#register')

        try:
            # We'll use email as the username for standard Django authentication
            user = User.objects.create_user(username=email, email=email, password=password)
            if full_name:
                parts = full_name.split(' ', 1)
                user.first_name = parts[0]
                if len(parts) > 1:
                    user.last_name = parts[1]
                user.save()

            if role_name:
                group, _ = Group.objects.get_or_create(name=role_name)
                user.groups.add(group)

            UserProfile.objects.create(
                user=user,
                mobile=mobile,
                studio=studio,
                movies_per_year=movies_per_year,
                country=country
            )

            login(request, user)
            return redirect('dashboard')

        except IntegrityError:
            messages.error(request, "An account with this email already exists.")
            return redirect('/#register')

    return redirect('landing')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Authentication failed. Verify credentials.")

    return render(request, 'login/index.html')

def logout_view(request):
    logout(request)
    return redirect('landing')

@never_cache
@login_required(login_url='login')
def dashbord_view(request):
    return render(request, 'vendor/dashboard.html')

@never_cache
@login_required(login_url='login')
@user_passes_test(lambda u: u.is_staff, login_url='dashboard')
def users_view(request):
    from django.contrib.auth.models import Group
    users = User.objects.select_related('profile').prefetch_related('groups').all().order_by('-date_joined')
    context = {
        'users': users,
        'total_users': users.count(),
        'active_users': users.filter(is_active=True).count(),
        'total_roles': Group.objects.count(),
    }
    return render(request, 'vendor/users.html', context)