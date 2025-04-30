from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from . import models
from . import forms
# Create your views here.

def user(request):
    return HttpResponse("User Page")


def user_signup(request):
    if request.method == 'POST':
        form = forms.UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "User Registration Successfully") 
            return redirect('login') 
        else:
            messages.error(request, "Fix the given error into the Form")  
    else:
        form = forms.UserRegisterForm()
    return render(request, 'user_signup.html', {'form': form, 'type':'signup'})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login Successful")
            return redirect('profile')
            
        else:
            messages.error(request, "Invalid credentials")
    else:
        form = AuthenticationForm()
    return render(request, 'user_signup.html', {'form': form, 'type':'login'})


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "Logout Successful")
    return redirect('login')


def user_profile(request):
    return render(request, 'user_profile.html')

def home(request):
    return render(request, 'home_page.html')

            