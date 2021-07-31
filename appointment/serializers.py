from rest_framework import fields, serializers
from .models import *

class AppointmentListSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppointmentList
        fields = '__all__'

class AppointmentRequestSerializer(serializers.ModelSerializer):

    sender_name = serializers.ReadOnlyField(source='sender.username')

    class Meta:
        model = AppointmentRequest
        fields = ('id', 'sender_name', 'receiver', 'title',  'content', 'register_date', 'appointment_date', "is_active", )