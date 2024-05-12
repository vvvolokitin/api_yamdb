from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from core.constants import MAX_EMAIL_LENGTH, MAX_USER_NAME_LENGTH
from reviews.models import Category, Genre, Title, Comment, Review

User = get_user_model()


def name_is_not_me(username):
    if username == 'me':
        raise serializers.ValidationError('Имя не может быть <me>')


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер категорий."""

    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
        )


class GenreSerializer(serializers.ModelSerializer):
    """Сериалайзер жанров."""

    class Meta:
        model = Genre
        fields = (
            'name',
            'slug',
        )


class TitleSerializer(serializers.ModelSerializer):
    """Сериалайзер произведений."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating',
        )


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериалайзер для создания новых пользователей."""

    email = serializers.EmailField(
        max_length=MAX_EMAIL_LENGTH,
        allow_blank=False,
        required=True,
    )
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=MAX_USER_NAME_LENGTH,
        allow_blank=False,
        required=True,
    )

    def validate(self, attrs):
        """
        Проверка на имя 'me' и уникальность имени с email по отдельности,
        если юзер с таким именем и почтой существует,
        то ошибки нет(необходимо для повторной отправки кода подтверждения)
        """

        username = attrs.get('username')
        email = attrs.get('email')

        name_is_not_me(username)
        user_by_username = User.objects.filter(username=username).first()
        user_by_email = User.objects.filter(email=email).first()

        if user_by_username and not user_by_email:
            raise serializers.ValidationError(
                'Пользователь с таким именем уже существует'
            )
        if user_by_email and not user_by_username:
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует'
            )

        return attrs

    class Meta:
        model = User
        fields = ('username', 'email')


class UserRecieveTokenSerializer(serializers.Serializer):
    """Сериализатор для объекта класса User при получении токена JWT."""

    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=MAX_USER_NAME_LENGTH,
        allow_blank=False,
        required=True
    )
    confirmation_code = serializers.CharField(
        allow_blank=False,
        required=True
    )


class SimpleUserSerializer(serializers.ModelSerializer):
    """Сериалайзер пользователя для самого пользователя"""

    email = serializers.EmailField(
        max_length=MAX_EMAIL_LENGTH,
        allow_blank=False,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=MAX_USER_NAME_LENGTH,
        allow_blank=False,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    def validate(self, attrs):
        """Проверка на имя 'me'"""
        username = attrs.get('username')
        name_is_not_me(username)
        return attrs

    class Meta():
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)


class AdminUserSerializer(SimpleUserSerializer):
    """Сериалайзер пользователя для супер юзера"""

    class Meta():
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'pub_date')
        read_only_fields = ('author',)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер отзывов."""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)
    title = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'author', 'title', 'text', 'score', 'pub_date')
        read_only_fields = ('author', 'title')

        def validate(self, data):
            """Проверка на наличие отзыва."""
            if Review.objects.filter(
                    author=self.context['request'].user,
                    title=self.context['title']
            ).exists():
                raise serializers.ValidationError(
                    'Отзыв уже существует'
                )
            return data
