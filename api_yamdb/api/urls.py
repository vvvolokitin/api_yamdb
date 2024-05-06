from django.conf import settings
from django.urls import include, path

from .views import CategoryViewSet

if settings.DEBUG:
    from rest_framework.routers import DefaultRouter as Router
else:
    from rest_framework.routers import SimpleRouter as Router


router_v1 = Router()
router_v1.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)

urlpatterns = [
    path('v1', include(router_v1.urls)),
]

