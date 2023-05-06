from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django import forms

from .forms import SignUpForm


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.error(request, "There Was An Error Logging In. PLease Try Again...")
            return redirect('login')

    else:
        return render(request, "login.html", {})


def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out!")
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # first_name = form.cleaned_data['first_name']
            # second_name = form.cleaned_data['second_name']
            # email = form.cleaned_data['email']
            # Log in User
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered! Welcome!")
            return redirect('home')

    return render(request, "register.html", {'form': form})


def home(request):
    return render(request, "home.html", {})
