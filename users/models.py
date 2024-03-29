from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    """Модель пользователя
    авторизация по email"""
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    telegram_id = models.CharField(max_length=30, verbose_name='Телеграм', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'пользователя'
        verbose_name_plural = 'пользователей'