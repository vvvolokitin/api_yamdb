from rest_framework import permissions


class ReadOrAuthenticatedOrInAuthorModerAdmin(permissions.BasePermission):
    """
    Класс разрешений на получение, создание, обновление, удаление контента

    Аноним может только смотреть, но не трогать;
    аутентифицированный пользователь: смотреть, создавать, менять
    и удалять свой контент;
    админ и модер может создавать, менять и удалять чужой контент.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or (
            obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )


class IsSuperUser(permissions.BasePermission):
    """
    Этот класс разрешений предоставляет разрешения
    только суперпользователям и админам Джанго, либо пользователю с
    ролью админ.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.is_admin
            )
        )


class IsSuperUserOrReadOnly(IsSuperUser):
    """Проверка на суперпользователя или запроса на чтение."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return super().has_permission(request, view)
