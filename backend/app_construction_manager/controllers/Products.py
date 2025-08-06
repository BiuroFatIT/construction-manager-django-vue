import django_filters
from rest_framework import serializers, viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from app_construction_manager.models import Product
from django.db import models
from datetime import datetime, timedelta

model = Product

class CustomDateRangeFilter(django_filters.Filter):
    def __init__(self, *args, param_name=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.param_name = param_name or self.field_name

    def filter(self, qs, value):
        values = self.parent.request.GET.getlist(self.param_name)

        if len(values) == 2:
            start, end = values
            try:
                start_date = datetime.strptime(start, "%Y-%m-%d").date()
                end_date = datetime.strptime(end, "%Y-%m-%d").date() + timedelta(days=1)
            except ValueError:
                return qs.none()  # Błędny format daty

            return qs.filter(**{
                f"{self.field_name}__gte": start_date,
                f"{self.field_name}__lt": end_date
            })
        return qs
    
class BooleanInFilter(django_filters.BaseInFilter, django_filters.BooleanFilter):
    def filter(self, qs, value):
        param_name = self.field_name + '[]'
        values = self.parent.request.GET.getlist(param_name)
        if not values:
            values = self.parent.request.GET.getlist(self.field_name)
        if values:
            # Konwersja stringów na boolean
            bool_values = [val.lower() == 'true' for val in values if val.lower() in ('true', 'false')]
            return qs.filter(**{f"{self.field_name}__in": bool_values})
        return qs
    
class Serializer(serializers.ModelSerializer):
    class Meta:
        model = model
        fields = '__all__'

class Filter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    usable_area_m2_min = django_filters.NumberFilter(field_name='usable_area_m2', lookup_expr='gte')
    usable_area_m2_max = django_filters.NumberFilter(field_name='usable_area_m2', lookup_expr='lte')

    class Meta:
        model = model
        fields = '__all__'

class Pagination(PageNumberPagination):
    page_query_param = 'page'
    page_size_query_param = 'page_size'

class ViewSet(viewsets.ModelViewSet):
    queryset = model.objects.all()
    serializer_class = Serializer
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = Filter
    ordering_fields = '__all__'
    ordering = ['-created_at']
    search_fields = ['id', 'name', 'description', 'price_net', 'price_gross', 'estimated_duration_weeks', 'usable_area_m2', 
                     'net_area_m2', 'gross_volume_m3', 'is_active']



    