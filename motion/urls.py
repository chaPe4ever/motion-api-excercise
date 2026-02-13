import os

from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt import views as jwt_views

# Determine the base URL for Swagger schema
# In production, use HTTPS; in development, auto-detect
schema_url = None
if not settings.DEBUG:
    # In production, construct HTTPS URL from ALLOWED_HOSTS
    allowed_hosts = os.environ.get("ALLOWED_HOSTS", "").split(",")
    if allowed_hosts and allowed_hosts[0].strip():
        domain = allowed_hosts[0].strip()
        # Remove http:// or https:// if present
        domain = domain.replace("http://", "").replace("https://", "").split("/")[0].split(":")[0]
        if domain:
            schema_url = f"https://{domain}"

schema_view = get_schema_view(
    openapi.Info(
        title="Motion API",
        default_version="v1",
        description="""
API documentation for Motion

## Authentication
This API uses JWT (JSON Web Token) authentication.

### How to authenticate in Swagger:
1. Get a token by calling **POST /api/token/** with your email and password
2. Click the **'Authorize'** button (🔓 at the top right)
3. Paste just your token (no need to add "Bearer" prefix)
4. Click **'Authorize'** and then **'Close'**

That's it! The token will be automatically added to all requests.

**Note:** When using curl or other tools, include "Bearer" prefix:
`Authorization: Bearer YOUR_TOKEN`
        """,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@motion.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    url=schema_url,  # Use HTTPS in production, auto-detect in development
)

urlpatterns = [
    path("health/", lambda r: HttpResponse("ok", content_type="text/plain")),
    path("admin/", admin.site.urls),
    path("backend/api/users/", include("user.urls")),
    path(
        "backend/api/token/",
        jwt_views.TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("backend/api/followers/", include("follow.urls")),
    path("backend/api/posts/", include("post.urls")),
    # Swagger documentation URLs
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
