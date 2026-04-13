from rest_framework.routers import DefaultRouter
from .views import InternshipPlacementViewSet
router = DefaultRouter()
router.register('', InternshipPlacementViewSet, basename='placements')
urlpatterns = router.urls
