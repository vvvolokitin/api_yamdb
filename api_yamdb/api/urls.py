from django.conf import settings
from django.urls import include, path

from .views import (
    CategoryViewSet,
    GenreViewSet,
    UserCreateViewSet,
    UserReceiveTokenViewSet,
    UserViewSet,
    TitleViewSet
)


if settings.DEBUG:
    from rest_framework.routers import DefaultRouter as Router
else:
    from rest_framework.routers import SimpleRouter as Router

app_name = 'api'

router_v1 = Router()
router_v1.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)
router_v1.register(
    'genres',
    GenreViewSet,
    basename='genres'
)
router_v1.register(
    'users',
    UserViewSet,
    basename='users'
)
router_v1.register(
    'titles',
    TitleViewSet,
    basename='titles'
)

auth_urls = [
    path(
        'signup/',
        UserCreateViewSet.as_view({'post': 'create'}),
        name='signup'
    ),
    path(
        'token/',
        UserReceiveTokenViewSet.as_view({'post': 'create'}),
        name='token'
    )
]


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(auth_urls))
]
