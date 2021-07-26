from rest_framework import fields, serializers
from .models import *

class MyCardSerializer(serializers.ModelSerializer) :
    
    author_name = serializers.ReadOnlyField(source='author.username')

    class Meta :
        model = MyCard
        fields= ('id', 'author_name', 'name', 'job', 'phone', 'email', 'tag1', 'tag2', 'tag3', 'author_name', )


class CardSerializer(serializers.ModelSerializer) :
    
    owner_name = serializers.ReadOnlyField(source='owner.username')

    class Meta :
        model = Card
        fields = ('id', 'owner_name', 'follow_mycard', 'custom_tag1',
            'custom_tag2', 'custom_tag3', 'custom_tag4', 'custom_tag5', 'notes', 'division', 'isBookmarked', 'owner_name',)


class AddCardSerializer(serializers.Serializer) :
    
    qr_code = serializers.CharField(required=True)


