from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlacementViewSet

router = DefaultRouter()
router.register('placements', PlacementViewSet, basename='placements')

urlpatterns = [
    path('', include(router.urls)),
]
