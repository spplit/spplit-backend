from django.urls import path
from .views import CardListViewSet, CardRequestViewSet, api_root

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

request_accept = CardRequestViewSet.as_view({'get':'accept'})
request_decline = CardRequestViewSet.as_view({'get':'decline'})
request_cancel = CardRequestViewSet.as_view({'get':'cancel'})

urlpatterns = [
    path('', api_root),
    path('friendcard', friendcard_list, name="friendcard-list"),
    path('friendcard/<int:pk>/', friendcard_detail, name="friendcard-detail"),
    path('request',request_list, name="request-list"),
    path('request/<int:pk>/', request_detail, name="request-detail"),
    path('request/<int:pk>/accept', request_accept, name="request-accept"),
    path('request/<int:pk>/decline', request_decline, name="request-decline"),
    path('request/<int:pk>/cancel', request_cancel, name="request-cancel"),
]