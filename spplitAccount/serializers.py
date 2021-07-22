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
