from django.db import models

from .validators import slug_validator


class Category(models.Model):
    """Модель 'Категории'."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        help_text='Выберите категорию'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, дефис и подчёркивание.'
        ),
        validators=[
            slug_validator,
        ]
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        help_text='Выберите жанр'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, дефис и подчёркивание.'
        ),
        validators=[
            slug_validator,
        ]
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
