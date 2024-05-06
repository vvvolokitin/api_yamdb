from django.shortcuts import render
from rest_framework import filters, viewsets


from .mixins import ListCreateDestroyViewSet
from .serializers import CategorySerializer
from reviews.models import Category


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет получения, добавления и удаления категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer