from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from users.urls import users_urlpatterns, auth_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("tickets/", include("tickets.urls", namespace="tickets")),
    path("users/", include((users_urlpatterns, "users"), namespace="users")),
    path("auth/", include((auth_urlpatterns, "auth"), namespace="auth")),
]
