from django.contrib import admin
from .models import UploadedFile

class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('file', 'uploaded_at', 'user_id')
    list_filter = ('user_id',)

admin.site.register(UploadedFile, UploadedFileAdmin)