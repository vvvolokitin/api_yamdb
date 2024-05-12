from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from .validators import slug_validator, year_validator
from core.constants import MAX_LENGTH_NAME, MAX_LENGTH_SLUG
from users.models import MyUser

COMMENT_LENGHT = 15


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


class Review(models.Model):
    """Модель 'Отзывы'."""
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        MyUser, on_delete=models.CASCADE,
        verbose_name='Автор', related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name='Произведение',
        related_name='reviews')
    score = models.IntegerField(validators=[
        MinValueValidator(1), MaxValueValidator(10),
    ], verbose_name='Рейтинг', null=True)
    pub_date = models.DateTimeField('Дата публикации',
                                    auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('pub_date',)

    def __str__(self):
        return f'{self.title} - {self.author}'


class Comment(models.Model):
    """Модель 'Комментарии'."""
    review = models.ForeignKey(
        Review, verbose_name='Произведение', on_delete=models.CASCADE,
        related_name='comments')
    text = models.TextField('Текст комментария')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    author = models.ForeignKey(
        MyUser, verbose_name='Автор', on_delete=models.CASCADE,
        related_name='comments')
    pub_date = models.DateTimeField('Дата публикации',
                                    auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_at',)

        def __str__(self):
            return self.text[:COMMENT_LENGHT]
