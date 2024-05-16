from django.conf import settings
from django.urls import include, path

from .views import (
    CategoryViewSet,
    GenreViewSet,
    UserViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet,
    create_user,
    get_token
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
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

auth_urls = [
    path(
        'signup/',
        create_user,
        name='signup'
    ),
    path(
        'token/',
        get_token,
        name='token'
    )
]


urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include(auth_urls))
]
