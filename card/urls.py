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
    'post' : 'create',
})

card_detail = CardViewSet.as_view({
    'get': 'retrieve', 
    'put': 'update', 
    'patch': 'partial_update', 
    'delete': 'destroy', 
})

urlpatterns = [

    path('mycard/', mycard_list),
    path('mycard/<int:pk>', mycard_detail),

    path('card/add', CardAddView.as_view()),
    path('card/', card_list),
    path('card/<int:pk>', card_detail),

]

