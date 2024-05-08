from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from core.constants import MAX_USER_NAME_LENGTH, MAX_EMAIL_LENGTH


class MyUser(AbstractUser):
    class UserRole(models.TextChoices):
        USER = "user"
        MODERATOR = "moderator"
        ADMIN = "admin"

    username = models.CharField(
        max_length=150,
        verbose_name="имя пользователя",
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[\w.@+-]+$",
                message="Недопустимый символ в имя пользователя"
            )
        ],
    )
    email = models.EmailField(
        max_length=MAX_EMAIL_LENGTH, unique=True, verbose_name="email"
    )
    first_name = models.CharField(
        max_length=MAX_USER_NAME_LENGTH, verbose_name="имя", blank=True
    )
    last_name = models.CharField(
        max_length=MAX_USER_NAME_LENGTH, verbose_name="фамилия", blank=True
    )
    bio = models.TextField(verbose_name="биография", blank=True)
    role = models.CharField(
        max_length=20,
        verbose_name="роль",
        choices=UserRole.choices,
        default=UserRole.USER,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username

    def is_admin(self):
        return self.role == MyUser.UserRole.ADMIN

    def is_moderator(self):
        return self.role == MyUser.UserRole.MODERATOR

    def is_user(self):
        return self.role == MyUser.UserRole.USER
