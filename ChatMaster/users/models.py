from django.db import models

class User(models.Model):
    username = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    creat_at=models.DateTimeField('date published')
    chat=models.CharField(max_length=200)