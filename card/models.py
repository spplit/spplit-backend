from django.db import models
from django.conf import settings
import uuid

class MyCard(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)

    name = models.CharField(max_length = 20, verbose_name = '이름')
    job = models.CharField(max_length = 20, verbose_name = '직업')
    phone = models.CharField(max_length = 20, verbose_name = '번호')
    email = models.CharField(max_length = 50, verbose_name = '이메일')

    tag1= models.CharField(max_length = 20, verbose_name = '태그1', default='태그1')
    tag2= models.CharField(max_length = 20, verbose_name = '태그2', default='태그2')
    tag3= models.CharField(max_length = 20, verbose_name = '태그3', default='태그3')
    
    # unique_num = models.IntegerField(default=0, verbose_name = '고유번호')
    register_date = models.DateTimeField(auto_now_add=True, verbose_name = '등록날짜')
    update_date = models.DateTimeField(auto_now=True, verbose_name = '마지막수정일')

    def __str__(self):
        return self.name

    class Meta :
        db_table = 'MyCard_table'
        verbose_name = '내명함'
        verbose_name_plural = '내명함'

class Card(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    friend_card = models.ForeignKey(MyCard, on_delete=models.CASCADE) # mycard에서 가져올 카드정보
    custom_tag1 = models.CharField(max_length = 20, verbose_name = '커스텀태그1', blank=True, null=True)
    custom_tag2 = models.CharField(max_length = 20, verbose_name = '커스텀태그2', blank=True, null=True)
    custom_tag3 = models.CharField(max_length = 20, verbose_name = '커스텀태그3', blank=True, null=True)
    custom_tag4 = models.CharField(max_length = 20, verbose_name = '커스텀태그4', blank=True, null=True)
    custom_tag5 = models.CharField(max_length = 20, verbose_name = '커스텀태그5', blank=True, null=True)
    notes = models.TextField(blank=True)
    division = models.CharField(max_length = 30, blank=True)
    isBookmarked = models.BooleanField(default=False)

    register_date = models.DateTimeField(auto_now_add=True, verbose_name = '등록날짜')
    update_date = models.DateTimeField(auto_now=True, verbose_name = '마지막수정일')


    class Meta :
        db_table = 'Card_table'
        verbose_name = '명함'
        verbose_name_plural = '명함'
