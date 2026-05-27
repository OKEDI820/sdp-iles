"""URL configuration for config project."""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('api/v1/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/auth/', include('apps.users.urls')),

    # Resources
    path('api/v1/users/', include('apps.users.urls')),
    path('api/v1/logs/', include('apps.logs.urls')),
    path('api/v1/placements/', include('apps.placements.urls')),
    path('api/v1/evaluations/', include('apps.evaluations.urls')),
    path('api/v1/dashboard/', include('apps.dashboard.urls')),
]