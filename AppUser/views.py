from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from PathPilot.decorators import login_required
from .forms import StudentRegisterForm
from django.contrib import messages

def register_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Log user in immediately after registering
            messages.success(request, "Registration successful!")
            return redirect('dashboard') # Redirect to your main app page
    else:
        form = StudentRegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('userHome')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('userHome')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('user-login')
    return render(request, 'user-onboarding/login.html')


def logout_view(request):
    logout(request)
    return redirect('user-login')


@login_required
def userHome(request):
    return render(request, 'dashboard/user-home.html')