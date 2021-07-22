from django.urls import path
from .views import *
from rest_auth.views import ( LoginView, LogoutView)
from rest_auth.registration.views import RegisterView

user_info = UserInfoViewSet.as_view({
    'get': 'list',
})

user_detail = UserInfoViewSet.as_view({
    'patch': 'partial_update',
})

urlpatterns = [
    
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    # path('logout/', UserLogoutView.as_view()),
    path('logout/', LogoutView.as_view()),

    path('password/change', ChangePasswordView.as_view()),

    path('user/', user_info),
    path('user/change', ChangeUserInfoView.as_view()),
]

