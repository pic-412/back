from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('이메일을 입력해주세요.')
        email = self.normalize_email(email)
        nickname = extra_fields.pop('nickname', None) or email.split('@')[0]
        user = self.model(email=email, nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(unique=True) 
    password = models.CharField(max_length=32)
    username = None
    nickname = models.CharField(max_length=50)
    
    USERNAME_FIELD = 'email'  # email 유저 식별자 설정
    REQUIRED_FIELDS = []

    objects = UserManager()
    
    def __str__(self):
        return self.nickname