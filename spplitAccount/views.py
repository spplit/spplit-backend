from card.models import Card
from django.conf import settings
from django.utils import datastructures
from django.utils.text import phone2numeric
from rest_framework.fields import NullBooleanField
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, viewsets
from .models import *
from .serializers import *
from rest_auth.registration.views import RegisterView
from rest_auth.utils import import_callable


serializers = getattr(settings, 'REST_AUTH_REGISTER_SERIALIZERS', {})
CustomRegisterSerializer = import_callable(
    serializers.get('REGISTER_SERIALIZER', CustomRegisterSerializer))

#회원가입 custom
class CustomRegisterView(RegisterView) :
    serializer_class = CustomRegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        custom_data = {"status": status.HTTP_201_CREATED, "message": "User Register Success"}
        response.data.update(custom_data)
        
        return response


# 유저정보 조회
class UserInfoViewSet(viewsets.ModelViewSet) :
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

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
            return Response({"message": "number changed to " + str(serializer.data)}, status=status.HTTP_200_OK)
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
                return Response({"message": "Wrong password"}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"message": "Password change success"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 카테고리 조회
class CategoryViewSet(viewsets.ModelViewSet) :
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.user.is_authenticated :
            
            category_list = Category.objects.filter(user = self.request.user)
            if not category_list :
                category_list = Category(user = self.request.user)
                category_list.save()
            
            qs = qs.filter(user = self.request.user)
            
        else :
            qs = qs.none()
        return qs

# 카테고리 추가/삭제/수정
class ChangeCategoryView(generics.UpdateAPIView) :

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    model = Category
    serializer_class = ChangeCategorySerializer

    def update(self, request, *args, **kwargs):
        category = Category.objects.filter(user = self.request.user).first()
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid() :
            category.category3 = serializer.data.get("category3")
            category.category4 = serializer.data.get("category4")
            category.category5 = serializer.data.get("category5")
            category.category6 = serializer.data.get("category6")
            category.category7 = serializer.data.get("category7")
            category.category8 = serializer.data.get("category8")
            category.category9 = serializer.data.get("category9")
            category.category10 = serializer.data.get("category10")

            category.save()
            return Response({"message": "Category has been successfully updated"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 카테고리 조회
class DivisionViewSet(viewsets.ModelViewSet) :
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    queryset = Division.objects.all()
    serializer_class = DivisionSerializer


    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.user.is_authenticated :
            
            division_list = Division.objects.filter(user = self.request.user)
            if not division_list :
                category_list = Division(user = self.request.user)
                category_list.save()
            
            qs = qs.filter(user = self.request.user)
            
        else :
            qs = qs.none()
        return qs

# 카테고리 추가/삭제/수정 - isChecked만 수정 가능 / isChecked_categroy1, isChecked_category2는 무조건 true, 총 true는 무조건 4와 같아야함
class ChangeDivisionView(generics.UpdateAPIView) :

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    model = Division
    serializer_class = ChangeDivisionSerializer

    def update(self, request, *args, **kwargs):
        division = Division.objects.filter(user = self.request.user).first()
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid() :
            division.is_checked_category3 = serializer.data.get("is_checked_category3")
            division.is_checked_category4 = serializer.data.get("is_checked_category4")
            division.is_checked_category5 = serializer.data.get("is_checked_category5")
            division.is_checked_category6 = serializer.data.get("is_checked_category6")
            division.is_checked_category7 = serializer.data.get("is_checked_category7")

            is_checked_list = []
            is_checked_list.append(division.is_checked_category3)
            is_checked_list.append(division.is_checked_category4)
            is_checked_list.append(division.is_checked_category5)
            is_checked_list.append(division.is_checked_category6)
            is_checked_list.append(division.is_checked_category7)

            print(is_checked_list)
            cnt_true = 0
            for i in range(len(is_checked_list)) :
                if is_checked_list[i] == "True" :
                    cnt_true += 1
            
            print(is_checked_list)
            print(cnt_true)

            if cnt_true == 2 :
                division.save()
                return Response({"message": "Category has been successfully updated"}, status=status.HTTP_200_OK)
            return Response({"message": "You should select totally 4 categories"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

