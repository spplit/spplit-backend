from django.db import models
from django.conf import settings
import uuid

class MyCard(models.Model):
    '''
        id : qr에 첨부되는 명함별 식별 id
        author : 명함 주인
        tag1, tag2, tag3 : 명함 주인이 작성하는 필수 태그

    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)

    name = models.CharField(max_length = 20, verbose_name = '이름')
    job = models.CharField(max_length = 20, verbose_name = '직업')
    phone = models.CharField(max_length = 20, verbose_name = '번호')
    email = models.CharField(max_length = 50, verbose_name = '이메일')

    tag1= models.CharField(max_length = 20, verbose_name = '태그1', default='태그1')
    tag2= models.CharField(max_length = 20, verbose_name = '태그2', default='태그2')
    tag3= models.CharField(max_length = 20, verbose_name = '태그3', default='태그3')
    
    register_date = models.DateTimeField(auto_now_add=True, verbose_name = '등록날짜')
    update_date = models.DateTimeField(auto_now=True, verbose_name = '마지막수정일')

    def __str__(self):
        return self.name

    class Meta :
        db_table = 'MyCard_table'
        verbose_name = '내명함'
        verbose_name_plural = '내명함'

class Card(models.Model):
    '''
        owner : 타인의 명함을 소유하고 있는 사람
        friend_card : 타인의 명함, MyCard를 참조하고 있기에 MyCard의 pk값인 uuid를 값으로 갖는다
        custom_tag : 명함 소유자가 임의로 추가할 수 있는 태그
        notes : 명함 소유자가 임의로 작성할 수 있는 노트
        division : 명함 소유자가 편리한 분류를 위해 구분하는 속성
        isBookmarked : 즐겨찾는 명함에 대한 bookmark, 기본값 false
    '''
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