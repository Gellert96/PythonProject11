from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя с авторизацией по email."""

    username = None

    email = models.EmailField(
        unique=True,
        verbose_name="Электронная почта",
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        blank=True,
        null=True,
        verbose_name="Аватар",
    )
    phone = models.CharField(
        max_length=35,
        blank=True,
        verbose_name="Номер телефона",
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Страна",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: ClassVar[list[str]] = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
