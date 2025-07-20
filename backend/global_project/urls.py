from django.contrib import admin
from django.urls import path, include, re_path
from .views import FrontendAppView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),

    # JWT endpoints (możesz je zostawić tutaj)
    path("api/v1/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Wszystkie endpointy userów (register, users/, users/me/) są tutaj:
    path("api/v1/auth/", include(("global_auth.api.urls", "global_auth"), namespace="auth-api")),
    
    # Frontend app view
    re_path(r"^(?!api/).*", FrontendAppView.as_view(), name="spa"),

    # API Construction Manage
    path('api/construction/manager/', include('app_construction_manager.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])