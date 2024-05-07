from rest_framework import serializers
from django.contrib.auth import get_user_model

from reviews.models import Category, Genre
from core.constants import MAX_USER_NAME_LENGTH, MAX_EMAIL_LENGTH
from users.models import MyUser


User = get_user_model()


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


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериалайзер для создания новых пользователей"""

    email = serializers.EmailField(
        max_length=MAX_EMAIL_LENGTH,
        allow_blank=False
    )
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=MAX_USER_NAME_LENGTH,
        allow_blank=False,
    )

    def validate(self, attrs):
        """
        Проверка на имя 'me' и уникальность имени с email по отдельности,
        если юзер с таким именем и почтой существует,
        то ошибки нет(необходимо для повторной отправки кода подтверждения)
        """

        username = attrs.get('username')
        email = attrs.get('email')

        if username == 'me':
            raise serializers.ValidationError('Имя не может быть <me>')

        username_exists = User.objects.filter(username=username).first()
        email_exists = User.objects.filter(email=email).first()
        if username_exists and not email_exists:
            raise serializers.ValidationError(
                'Пользователь с таким именем уже существует'
            )
        if email_exists and not username_exists:
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
    )
    confirmation_code = serializers.CharField(
        allow_blank=False,
    )


class UserSerializer(UserCreateSerializer):
    """Сериалайзер пользователя"""

    first_name = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=MAX_USER_NAME_LENGTH,
        required=True
    )
    last_name = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=MAX_USER_NAME_LENGTH,
        required=True
    )
    role = serializers.ChoiceField(choices=MyUser.UserRole)

    class Meta(UserCreateSerializer.Meta):
        fields = '__all__'
