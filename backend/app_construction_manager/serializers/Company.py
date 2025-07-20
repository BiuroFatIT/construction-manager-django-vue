from rest_framework import serializers
from app_construction_manager.models import Company

class ComapnySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'