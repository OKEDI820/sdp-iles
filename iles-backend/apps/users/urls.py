from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CurrentUserView, UserViewSet

router = DefaultRouter()
router.register('', UserViewSet, basename='users')

urlpatterns = [
    path('me/', CurrentUserView.as_view(), name='current-user'),
    path('', include(router.urls)),
]
