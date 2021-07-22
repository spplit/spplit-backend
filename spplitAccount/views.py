from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, viewsets
from .models import *
from .serializers import *

# 유저정보 조회
class UserInfoViewSet(viewsets.ModelViewSet) :
    
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.user.is_authenticated :
            qs = qs.filter(email = self.request.user)
        else :
            qs = qs.none()
        return qs


# 유저정보 변경 - 번호 변경
class ChangeUserInfoView(generics.UpdateAPIView) :

    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    model = User
    serializer_class = ChangeUserInfoSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            self.object.phone = serializer.data.get("phone")
            self.object.save()
            return Response("Phone Change Success.", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 비밀번호 변경
class ChangePasswordView(generics.UpdateAPIView) :

    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    model = User
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response("Password Change Success.", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

