from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .mixins import ValidateUsernameMixin
from .utils import send_confirmation_code
from .validators import username_and_email_are_unique
from core.constants import MAX_EMAIL_LENGTH, MAX_USER_NAME_LENGTH
from reviews.models import Category, Comment, Genre, Review, Title

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


class UserCreateSerializer(ValidateUsernameMixin, serializers.Serializer):
    """Сериалайзер для создания новых пользователей."""

    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=MAX_USER_NAME_LENGTH
    )
    email = serializers.EmailField(
        max_length=MAX_EMAIL_LENGTH
    )

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        username_and_email_are_unique(username, email)
        return attrs

    def save(self, **kwargs):
        username = self.validated_data.get('username')
        email = self.validated_data.get('email')
        user, _ = User.objects.get_or_create(
            username=username,
            email=email
        )
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
        max_length=MAX_USER_NAME_LENGTH
    )
    confirmation_code = serializers.CharField()


class UserSerializer(ValidateUsernameMixin, serializers.ModelSerializer):
    """Сериалайзер пользователя."""

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
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'author',
            'text',
            'score',
            'pub_date'
        )

    def validate(self, data):
        """Проверка на наличие отзыва."""
        request = self.context.get('request')
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        if request.method != 'POST':
            return data
        if Review.objects.filter(title=title_id, author=author).exists():
            raise serializers.ValidationError(
                'Вы уже оставили отзыв на это произведение'
            )
        return data
