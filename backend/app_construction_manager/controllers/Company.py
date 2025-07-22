import django_filters
from rest_framework import serializers, viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from app_construction_manager.models import Company

model = Company

class Serializer(serializers.ModelSerializer):
    class Meta:
        model = model
        fields = '__all__'

class Filter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = model
        fields = '__all__'

class Pagination(PageNumberPagination):
    page_query_param = 'pageIndex'
    page_size_query_param = 'pageSize'
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