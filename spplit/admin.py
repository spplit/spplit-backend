from django.contrib import admin
from .models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'phone', 'is_superuser', 'is_active',)
    list_display_links = ('id', 'email',)
    exclude = ('password',)    


class MyCardAdmim(admin.ModelAdmin) :
    list_display = ('id', 'author', 'name', 'job', 'phone', 'email', 'tag1', 'tag2', 'tag3', 'unique_num', )
    list_display_links = ('id', 'author', 'name', )

class CardAdmin(admin.ModelAdmin) :
    # list_display = ('id', 'owner', 'name', 'job', 'division', 'isBookmarked', 'unique_num', )
    # list_display_links = ('id',)
    list_display = ('id', 'owner', 'follow_mycard', 'division', 'custom_tag1', 'custom_tag2', 'custom_tag3', 'custom_tag4', 'custom_tag5','isBookmarked',)
    list_display_links = ('id', 'follow_mycard',)

class RelationAdmin(admin.ModelAdmin) :
    list_display = ('id', 'from_user', 'follow_card',)
    list_display_links = ('id', 'from_user', )

admin.site.register(MyCard, MyCardAdmim)
admin.site.register(Card, CardAdmin)
admin.site.register(Relation, RelationAdmin)
