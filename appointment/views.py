from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import status
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from friend.models import CardList
from card.models import MyCard, Card
from django.db.models import Q


class AppointmentListViewSet(viewsets.ModelViewSet):
 
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    queryset = AppointmentList.objects.all()
    serializer_class = AppointmentListSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.user.is_authenticated :
            qs = qs.filter(user1 = self.request.user) | qs.filter(user2 = self.request.user)

        else :
            qs = qs.none()
        return qs




class AppointmentRequestViewSet(viewsets.ModelViewSet):
    '''
        Functions
            create : post override
                     send appointment request
                     본인에게 요청, 이미 추가된 약속 요청, 이미 요청된 카드에 대한 약속 방지
            accept : 타인이 자신에게 보낸 요청 승인 (본인이 보낸 요청 승인 방지)
            decline : 타인이 자신에게 보낸 요청 거부 (본인이 보낸 요청 거부 방지)
            cancel : 본인이 보낸 요청 취소 (타인이 보낸 요청 취소 방지)
    '''

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    queryset = AppointmentRequest.objects.all()
    serializer_class = AppointmentRequestSerializer


    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.user.is_authenticated :
            qs = qs.filter(sender = self.request.user) | qs.filter(receiver = self.request.user)
        else :
            qs = qs.none()
        return qs


    def create(self, request, *args, **kwargs):
        # 지금 선택된 카드의 인덱스값을 받아서 현재 선택된 카드의 본래 작성자 누구인지 찾기 -> receiver에 할당

        active_card = self.request.POST['active_card']
        receiver = get_object_or_404(Card, id=active_card).friend_card.author
        
        if receiver == self.request.user:
            return Response("You can't add your appointment to yourself",status=status.HTTP_404_NOT_FOUND)

        serializer = AppointmentRequestSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(sender=self.request.user, receiver=receiver)
            return Response({"message": "Appointment Request has been sent"}, status=status.HTTP_201_CREATED, )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, method=["GET"])
    def accept(self, request, pk=None):
        request = get_object_or_404(AppointmentRequest, pk=pk)
        if request.sender == self.request.user :
            return Response("You can't add your appointment to yourself", status=status.HTTP_404_NOT_FOUND)

        request.accept()
        request.delete()
        return Response(status=status.HTTP_200_OK)


    @action(detail=True, method=["GET"])
    def decline(self, request, pk=None):
        request = get_object_or_404(AppointmentRequest, pk=pk)
        if request.sender == self.request.user:
            return Response("You can't decline your request, if you want to delete request you sent cancel request",status=status.HTTP_404_NOT_FOUND)

        request.decline()
        request.delete()
        return Response(status=status.HTTP_200_OK)

    #cancel은 그냥 request detail에서 delete해도 되는 것 같음, 확인 필요
    @action(detail=True, method=["GET"])
    def cancel(self, request, pk=None):
        request = get_object_or_404(AppointmentRequest, pk=pk)
        if request.sender == self.request.user:
            request.cancel()
            request.delete()
            return Response(status=status.HTTP_200_OK)
            
        return Response("You can't cancel request of another people",status=status.HTTP_404_NOT_FOUND)  