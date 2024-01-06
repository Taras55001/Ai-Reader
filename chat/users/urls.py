from django.urls import path

from . import views
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

app_name = 'users'

urlpatterns = [
    path('login', views.login_s, name='login'),
    path('sign', views.sign, name='sign'),
    path('profile', views.profile, name='profile'),
    path('logout', views.logoutuser, name='logout'),
    path('', views.index, name='index'),
    path('delete', views.delete, name='delete'),
    path('change', views.changed, name='change'),
    path('eror_aut', views.eror_aut, name='eror_aut'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('reset-password/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html',
                                          success_url='/users/reset-password/complete/'),
         name='password_reset_confirm'),
    path('reset-password/complete/',
         PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    path('reset-password/complete/',
         PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),

]