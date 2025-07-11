# backend/global_auth/api/views.py

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .serializers import CustomUserSerializer, RegistrationSerializer
from ..models import CustomUser


class CustomUserViewSet(viewsets.ModelViewSet):
    """
    CRUD dla CustomUser + dodatkowa akcja /me/
    - GET    /api/v1/auth/users/       → lista
    - POST   /api/v1/auth/users/       → tworzenie
    - GET    /api/v1/auth/users/{pk}/  → szczegóły
    - PUT    /api/v1/auth/users/{pk}/  → edycja
    - DELETE /api/v1/auth/users/{pk}/  → usunięcie
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """ GET /api/v1/auth/users/me/ """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class RegisterView(CreateAPIView):
    """
    POST /api/v1/auth/register/
    Rejestracja nowego użytkownika
    """
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]
