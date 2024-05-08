from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination


from .mixins import ListCreateDestroyViewSet
from .permissions import CustomObjectPermissions
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer
from reviews.models import Category, Genre, Title


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет получения, добавления и удаления категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (
        CustomObjectPermissions,
    )


class GenreViewSet(ListCreateDestroyViewSet):
    """Вьюсет получения, добавления и удаления жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (
        CustomObjectPermissions,
    )


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет получения, добавления и удаления произведений."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (
        CustomObjectPermissions,
    )
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(
            category=get_object_or_404(
                Category, slug=self.request.data.get('category')
            ),
            genre=Genre.objects.filter(
                slug__in=self.request.data.getlist('genre')
            ),
        )

    def perform_update(self, serializer):
        self.perform_create(serializer)
