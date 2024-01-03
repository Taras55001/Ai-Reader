from django.db import models
from django.contrib.auth.models import User


class UploadedFile(models.Model):
    file = models.FileField()
    vector_db = models.FileField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, default=None
    )
