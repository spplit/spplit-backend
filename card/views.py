from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.http.response import Http404
from .models import MyCard
from .serializers import *

# 내명함 관리 (조회, 추가, 수정, 삭제)
class MyCardViewSet(viewsets.ModelViewSet) :

    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    queryset = MyCard.objects.all()
    serializer_class = MyCardSerializer

    def perform_create(self, serializer):
        # mycards = MyCard.objects.filter(author = self.request.user)
        # unique_num = int(str(random.randint(100, 999)) + str(self.request.user.id) + str(len(mycards)) + str(random.randint(100, 999)))
        serializer.save(author = self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.user.is_authenticated :
            qs = qs.filter(author = self.request.user)
        else :
            qs = qs.none()
        return qs



# qr로 명함 추가 -> 명함 추가 시 관계까지 자동 추가 // 일단 자동으로 추가 / 상대방이 accept하지 않으면 DB에서 바로 삭제(추후 구현)
class CardAddView(APIView) :

    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    # 1단계 친구request를 보냄 -> 2단계 친구request수락 -> 3단계 친구request를 지움과 동시에 친구list에 추가 -> 4단계 명함 추가
    def post(self, request) :
        serializer = AddCardSerializer(data=request.data)

        if serializer.is_valid() :
            # card = MyCard.objects.get(unique_num = request.data["qr_code"])
            card = MyCard.objects.get(pk = request.data["qr_code"])

            if not Card.objects.filter(owner = self.request.user, follow_mycard = card) :
                if not self.request.user.id == card.author_id :

                    # 명함 객체 추가
                    Card.objects.create(owner = self.request.user, follow_mycard = card)

                    # 관계 객체 추가
                    follow_card = Card.objects.filter(owner = self.request.user).get(follow_mycard = card)
                    Relation.objects.create(from_user = self.request.user, follow_card = follow_card)

                    return Response("new card&relation added", status = status.HTTP_201_CREATED)
                return Response("active user is same as the owner of card", status = status.HTTP_400_BAD_REQUEST)
            return Response("already exists", status = status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)



# 남의 명함 관리 조회, 수정, 삭제 -> 명함 삭제 시 관계도 삭제됨
class CardViewSet(viewsets.ModelViewSet) :

    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.user.is_authenticated :
            qs = qs.filter(owner = self.request.user)
        else :
            qs = qs.none()
        return qs

    # # # test용 / too complicated
    # info = MyCard.objects.filter(id = queryset.values()[0]["follow_mycard_id"])
    # print(info.values()[0]["name"])
    # print(info.values()[0]["job"])
    # print(info.values()[0]["email"])
    # print(info.values()[0]["phone"])
