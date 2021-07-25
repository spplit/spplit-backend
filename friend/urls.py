from django.urls import path
from .views import CardListViewSet, CardRequestViewSet

friendcard_list = CardListViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

friendcard_detail = CardListViewSet.as_view({
    'get': 'retrieve', 
    'put': 'update', 
    'patch': 'partial_update', 
    'delete': 'destroy', 
})

request_list = CardRequestViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

request_detail = CardRequestViewSet.as_view({
    'get': 'retrieve', 
    'put': 'update', 
    'patch': 'partial_update', 
    'delete': 'destroy',
})

request_accept = CardRequestViewSet.as_view({'post':'accept'})
request_decline = CardRequestViewSet.as_view({'post':'decline'})

urlpatterns = [
    path('friendcard', friendcard_list, name="friendcard-list"),
    path('friendcard/<int:pk>/', friendcard_detail, name="friendcard-detail"),
    path('request',request_list, name="request-list"),
    path('request/<int:pk>/', request_detail, name="request-detail"),
]