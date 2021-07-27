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

# 내명함 관리 (조회, 추가, 수정, 삭제)
class MyCardViewSet(viewsets.ModelViewSet) :

    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

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


# 남의 명함 관리 조회, 수정, 삭제 -> 명함 삭제 시 관계도 삭제됨
class CardViewSet(viewsets.ModelViewSet) :

    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)

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
        return Response(status=status.HTTP_200_OK)

    # # # test용 / too complicated
    # info = MyCard.objects.filter(id = queryset.values()[0]["follow_mycard_id"])
    # print(info.values()[0]["name"])
    # print(info.values()[0]["job"])
    # print(info.values()[0]["email"])
    # print(info.values()[0]["phone"])
