from rest_framework import viewsets
from app_construction_manager.models import Company
from app_construction_manager.serializers.Company import ComapnySerializer

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = ComapnySerializer
