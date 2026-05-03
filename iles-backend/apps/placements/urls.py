from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PlacementViewSet

router = DefaultRouter()
router.register("", PlacementViewSet, basename="placements")

urlpatterns = [path("", include(router.urls))]
