from unicodedata import category
from rest_framework import fields, serializers, views
from .models import *
from rest_auth.registration.serializers import RegisterSerializer
from allauth.utils import (email_address_exists, get_username_max_length)
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.utils.translation import gettext as _

# class UserStatusSerializer(serializers.ModelSerializer):
#     user_profile = serializers.StringRelatedField(read_only=True)

#     class Meta:
#         model = User


from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

class CustomRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    username = serializers.CharField(required=True, max_length=30)
    phone = serializers.CharField(required=True, max_length=30)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(
                _("The two password fields didn't match."))
        return data

    def get_cleaned_data(self):
        return {
            'username' : self.validated_data.get('username', ''),
            'phone' : self.validated_data.get('phone', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):

    email = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'phone',)


class ChangePasswordSerializer(serializers.Serializer) :
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ChangeUserInfoSerializer(serializers.Serializer) :

    phone = serializers.CharField(required=True)


class CategorySerializer(serializers.ModelSerializer):

    category1 = serializers.ReadOnlyField()
    category2 = serializers.ReadOnlyField()
    
    class Meta:
        model = Category
        fields = '__all__'


class ChangeCategorySerializer(serializers.Serializer) :

    category3 = serializers.CharField(required=True)
    category4 = serializers.CharField(required=True)
    category5 = serializers.CharField(required=False)
    category6 = serializers.CharField(required=False)
    category7 = serializers.CharField(required=False)
    category8 = serializers.CharField(required=False)
    category9 = serializers.CharField(required=False)
    category10 = serializers.CharField(required=False)


class DivisionSerializer(serializers.ModelSerializer):

    category1 = serializers.ReadOnlyField()
    is_checked_category1 = serializers.ReadOnlyField()
    category2 = serializers.ReadOnlyField()
    is_checked_category2 = serializers.ReadOnlyField()
    
    class Meta:
        model = Division
        fields = '__all__'


class ChangeDivisionSerializer(serializers.Serializer) :

    is_checked_category3 = serializers.CharField()
    is_checked_category4 = serializers.CharField()
    is_checked_category5 = serializers.CharField()
    is_checked_category6 = serializers.CharField()
    is_checked_category7 = serializers.CharField()
