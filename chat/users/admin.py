from django.contrib import admin
from .models import Blacklist

class UsersBlacklistAdmin(admin.ModelAdmin):
    list_display = ('email',) 

admin.site.register(Blacklist, UsersBlacklistAdmin)