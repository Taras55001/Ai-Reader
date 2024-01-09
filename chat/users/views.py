"""
The module provides work with users: registration, authentication, deleting, profile editing
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
from .models import Blacklist
from django.http import JsonResponse
import json
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy


def index(request):
    return render(request, 'users/index.html', context={'title': 'Main Page'})


def login_s(request):

    if request.user.is_authenticated:
        return redirect(to='users:profile')

    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.error(request, 'Username or password didn\'t match')
            return redirect(to='users:login')

        login(request, user)
        return redirect(to='chat:chat')

    return render(request, 'users/login.html', context={"form": LoginForm()})

def sign(request):
    """
    Check/Create new user
    """
    if request.user.is_authenticated:
        return redirect(to='chat:chat')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if Blacklist.objects.filter(email=email).exists():
                messages.error(request, 'Ця електронна адреса заблокована')
                return render(request, 'users/sign.html', context={"form": form, "error_message": "Ця електронна адреса заблокована."})
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Ця електронна адреса вже зареєстрована')
                return render(request, 'users/sign.html', context={"form": form, "error_message": "Ця електронна адреса вже зареєстрована."})
            form.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, user)
            return redirect(to='chat:chat')
        else:
            return render(request, 'users/sign.html', context={"form": form})
    return render(request, 'users/sign.html', context={"form": RegisterForm()})

@login_required
def logoutuser(request):
    logout(request)
    return redirect(to='chat:main')

def delete(request):
    """
    Deleting an existing user. User e-mail will be blocked permanently
    """
    if request.method == 'POST':

        user = request.user 
        email = Blacklist(email=user.email)
        email.save()
        user.delete()
        return redirect(to='users:index')

    return JsonResponse({'message': 'Помилка при обробці запиту!'}, status=400)



def changed(request):
    """
    Updating user info
    """
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


def eror_aut(request):
    return render(request, 'users/eror_aut.html')


def profile(request):
    if request.user.is_authenticated:
        return render(request, 'users/profile.html')
    else:
        return redirect(reverse('users:eror_aut')) 
    


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    html_email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'users/password_reset_subject.txt'