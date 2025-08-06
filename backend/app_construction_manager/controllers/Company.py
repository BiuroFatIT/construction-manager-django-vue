import django_filters
from rest_framework import serializers, viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from app_construction_manager.models import Company, Address
from django.db import models
from datetime import datetime, timedelta

model = Company

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
    
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class Serializer(serializers.ModelSerializer):
    address = AddressSerializer()
    create_by = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = model
        fields = '__all__'

    def create(self, validated_data):
        # 1. Extract nested address data from incoming JSON
        address_data = validated_data.pop('address')

        # 2. Create the Address instance
        address = Address.objects.create(**address_data)

        # 3. If request is available, auto-fill 'create_by' field
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['create_by'] = request.user

        # 4. Create the Company with the address assigned
        company = Company.objects.create(address=address, **validated_data)
        return company
    
    def update(self, instance, validated_data):
        # Handle nested address update
        address_data = validated_data.pop('address', None)
        if address_data:
            address_instance = instance.address
            for attr, value in address_data.items():
                setattr(address_instance, attr, value)
            address_instance.save()

        # Handle Company fields update
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class Filter(django_filters.FilterSet):
    id_min = django_filters.NumberFilter(field_name='id', lookup_expr='gte')
    id_max = django_filters.NumberFilter(field_name='id', lookup_expr='lte')
    is_active = BooleanInFilter(field_name='is_active', lookup_expr='in')
    created_at = CustomDateRangeFilter(field_name='created_at', param_name='created_at[]')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    email = django_filters.CharFilter(field_name='email', lookup_expr='icontains')
    phone_number_1 = django_filters.CharFilter(field_name='phone_number_1', lookup_expr='icontains')
    vat_id = django_filters.CharFilter(field_name='vat_id', lookup_expr='icontains')
    regon_id = django_filters.CharFilter(field_name='regon_id', lookup_expr='icontains')
    address__state = django_filters.CharFilter(field_name='address__state', lookup_expr='icontains')
    address__city = django_filters.CharFilter(field_name='address__city', lookup_expr='icontains')
    address__postal_code = django_filters.CharFilter(field_name='address__postal_code', lookup_expr='icontains')

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
    search_fields = ['id', 'is_active', 'name', 'email', 'phone_number_1', 'vat_id', 'regon_id', 'address__state',
                     'address__city', 'address__postal_code']



    