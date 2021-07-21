from enum import unique
from django.db import models
from django.http import request
from rest_framework import fields, serializers
from .models import *


class UserStatusSerializer(serializers.ModelSerializer):
    user_profile = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = User


class UserSerializer(serializers.ModelSerializer):

    email = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'phone', )


class ChangePasswordSerializer(serializers.Serializer) :
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ChangeUserInfoSerializer(serializers.Serializer) :

    phone = serializers.CharField(required=True)


class MyCardSerializer(serializers.ModelSerializer) :
    
    author_name = serializers.ReadOnlyField(source='author.username')
    unique_num = serializers.ReadOnlyField()

    class Meta :
        model = MyCard
        fields= ('id', 'author', 'name', 'job', 'phone', 'email', 'tag1', 'tag2', 'tag3', 'author_name', 'unique_num',)


class CardSerializer(serializers.ModelSerializer) :
    
    owner_name = serializers.ReadOnlyField(source='owner.username')

    class Meta :
        model = Card
        fields = ('id', 'owner', 'follow_mycard', 'custom_tag1',
            'custom_tag2', 'custom_tag3', 'custom_tag4', 'custom_tag5', 'notes', 'division', 'isBookmarked', 'owner_name',)


class AddCardSerializer(serializers.Serializer) :
    
    qr_code = serializers.IntegerField(required=True)









