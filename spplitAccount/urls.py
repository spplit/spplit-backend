from django.urls import path
from .views import *
from rest_auth.views import ( LoginView, LogoutView)
from rest_auth.registration.views import RegisterView

user_info = UserInfoViewSet.as_view({
    'get': 'list',
})

category_list = CategoryViewSet.as_view({
    'get': 'list',
})

division_list = DivisionViewSet.as_view({
    'get': 'list',
})


urlpatterns = [
    
    # path('register', RegisterView.as_view()),
    path('register', CustomRegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),

    path('password/change', ChangePasswordView.as_view()),

    path('user', user_info),
    path('user/change', ChangeUserInfoView.as_view()),

    path('user/category', category_list),
    path('user/category/change', ChangeCategoryView.as_view()),

    path('user/division', division_list),
    path('user/division/change', ChangeDivisionView.as_view()),

]

