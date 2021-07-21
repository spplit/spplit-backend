from django.urls import path
from .views import *
from rest_auth.views import ( LoginView, LogoutView, PasswordChangeView, 
PasswordResetView, PasswordResetConfirmView )
from rest_auth.registration.views import RegisterView

urlpatterns = [

    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    # path('logout/', UserLogoutView.as_view()),
    path('logout/', LogoutView.as_view()),

    path('password/change', ChangePasswordView.as_view()),

    path('user/', user_info),
    path('user/change', ChangeUserInfoView.as_view()), 


    path('mycard/', mycard_list),
    path('mycard/add', mycard_add),
    path('mycard/<int:pk>', mycard_detail),

    path('card/add', CardAddView.as_view()),
    path('card/', card_list),
    path('card/<int:pk>', card_detail),



]