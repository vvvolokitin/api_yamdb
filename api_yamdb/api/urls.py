from django.conf import settings
from django.urls import include, path

from .views import CategoryViewSet, GenreViewSet

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

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
