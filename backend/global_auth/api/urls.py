# backend/global_auth/api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet, RegisterView

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')

urlpatterns = [
    # Rejestracja
    path('register/', RegisterView.as_view(), name='auth-register'),
    # Wszystkie /users/ i custom action /users/me/
    path('', include(router.urls)),
]
