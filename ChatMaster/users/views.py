from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm



def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def login_s(request):
    if request.user.is_authenticated:
        return redirect(to='users:profile')

    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.error(request, 'Username or password didn\'t match')
            return redirect(to='users:login')

        login(request, user)
        return redirect(to='users:profile')

    return render(request, 'users/login.html', context={"form": LoginForm()})

def sign(request):
    if request.user.is_authenticated:
        return redirect(to='users:profile')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='users:profile')
        else:
            return render(request, 'users/sign.html', context={"form": form})
    return render(request, 'users/sign.html', context={"form": RegisterForm()})

@login_required
def logoutuser(request):
    logout(request)
    return redirect(to='users:profile')

def profile(request):
    return render(request, 'users/profile.html')