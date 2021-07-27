from rest_framework import fields, serializers
from .models import *

class MyCardSerializer(serializers.ModelSerializer) :
    
    author_name = serializers.ReadOnlyField(source='author.username')

    class Meta :
        model = MyCard
        fields= ('id', 'author_name', 'name', 'job', 'phone', 'email', 'tag1', 'tag2', 'tag3', 'author_name', )


class CardSerializer(serializers.ModelSerializer) :
    
    owner_name = serializers.ReadOnlyField(source='owner.username')
    friend_card = MyCardSerializer()

    class Meta :
        model = Card
        fields = ('id', 'owner_name', 'friend_card', 'custom_tag1',
            'custom_tag2', 'custom_tag3', 'custom_tag4', 'custom_tag5', 'notes', 'division', 'isBookmarked', 'owner_name',)

class UserCountSerializer(serializers.Serializer):
    count_user_mycard = serializers.IntegerField()