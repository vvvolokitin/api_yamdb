from django.shortcuts import render
from rest_framework import filters, viewsets


from .mixins import ListCreateDestroyViewSet
from .serializers import CategorySerializer, GenreSerializer
from reviews.models import Category, Genre


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет получения, добавления и удаления категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class GenreViewSet(ListCreateDestroyViewSet):
    """Вьюсет получения, добавления и удаления жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
