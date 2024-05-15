from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from core.constants import MAX_EMAIL_LENGTH, MAX_USER_NAME_LENGTH
from reviews.models import Category, Genre, Title, Comment, Review
from .validators import name_is_not_me, username_and_email_are_unique
from .utils import send_confirmation_code

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


class UserCreateSerializer(serializers.Serializer):
    """Сериалайзер для создания новых пользователей."""

    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=MAX_USER_NAME_LENGTH,
        required=True,
    )
    email = serializers.EmailField(
        max_length=MAX_EMAIL_LENGTH,
        required=True,
    )

    class Meta:
        fields = (
            'username',
            'email'
        )

    def validate_username(self, value):
        name_is_not_me(value)
        return value

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        username_and_email_are_unique(username, email)
        return attrs

    def save(self, **kwargs):
        username = self.validated_data.get('username')
        email = self.validated_data.get('email')
        user, _ = User.objects.get_or_create(username=username, email=email)
        confirmation_code = default_token_generator.make_token(user)
        send_confirmation_code(
            email=user.email,
            code=confirmation_code
        )
        return user


class UserRecieveTokenSerializer(serializers.Serializer):
    """Сериализатор для пользователя при получении токена JWT."""

    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=MAX_USER_NAME_LENGTH,
        required=True
    )
    confirmation_code = serializers.CharField(
        required=True
    )

    class Meta:
        fields = (
            'username',
            'confirmation_code'
        )


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер пользователягтш."""

    class Meta():
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

    def validate_username(self, value):
        name_is_not_me(value)
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер комментариев."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'author',
            'text',
            'pub_date'
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер отзывов."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        # default=serializers.CurrentUserDefault()
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
        # default=''
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'author',
            'title',
            'text',
            'score',
            'pub_date'
        )
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=model.objects.all(),
        #         fields=['author', 'title'],
        #         message='Вы уже оставили отзыв на это произведение'
        #     )
        # ]

    def validate(self, data):
        """Проверка на наличие отзыва."""
        request = self.context.get('request')
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (request.method == 'POST' and Review.objects.filter(
                title=title, author=author).exists()):
            raise serializers.ValidationError(
                'Вы уже оставили отзыв на это произведение'
            )
        return data
