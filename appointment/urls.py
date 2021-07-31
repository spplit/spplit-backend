from django.urls import path
from .views import *

appointment_list = AppointmentListViewSet.as_view({
    'get': 'list',
    # 'post': 'create', # 개별 생성 불가 / Request를 통해서만 약속을 잡을 수 있음
})

appointment_detail = AppointmentListViewSet.as_view({
    'get': 'retrieve', 
    # 'put': 'update',  # 생성된 개별 약속 개체는 조회만 가능. 임의로 수정 및 삭제 불가능
    # 'patch': 'partial_update', 
    # 'delete': 'destroy', 
})

appointment_request_list = AppointmentRequestViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

appointment_request_detail = AppointmentRequestViewSet.as_view({
    'get': 'retrieve', 
    # 'put': 'update', 
    # 'patch': 'partial_update', 
    # 'delete': 'destroy',
})

appointment_request_accept = AppointmentRequestViewSet.as_view({'get':'accept'})
appointment_request_decline = AppointmentRequestViewSet.as_view({'get':'decline'})
appointment_request_cancel = AppointmentRequestViewSet.as_view({'get':'cancel'})

urlpatterns = [
    path('appointment', appointment_list,),
    path('appointment/<int:pk>/', appointment_detail),
    path('appointment/request',appointment_request_list),
    path('appointment/request/<int:pk>/', appointment_request_detail),
    path('appointment/request/<int:pk>/accept', appointment_request_accept),
    path('appointment/request/<int:pk>/decline', appointment_request_decline),
    path('appointment/request/<int:pk>/cancel', appointment_request_cancel),
]

