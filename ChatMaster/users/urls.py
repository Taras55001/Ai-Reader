from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('login', views.login_s, name='login'),
    path('sign', views.sign, name='sign'),
    path('profile', views.profile, name='profile'),
    path('logout', views.logoutuser, name='logout'),
    path('', views.index, name='index'),

]