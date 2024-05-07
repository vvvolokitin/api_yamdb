from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from rest_framework import filters, viewsets, mixins, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action

from .mixins import ListCreateDestroyViewSet
from .permissions import CustomObjectPermissions, IsSuperUser
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    UserCreateSerializer,
    UserRecieveTokenSerializer,
    SimpleUserSerializer, 
    AdminUserSerializer
)
from reviews.models import Category, Genre
from .utils import send_confirmation_code


User = get_user_model()


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет получения, добавления и удаления категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyViewSet):
    """Вьюсет получения, добавления и удаления жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class UserCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Вьюсет для создания новых пользователей"""

    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        """Создает объект класса User и
        отправляет на почту пользователя код подтверждения."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, created = User.objects.get_or_create(
            **serializer.validated_data
        )

        confirmation_code = default_token_generator.make_token(user)
        send_confirmation_code(
            email=user.email,
            code=confirmation_code
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserReceiveTokenViewSet(
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    """Вьюсет для получения токена"""

    queryset = User.objects.all()
    serializer_class = UserRecieveTokenSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        """Предоставляет пользователю JWT токен по коду подтверждения."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')

        user = get_object_or_404(User, username=username)

        if not default_token_generator.check_token(user, confirmation_code):
            message = {'confirmation_code': 'Некорректный код подтверждения'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        message = {'token': str(AccessToken.for_user(user))}
        return Response(message, status=status.HTTP_200_OK)


class UserViewSet(
    viewsets.ModelViewSet
):
    """
    Вьюсет для получения/создания/обновления/удаления новых пользователей
    админом либо самим пользователем
    """

    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = (IsSuperUser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=('get', 'patch', 'delete'),
        detail=False,
        url_path=r'(?P<username>[\w.@+-]+)',
    )
    def get_user_by_username(self, request, username):
        """
        Извлечение данных пользователя по его username
        админом и обновление/удаление информации
        """
        user = get_object_or_404(User, username=username)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = AdminUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=('get', 'patch'),
        url_path='me',
        permission_classes=(IsAuthenticated,)
    )
    def get_my_data(self, request):
        """Позволяет пользователю получить подробную информацию о себе
        и редактировать её."""
        if request.method == 'PATCH':
            serializer = SimpleUserSerializer(
                request.user, data=request.data,
                partial=True, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = AdminUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)