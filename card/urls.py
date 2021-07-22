from django.urls import path
from .views import *

mycard_list = MyCardViewSet.as_view({
    'get': 'list',
    'post': 'create',
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

urlpatterns = [

    path('mycard/', mycard_list),
    path('mycard/<int:pk>', mycard_detail),

    path('card/add', CardAddView.as_view()),
    path('card/', card_list),
    path('card/<int:pk>', card_detail),

]

