from django.db import models, transaction
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, phone, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, phone=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, phone, password, **extra_fields)

    def create_superuser(self, email, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin) :
    email = models.EmailField('이메일', unique=True)
    username = models.CharField('유저명', max_length=30, unique=False)
    phone = models.CharField('번호', max_length=30)

    is_staff = models.BooleanField('스태프 권한', default=False)
    is_active = models.BooleanField('사용중', default=True)
    date_joined = models.DateTimeField('가입일', default=timezone.now)

    objects = UserManager()
    
    USERNAME_FIELD = 'email'                     
    REQUIRED_FIELDS = ['username', 'phone']                 

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        swappable = 'AUTH_USER_MODEL'
                


class Category(models.Model) :
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cateogory_user")

    category1 = models.CharField(max_length=30, default="All", null=False, blank=False, editable=False)
    category2 = models.CharField(max_length=30, default="Bookmark", null=False, blank=False, editable=False)
    category3 = models.CharField(max_length=30, default="Work", null=False, blank=False) # null=True?
    category4 = models.CharField(max_length=30, default="Teams", null=False, blank=False) # null=True?
    category5 = models.CharField(max_length=30, null=True, blank=True)
    category6 = models.CharField(max_length=30, null=True, blank=True)
    category7 = models.CharField(max_length=30, null=True, blank=True)
    category8 = models.CharField(max_length=30, null=True, blank=True)
    category9 = models.CharField(max_length=30, null=True, blank=True)
    category10 = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'Category_table'
        verbose_name = '카테고리'
        verbose_name_plural = '카테고리'

class Division(models.Model) :
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="division_user")

    category1 = models.CharField(max_length=30, default="All", null=False, blank=False, editable=False)
    is_checked_category1 = models.BooleanField(default=True, editable=False)
    category2 = models.CharField(max_length=30, default="Bookmark", null=False, blank=False, editable=False)
    is_checked_category2 = models.BooleanField(default=True, editable=False)
    category3 = models.CharField(max_length=30, default="Work", null=False, blank=False, editable=False)
    is_checked_category3 = models.BooleanField(default=True, null=True, blank=True)
    category4 = models.CharField(max_length=30, default="Group", null=False, blank=False, editable=False)
    is_checked_category4 = models.BooleanField(default=True, null=True, blank=True)
    category5 = models.CharField(max_length=30, default="Sports", null=False, blank=False, editable=False)
    is_checked_category5 = models.BooleanField(default=False, null=True, blank=True)
    category6 = models.CharField(max_length=30, default="Hobby", null=False, blank=False, editable=False)
    is_checked_category6 = models.BooleanField(default=False, null=True, blank=True)
    category7 = models.CharField(max_length=30, default="Others", null=False, blank=False, editable=False)
    is_checked_category7 = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'Division_table'
        verbose_name = '카테고리목록'
        verbose_name_plural = '카테고리목록'
    