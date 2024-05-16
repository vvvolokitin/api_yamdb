from rest_framework import mixins, viewsets, serializers
from rest_framework.response import Response


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class PatchModelMixin:
    def perform_update(self, serializer):
        self.perform_create(serializer)

    def partial_update(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            self.get_object(),
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class ValidateUsernameMixin:
    def validate_username(self, username):
        if username and username.lower() == 'me':
            raise serializers.ValidationError('Имя не может быть <me>')
        return username
