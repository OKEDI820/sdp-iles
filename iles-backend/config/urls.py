"""Top-level URL routing for ILES."""
from django.contrib import admin
from django.urls import include, path

api_v1 = [
    path("auth/", include("apps.users.auth_urls")),
    path("users/", include("apps.users.urls")),
    path("placements/", include("apps.placements.urls")),
    path("logs/", include("apps.logs.urls")),
    path("evaluations/", include("apps.evaluations.urls")),
    path("audit/", include("apps.audit.urls")),
    path("dashboard/", include("apps.dashboard.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(api_v1)),
]
