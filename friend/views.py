from django.shortcuts import render
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
from card.models import MyCard, Card
from .models import CardList, CardRequest
from .serializers import CardListSerializers, CardRequestSerializers

class CardListViewSet(viewsets.ModelViewSet):
    '''
        내가 소유한 타인의 카드 list
    '''

    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    queryset = CardList.objects.all()
    serializer_class = CardListSerializers

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CardRequestViewSet(viewsets.ModelViewSet):
    '''
        QR 인식을 통해 sender(QR 인식자)가 receiver(QR 제공자)에게 권한 요청

        Functions
            create : post override
                     send friend request
                     본인에게 요청, 이미 추가된 카드 요청, 이미 요청된 카드에 대한 요청 방지
            accept : 타인이 자신에게 보낸 요청 승인 (본인이 보낸 요청 승인 방지)
            decline : 타인이 자신에게 보낸 요청 거부 (본인이 보낸 요청 거부 방지)
            cancel : 본인이 보낸 요청 취소 (타인이 보낸 요청 취소 방지)
    '''

    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    queryset = CardRequest.objects.all()
    serializer_class = CardRequestSerializers

 
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def create(self, request, *args, **kwargs):
        cardId = self.request.POST['cardId']
        receiver = get_object_or_404(MyCard, id=cardId).author
        if receiver == self.request.user:
            return Response("You can't add your namecard to your account card list",status=status.HTTP_404_NOT_FOUND)

        card_request = CardRequest.objects.filter(sender=self.request.user, receiver=receiver, cardId=cardId)
        if card_request:
            return Response("You already send a friend request to her/him",status=status.HTTP_409_CONFLICT)

        card_exist = Card.objects.filter(owner=self.request.user, friend_card=cardId)
        if card_exist:
            return Response("You already add this card to your friend card list",status=status.HTTP_409_CONFLICT)

        serializer = CardRequestSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=self.request.user, receiver=receiver)
            return Response(status=status.HTTP_200_OK)

    @action(detail=True, method=["GET"])
    def accept(self, request, pk=None):
        request = get_object_or_404(CardRequest, pk=pk)
        if request.sender == self.request.user:
            return Response("You can't add your namecard to your account card list",status=status.HTTP_404_NOT_FOUND)

        request.accept()
        request.delete()
        return Response(status=status.HTTP_200_OK)


    @action(detail=True, method=["GET"])
    def decline(self, request, pk=None):
        request = get_object_or_404(CardRequest, pk=pk)
        if request.sender == self.request.user:
            return Response("You can't decline your request, if you want to delete request you sent cancel request",status=status.HTTP_404_NOT_FOUND)

        request.decline()
        request.delete()
        return Response(status=status.HTTP_200_OK)

    #cancel은 그냥 request detail에서 delete해도 되는 것 같음, 확인 필요
    @action(detail=True, method=["GET"])
    def cancel(self, request, pk=None):
        request = get_object_or_404(CardRequest, pk=pk)
        if request.sender == self.request.user:
            request.cancel()
            request.delete()
            return Response(status=status.HTTP_200_OK)
            
        return Response("You can't cancel request of another people",status=status.HTTP_404_NOT_FOUND)  

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'mycard' : reverse('mycard-list',request=request, format=format),
        'card' : reverse('card-list',request=request, format=format),
        'friendcard' : reverse('friendcard-list',request=request, format=format),
        'request' : reverse('request-list',request=request, format=format),
    })