from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from card.models import MyCard
from .models import CardList, CardRequest
from .serializers import CardListSerializers, CardRequestSerializers

class CardListViewSet(viewsets.ModelViewSet):
    queryset = CardList.objects.all()
    serializer_class = CardListSerializers

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CardRequestViewSet(viewsets.ModelViewSet):
    queryset = CardRequest.objects.all()
    serializer_class = CardRequestSerializers

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    # send_friend_request 
    def create(self, request, *args, **kwargs):
        cardId = self.request.POST['cardId']
        if cardId:
            receiver = get_object_or_404(MyCard, id=cardId).author
            card_request = CardRequest.objects.filter(sender=self.request.user, receiver=receiver, cardId=cardId)
            print(card_request)
            if card_request:
                return Response(status=status.HTTP_409_CONFLICT)
            added_card_request = CardRequest(sender=self.request.user, receiver=receiver, cardId=cardId)
            added_card_request.save()
            return Response(status=status.HTTP_200_OK)

