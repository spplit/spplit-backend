from rest_framework import fields, serializers
from .models import CardList, CardRequest

class CardListSerializers(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = CardList
        fields = ('pk', 'user_name', 'cards',)

class CardRequestSerializers(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.username')

    class Meta:
        model = CardRequest
        fields = ('pk', 'sender', 'receiver', 'cardId', 'timestamp', 'is_active',)