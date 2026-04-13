from rest_framework.routers import DefaultRouter
from .views import EvaluationCriteriaViewSet
router = DefaultRouter()
router.register('', EvaluationCriteriaViewSet, basename='evaluation-criteria')
urlpatterns = router.urls
