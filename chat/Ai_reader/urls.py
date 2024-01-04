from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.main, name='main'),
    path('chat/', views.chat, name='chat'),
    path('answer/', views.answer, name='answer')
]