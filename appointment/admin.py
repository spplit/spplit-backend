from django.contrib import admin
from .models import *

class AppointmentRequestAdmin(admin.ModelAdmin) :
    list_display = ('id', 'sender', 'receiver', 'title', 'appointment_date',)
    list_display_links = ('id', 'title',)

class AppointmentListAdmin(admin.ModelAdmin) :
    list_display = ('id', 'user1', 'user2', 'title', 'appointment_date',)
    list_display_links = ('id', 'title',)


admin.site.register(AppointmentRequest, AppointmentRequestAdmin)
admin.site.register(AppointmentList, AppointmentListAdmin)
