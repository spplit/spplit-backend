from django.contrib import admin
from .models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'phone', 'is_superuser', 'is_active',)
    list_display_links = ('id', 'email',)
    exclude = ('password',)    