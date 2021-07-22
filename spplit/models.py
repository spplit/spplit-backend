from re import M
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import connections, models
from django.utils import timezone
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
import uuid

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("phone", "")
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("phone", "")
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin) :
    email = models.EmailField('이메일', unique=True)
    username = models.CharField('유저명', max_length=30)
    phone = models.CharField('번호', max_length=30)

    is_staff = models.BooleanField('스태프 권한', default=False)
    is_active = models.BooleanField('사용중', default=True)
    date_joined = models.DateTimeField('가입일', default=timezone.now)

    objects = UserManager()
    
    USERNAME_FIELD = 'email'                     
    REQUIRED_FIELDS = ['username']                 

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        swappable = 'AUTH_USER_MODEL'


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
    follow_mycard = models.ForeignKey(MyCard, on_delete=models.CASCADE) # mycard에서 가져올 카드정보
    
    # author_id = models.IntegerField(verbose_name="작성자아이디")
    # name = models.CharField(max_length = 20, verbose_name = '이름')
    # job = models.CharField(max_length = 20, verbose_name = '직업')
    # phone = models.CharField(max_length = 20, verbose_name = '번호')
    # email = models.CharField(max_length = 50, verbose_name = '이메일')
    # tag1= models.CharField(max_length = 20, verbose_name = '태그1')
    # tag2= models.CharField(max_length = 20, verbose_name = '태그2')
    # tag3= models.CharField(max_length = 20, verbose_name = '태그3')
    # unique_num = models.IntegerField(default=0, verbose_name = '고유번호')
    
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

    # def __str__(self):
    #     return self.name

    class Meta :
        db_table = 'Card_table'
        verbose_name = '명함'
        verbose_name_plural = '명함'

# RELATIONSHIP_FOLLOWING = 1
# RELATIONSHIP_BLOCKED = 2
# RELATIONSHIP_STATUSES = (
#     (RELATIONSHIP_FOLLOWING, 'Following'),
#     (RELATIONSHIP_BLOCKED, 'Blocked'),
# )

class Relation(models.Model) :
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, related_name='from_user', on_delete=models.CASCADE) # 팔로우 요청한 유저
    follow_card = models.ForeignKey(Card, on_delete=models.CASCADE)  # 팔로우되어있는 카드번호
    # status = models.IntegerField(choices=RELATIONSHIP_STATUSES)

    class Meta :
        db_table = 'Relation_table'
        verbose_name = '관계'
        verbose_name_plural = '관계'


