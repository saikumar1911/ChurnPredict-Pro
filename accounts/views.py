from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import LoginForm, RegisterForm
from .models import StoreManagerProfile

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('dashboard:dashboard')
            form.add_error(None, 'Invalid username or password!')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data.get('first_name', '')
            last_name = form.cleaned_data.get('last_name', '')
            store_name = form.cleaned_data.get('store_name', '')
            phone = form.cleaned_data.get('phone', '')

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )

            profile, _ = StoreManagerProfile.objects.get_or_create(user=user)
            profile.store_name = store_name
            profile.phone = phone
            profile.save()

            login(request, user)
            messages.success(request, f'Welcome {username}! Account created.')
            return redirect('dashboard:dashboard')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Logged out successfully.')
    return redirect('login')