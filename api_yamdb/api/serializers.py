from rest_framework import serializers
from django.contrib.auth import get_user_model

from reviews.models import Category, Genre
from core.constants import MAX_USER_NAME_LENGTH, MAX_EMAIL_LENGTH



User = get_user_model()


def name_is_not_me(username):
    if username == 'me':
        raise serializers.ValidationError('Имя не может быть <me>')


def get_user_by_username(username):
    return User.objects.filter(username=username).first()


def get_user_by_email(email):
    return User.objects.filter(email=email).first()


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
        allow_blank=False,
        required=True
    )
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=MAX_USER_NAME_LENGTH,
        allow_blank=False,
        required=True
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
        user_by_username = get_user_by_username(username)
        user_by_email = get_user_by_email(email)

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


class SimpleUserSerializer(UserCreateSerializer):
    """Сериалайзер пользователя для самого пользователя"""

    first_name = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=MAX_USER_NAME_LENGTH,
        allow_blank=False,
        required=True
    )

    last_name = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=MAX_USER_NAME_LENGTH,
        allow_blank=False,
        required=True
    )

    def validate(self, attrs):
        """
        Проверка на имя 'me' и уникальность имени с email,
        при этом проверка не вызывает ошибку если оставить старые имя и email
        """

        username = attrs.get('username')
        email = attrs.get('email')

        name_is_not_me(username)
        user_by_username = get_user_by_username(username)
        user_by_email = get_user_by_email(email)

        if user_by_username and username != self.context.get('request').user.username:
            raise serializers.ValidationError(
                'Пользователь с таким именем уже существует'
            )
        if user_by_email and email != self.context.get('request').user.email:
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует'
            )

        return attrs

    class Meta():
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        read_only_fields = ("role",)


class AdminUserSerializer(SimpleUserSerializer):
    """Сериалайзер пользователя для суперюзера"""

    def validate(self, attrs):
        """
        Проверка на имя 'me' и уникальность имени с email,
        при этом проверка не вызывает ошибку если оставить старые имя и email
        """

        username = attrs.get('username')
        email = attrs.get('email')
        request = self.context.get('request')
        username_from_url = (
            request.parser_context.get('kwargs').get('username')
        )

        name_is_not_me(username)
        user_by_username = get_user_by_username(username)
        user_by_email = get_user_by_email(email)
        user_from_url = get_user_by_username(username_from_url)

        if user_by_username and username_from_url != user_by_username.username:
            raise serializers.ValidationError(
                'Пользователь с таким именем уже существует'
            )
        if user_by_email and email != user_from_url.email:
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует'
            )

        return attrs

    class Meta():
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
