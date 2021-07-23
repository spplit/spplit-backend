from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.http.response import Http404
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

    @action(detail=False, method=['POST'])
    def accept(request):
        cardId = self.request.POST['cardId']

    @action(detail=False, method=['POST'])
    def decline(request):
        cardId = self.request.POST['cardId']