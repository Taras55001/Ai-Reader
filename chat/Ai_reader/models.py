from django.db import models
from django.contrib.auth.models import User
from pdf.models import UploadedFile


class Chat(models.Model):
    name = models.CharField(max_length=100)
    doc = models.ForeignKey(
        UploadedFile, related_name="chats", on_delete=models.CASCADE, default=1
    )
    users = models.ForeignKey(User, related_name="sent_chats", on_delete=models.CASCADE)
    active = models.BooleanField(default=False)


class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(
        User, related_name="sent_messages", on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
