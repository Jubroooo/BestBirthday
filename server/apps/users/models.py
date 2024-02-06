from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser) : 
    first_name=None
    last_name=None
    username = models.CharField('아이디', unique=True, max_length=16, null=True, blank=True)
    nickname = models.CharField('닉네임', unique=True, max_length=24, null=True, blank=True)
    birthday = models.DateField('생일', null = True, blank=True)
    toss_account = models.CharField('토스 송금링크', max_length=100, blank=True, null=True)
    kakao_account = models.CharField('카카오 송금링크', max_length=100, blank=True, null=True)
    profile = models.ImageField('프로필', blank=True, upload_to='profiles/%Y%m%d', null=True)
    def __str__(self):
        return f'({self.nickname})'
