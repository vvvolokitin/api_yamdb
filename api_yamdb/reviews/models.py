from django.db import models

from .validators import slug_validator, year_validator
from core.constants import MAX_LENGTH_NAME, MAX_LENGTH_SLUG


class Category(models.Model):
    """Модель 'Категории'."""

    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Название',
        help_text='Выберите категорию'
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH_SLUG,
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
    """Модель 'Жанры'."""

    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Название',
        help_text='Выберите жанр'
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH_SLUG,
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


class Title(models.Model):
    """Модель 'Произведения'."""

    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Название',
        help_text='Выберите название произведения'
    )
    year = models.IntegerField(
        verbose_name='Год',
        validators=[
            year_validator,
        ],
        null=True,
        blank=True,
        help_text=(
            'Год выпуска не может быть больше текущего.'
        ),
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name='titles',
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles',
    )
