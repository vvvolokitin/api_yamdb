from rest_framework import permissions


class CustomObjectPermissions(permissions.BasePermission):
    """
    Этот класс разрешений предоставляет настраиваемые разрешения
    на основе типа запроса, проверки авторства объекта либо роли пользователя.
    """

    def has_permission(self, request, view):
        """
        Проверка на то, что запрос GET, HEAD или OPTIONS,
        иначе проверка на аутентификацию.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        При запросе конкретного обьекта, если запрос на изменение/удаление,
        то проверяем, что автор запроса == автор обьекта, автор запроса
        модератор или админ. В остальных случаях возвращаем True.
        """
        if request.method not in permissions.SAFE_METHODS:
            return (
                obj.author == request.user
                or request.user.is_moderator()
                or request.user.is_admin()
                or request.user.is_staff
                or request.user.is_superuser
            )
        return True


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
                request.user.is_admin()
                or request.user.is_staff
                or request.user.is_superuser
            )
        )
