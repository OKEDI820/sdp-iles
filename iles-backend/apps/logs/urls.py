from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import WeeklyLogViewSet

router = DefaultRouter()
router.register("", WeeklyLogViewSet, basename="logs")

urlpatterns = [path("", include(router.urls))]
