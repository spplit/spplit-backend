from django.urls import path
from .views import *

mycard_list = MyCardViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
mycard_detail = MyCardViewSet.as_view({
    'get': 'retrieve', 
    'put': 'update', 
    'patch': 'partial_update', 
    'delete': 'destroy',
})

card_list = CardViewSet.as_view({
    'get': 'list',
    #'post' : 'create', #테스트용으로 쓰는 friend card 추가 view 일단 막아둠
})

card_detail = CardViewSet.as_view({
    'get': 'retrieve', 
    'put': 'update', 
    'patch': 'partial_update', 
    'delete': 'destroy', 
})

count_user = MyCardViewSet.as_view({'get':'count_user_mycard'})

urlpatterns = [

    path('mycard/', mycard_list, name="mycard-list"),
    path('mycard/<uuid:pk>', mycard_detail, name="mycard-detail"),
    path('mycard/<uuid:pk>/count', count_user, name="count-user"),
    path('card/', card_list, name="card-list"),
    path('card/<int:pk>', card_detail, name="card-detail"),

]

