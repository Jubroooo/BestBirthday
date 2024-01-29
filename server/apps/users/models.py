from django.db import models
from django.contrib.auth.models import AbstractUser

class user(AbstractUser) : 
    name = models.CharField('이름', max_length=10)
    nickname = models.CharField('닉네임', max_length=24)
    birthday = models.DateField('생일')
    toss_account = models.CharField('토스 송금링크', max_length=100, blank=True, null=True)
    kakao_account = models.CharField('카카오 송금링크', max_length=100, blank=True, null=True)
    