from unicodedata import category
from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'phone',)
    list_display_links = ('id', 'email',)
    exclude = ('password',)    


class CategoryAdmin(admin.ModelAdmin) :
    list_display = ('id', 'user',)
    list_display_links = ('id', 'user',)

class DivisoinAdmin(admin.ModelAdmin) :
    list_display = ('id', 'user',)
    list_display_links = ('id', 'user',)

admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Division, DivisoinAdmin)