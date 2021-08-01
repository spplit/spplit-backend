from django.db import models
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime, time

class AppointmentList(models.Model):
    ''''
        Appointment에서 accept가 되면 자동으로 추가됨

        user1 : AppointmentRequest의 sender
        user2 : AppointmentRequest의 receiver
        title : AppointmentRequest의 title
        content : AppointmentRequest의 content
        appointment_date : AppointmentRequest의 appointment_date
        is_active : 약속이 진행 중인지, 이미 지난 약속인지 파악
        
        Functions 
            expire_appointment : 약속날짜가 지난 약속객체의 is_active를 False로 변경
    '''
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user1")
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user2")
    title = models.CharField(max_length=100, null=False, blank=False)
    content = models.TextField()
    appointment_date = models.CharField(max_length=20, null=False, blank=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'AppointmentList_table'
        verbose_name = '약속목록'
        verbose_name_plural = '약속목록'


    # 약속의 만료 여부 (날짜를 기준으로 판단)
    def check_is_expired(self) :
        now_date = timezone.localdate()
        appointment_date = self.appointment_date # 문자열을 날짜형식으로 변환해야함
        temp_date = datetime.strptime(appointment_date, '%Y/%m/%d').date()

        if temp_date < now_date :
            self.is_active = False
            print("ㅋㅋㅋ 지났네 이미")
        print("아직 멀었음")
        self.save()
    
        
class AppointmentRequest(models.Model):
    '''
        sender : 약속을 요청한 user (receiver의 명함을 가지고 있는 user)
        receiver : 약속을 요청받은 user (sender에게 명함을 건내준 user)
        title : 약속 제목
        content : 약속 내용
        appointment_date : 해당 약속날짜

        register_date : 약속 request가 요청되어 생성된 시간
        is_active : request가 진행중이면 True  accept/decline/cancel되어 진행중이 아니라면 False

        Functions
            accept : request accept (receiver)
            decline : request decline (receiver)
            cancel : request cancel (sender)
    '''
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="appointment_sender")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, related_name="appointment_receiver")
    title = models.CharField(max_length=100, null=False, blank=False)
    content = models.TextField()
    appointment_date = models.CharField(max_length=20)
    register_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.sender.username

    class Meta:
        db_table = 'AppointmentRequest_table'
        verbose_name = '약속요청'
        verbose_name_plural = '약속요청'

    def accept(self):
        appointment_list = AppointmentList.objects.filter(user1=self.sender).filter(user2=self.receiver).filter(appointment_date=self.appointment_date) # .first() ?
        
        if not appointment_list :
            appointment_list = AppointmentList(user1=self.sender, user2=self.receiver, title=self.title, content=self.content, appointment_date=self.appointment_date)
            appointment_list.save()
        
        self.is_active = False
        self.save()

    def decline(self):
        self.is_active = False
        self.save()

    def cancel(self):
        self.is_active = False
        self.save()