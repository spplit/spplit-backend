from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from .models import MyCard, Card
from friend.models import CardList
from .serializers import *

class MyCardViewSet(viewsets.ModelViewSet) :
    '''
        내 명함 관리 (조회, 추가, 수정, 삭제)

        Functions 
            count_user_mycard : 나의 명함을 갖고있는 사람이 몇명인지 count
    '''
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    queryset = MyCard.objects.all()
    serializer_class = MyCardSerializer

    def perform_create(self, serializer):
        serializer.save(author = self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.user.is_authenticated :
            qs = qs.filter(author = self.request.user)
        else :
            qs = qs.none()
        return qs

    @action(detail=True, method=["GET"])
    def count_user_mycard(self, request, pk=None):
        mycard = get_object_or_404(MyCard, pk=pk)
        user_list = Card.objects.filter(friend_card=mycard)
        return Response({'count_user':user_list.count()}, status=status.HTTP_200_OK)


class CardViewSet(viewsets.ModelViewSet) :
    '''
        내가 소유하고 있는 남의 명함 관리 
        (조회, 수정, 삭제 -> 명함 삭제 시 관계도 삭제됨)

        Functions 
            destroy : delete override
                      card list에서 해당 카드 삭제, friend card list에서 해당 카드 삭제
    '''

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)

        # 아래의 코드는 원활한 테스트를 위한 코드, 배포시에는 필요없는 코드임
        card_list = CardList.objects.filter(user=self.request.user).first()
        cardId = self.request.POST['friend_card']
        if not card_list:
            print("모델 row 존재하지 않음 -> 생성")
            card_list = CardList(user=self.request.user)
            card_list.save()
        card_list.add_card(cardId=cardId)
        # 위의 코드는 원활한 테스트를 위한 코드, 배포시에는 필요없는 코드임

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.user.is_authenticated :
            qs = qs.filter(owner = self.request.user)
        else :
            qs = qs.none()
        return qs
    
    def destroy(self, request, pk=None):
        queryset = Card.objects.all()
        owner = get_object_or_404(queryset, pk=pk).owner
        card = get_object_or_404(queryset, pk=pk)
        if owner != self.request.user:
            return Response("You can only delete your friend cards",status=status.HTTP_404_NOT_FOUND)
        card.delete()
        user_cardlist = CardList.objects.get(user=self.request.user)
        user_cardlist.remove_card(card.friend_card)
        return Response(status=status.HTTP_204_NO_CONTENT)
