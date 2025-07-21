from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email    = request.POST.get('email')
        password = request.POST.get('password')
        confirm  = request.POST.get('confirm_password')

        if password != confirm:
            messages.warning(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.warning(request, "Username already taken")
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.warning(request, "Account with this email already exist")
            return redirect('register')

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username, 
            email=email, 
            password=password
            )
        messages.success(request, "Registered successfully. Please log in.")
        return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            messages.warning(request, "Invalid credentials")
            return redirect('login')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')
