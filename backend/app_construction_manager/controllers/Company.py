import django_filters
from rest_framework import serializers, viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from app_construction_manager.models import Company
from django.db import models

model = Company

class Serializer(serializers.ModelSerializer):
    class Meta:
        model = model
        fields = '__all__'

class Filter(django_filters.FilterSet):
    id_min = django_filters.NumberFilter(field_name='id', lookup_expr='gte')
    id_max = django_filters.NumberFilter(field_name='id', lookup_expr='lte')

    class Meta:
        model = model
        fields = '__all__'
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.TextField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.EmailField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.AutoField: {
                'filter_class': django_filters.NumericRangeFilter, 
                'extra': lambda f: {
                    'lookup_expr': 'range',
                },
            },
        }

class Pagination(PageNumberPagination):
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    page_size = 20
    max_page_size = 100

class ViewSet(viewsets.ModelViewSet):
    queryset = model.objects.all()
    serializer_class = Serializer
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = Filter
    ordering_fields = '__all__'
    ordering = ['-created_at']



    