import re
from typing import Counter
from django.db.models.fields.related import OneToOneField
from django.views import generic
from rest_framework import generics, viewsets, serializers
from rest_framework import permissions
from rest_framework.views import APIView
from .models import MyCard, User
from .serializers import *
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, logout, models
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from django.contrib.auth import REDIRECT_FIELD_NAME, logout as auth_logout
from django.views.generic import FormView, RedirectView
from django.shortcuts import get_object_or_404, redirect
from django.http.response import Http404
import random
from django.utils import timezone


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

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

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

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

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


# # 로그아웃
# class UserLogoutView(RedirectView):

#     permission_classes = [IsAuthenticated]
#     authentication_classes = [TokenAuthentication]

#     url = '/login/'

#     def get(self, request, *args, **kwargs):
#         auth_logout(request)
#         return super(UserLogoutView, self).get(request, *args, **kwargs)


# 내명함 관리 (조회, 추가, 수정, 삭제)
class MyCardViewSet(viewsets.ModelViewSet) :

    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    queryset = MyCard.objects.all()
    serializer_class = MyCardSerializer

    def perform_create(self, serializer):
        mycards = MyCard.objects.filter(author = self.request.user)
        unique_num = int(str(random.randint(100, 999)) + str(self.request.user.id) + str(len(mycards)) + str(random.randint(100, 999)))
        serializer.save(author = self.request.user, unique_num = unique_num)

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.user.is_authenticated :
            qs = qs.filter(author = self.request.user)
        else :
            qs = qs.none()
        return qs



# qr로 명함 추가 -> 명함 추가 시 관계까지 자동 추가 // 일단 자동으로 추가 / 상대방이 accept하지 않으면 DB에서 바로 삭제(추후 구현)
class CardAddView(APIView) :

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request) :
        serializer = AddCardSerializer(data=request.data)

        if serializer.is_valid() :
            card = MyCard.objects.get(unique_num = request.data["qr_code"])

            if not Card.objects.filter(owner = self.request.user, follow_mycard = card) :
                if not self.request.user.id == card.author_id :

                    # 명함 객체 추가
                    Card.objects.create(owner = self.request.user, follow_mycard = card)

                    # 관계 객체 추가
                    follow_card = Card.objects.filter(owner = self.request.user).get(follow_mycard = card)
                    Relation.objects.create(from_user = self.request.user, follow_card = follow_card)

                    return Response("new card&relation added", status = status.HTTP_201_CREATED)
                return Response("active user is same as the owner of card", status = status.HTTP_400_BAD_REQUEST)
            return Response("already exists", status = status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)



# 남의 명함 관리 조회, 수정, 삭제 -> 명함 삭제 시 관계도 삭제됨
class CardViewSet(viewsets.ModelViewSet) :

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.user.is_authenticated :
            qs = qs.filter(owner = self.request.user)
        else :
            qs = qs.none()
        return qs

    # # test용 / too complicated
    info = MyCard.objects.filter(id = queryset.values()[0]["follow_mycard_id"])
    print(info.values()[0]["name"])
    print(info.values()[0]["job"])
    print(info.values()[0]["email"])
    print(info.values()[0]["phone"])


# 메소드 구분
user_info = UserInfoViewSet.as_view({
    'get': 'list',
})

user_detail = UserInfoViewSet.as_view({
    'patch': 'partial_update',
})

mycard_list = MyCardViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

mycard_add = MyCardViewSet.as_view({
    'post': 'create',
    'get': 'list',
})

mycard_detail = MyCardViewSet.as_view({
    'get': 'retrieve', # 조회
    'put': 'update', # 수정
    'patch': 'partial_update', # 일부만 수정 가능 -> 수정 불가능한 필드는 readonly로 막아버리기
    'delete': 'destroy', # 삭제
})

card_list = CardViewSet.as_view({
    'get': 'list',
})

card_detail = CardViewSet.as_view({
    'get': 'retrieve', # 조회
    'put': 'update', # 수정
    'patch': 'partial_update', # 이건 뭐지
    'delete': 'destroy', # 삭제
})
