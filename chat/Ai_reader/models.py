from django.db import models
from django.contrib.auth.models import User



class Chat(models.Model):
    name = models.CharField(max_length=100)  
    users = models.ManyToManyField(User, related_name='chats')  

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE) 
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE) 
    content = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True) 