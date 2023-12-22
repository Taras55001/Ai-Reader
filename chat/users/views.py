from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from .models import Blacklist
from django.http import JsonResponse
import json

def index(request):
    return render(request, 'users/base.html')


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
            email = form.cleaned_data['email']
            if Blacklist.objects.filter(email=email).exists():
                messages.error(request, 'Ця електронна адреса заблокована')
                return render(request, 'users/sign.html', context={"form": form, "error_message": "Ця електронна адреса заблокована."})
            form.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, user)
            return redirect(to='users:profile')
        else:
            return render(request, 'users/sign.html', context={"form": form})
    return render(request, 'users/sign.html', context={"form": RegisterForm()})

@login_required
def logoutuser(request):
    logout(request)
    return redirect(to='users:profile')

def delete(request):
    if request.method == 'POST':

        user = request.user 
        email = Blacklist(email=user.email)
        email.save()
        user.delete()
        return redirect(to='users:index')

    return JsonResponse({'message': 'Помилка при обробці запиту!'}, status=400)



def changed(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_username = data.get('username')
        new_email = data.get('email')

        user = request.user 
        user.username = new_username
        user.email = new_email
        user.save()

        return JsonResponse({'message': 'Дані збережено!'}, status=200)

    return JsonResponse({'message': 'Помилка при обробці запиту!'}, status=400)



def profile(request):

    return render(request, 'users/profile.html')