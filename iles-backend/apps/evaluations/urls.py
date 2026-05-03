from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EvaluationCriterionViewSet, EvaluationViewSet

router = DefaultRouter()
router.register("criteria", EvaluationCriterionViewSet, basename="criteria")
router.register("", EvaluationViewSet, basename="evaluations")

urlpatterns = [path("", include(router.urls))]
