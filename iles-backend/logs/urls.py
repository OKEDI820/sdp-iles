from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WeeklyLogViewSet

router = DefaultRouter()
router.register("logs", WeeklyLogViewSet, basename="logs")

urlpatterns = [
    path("", include(router.urls)),
]
