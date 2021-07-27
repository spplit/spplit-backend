from django.db import models
from django.conf import settings
from django.shortcuts import get_object_or_404
from card.models import MyCard, Card

class CardList(models.Model):
    ''''
        한 유저당 하나의 row만 갖고 있음

        user : user 모델
        cards : user가 소유하고 있는 카드 목록 

        Functions 
            add_card : 해당 유저의 카드 목록에 card를 추가
                args : cardId - 추가할 카드의 uuid
            remove_card : 해당 유저의 카드 목록에서 card를 제거
                args : removee - 제거할 카드
    '''
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
    cards = models.ManyToManyField('card.MyCard', blank=True, related_name="cards")

    def __str__(self):
        return self.user.username

    def add_card(self, cardId):
        card = get_object_or_404(MyCard, id=cardId)

        self.cards.add(card)
        self.save

    def remove_card(self, removee):
        if removee in self.cards.all():
            self.cards.remove(removee)

    
class CardRequest(models.Model):
    '''
        sender : QR 코드 인식하고 카드 추가 요청한 user
        receiver : QR 코드 제공한 user
        cardId : card의 uuid
        timestamp : request가 요청되어 생성된 시간
        is_active : request가 진행중이면 True  accept/decline/cancel되어 진행중이 아니라면 False

        Functions
            accept : request accept (receiver)
            decline : request decline (receiver)
            cancel : request cancel (sender)
    '''
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, related_name="receiver")
    cardId = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = True

    def __str__(self):
        return self.sender.username

    def accept(self):
        sender_card_list = CardList.objects.filter(user=self.sender).first()
        receiver_card = MyCard.objects.filter(id=self.cardId).first()
        if not sender_card_list:
            print("모델 row 존재하지 않음 -> 생성")
            sender_card_list = CardList(user=self.sender)
            sender_card_list.save()
        
        sender_card_list.add_card(cardId=self.cardId)
        if receiver_card:
            card = Card(owner=self.sender, friend_card=receiver_card)
            card.save()
        self.is_active = False
        self.save()

    def decline(self):
        self.is_active = False
        self.save()

    def cancel(self):
        self.is_active = False
        self.save()