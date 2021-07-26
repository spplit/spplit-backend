from django.contrib import admin
from .models import *

class MyCardAdmim(admin.ModelAdmin) :
    list_display = ('id', 'author', 'name', 'job', 'phone', 'email', 'tag1', 'tag2', 'tag3',)
    list_display_links = ('id', 'author', 'name', )

class CardAdmin(admin.ModelAdmin) :
    list_display = ('id', 'owner', 'friend_card', 'division', 'custom_tag1', 'custom_tag2', 'custom_tag3', 'custom_tag4', 'custom_tag5','isBookmarked',)
    list_display_links = ('id', 'friend_card',)

# class RelationAdmin(admin.ModelAdmin) :
#     list_display = ('id', 'from_user', 'follow_card',)
#     list_display_links = ('id', 'from_user', )

admin.site.register(MyCard, MyCardAdmim)
admin.site.register(Card, CardAdmin)
# admin.site.register(Relation, RelationAdmin)
