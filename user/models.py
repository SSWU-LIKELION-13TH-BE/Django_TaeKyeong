from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    nickname=models.CharField(max_length=30)

    id = models.CharField(primary_key=True,max_length=20)
    #암호화가 안된 비번을 저장하기 위해 정의
    raw_password = models.CharField(max_length=128, blank=True, null=True)

    #로그인시에 username 필드를 id로 대체하기 위해 추가해준 코드
    USERNAME_FIELD = 'id'
    
    groups=models.ManyToManyField(Group, related_name="customer_set", blank=True)
    user_permissions= models.ManyToManyField(Permission, related_name="customer_permissions_set", blank=True)
