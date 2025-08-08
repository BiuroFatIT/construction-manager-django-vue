import django_filters
from rest_framework import serializers, viewsets, filters, status
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from global_auth.models import CustomUser
from app_construction_manager.extra.Filters import CustomDateRangeFilter, BooleanInFilter,RelatedNameFilter
from rest_framework.response import Response
from django.contrib.auth.models import Group
from django.db.models import Min

model = CustomUser

class Serializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Group.objects.all(),
        required=False,
    )

    class Meta:
        model = model
        fields = ['id', 'first_name', 'last_name', 'email', 'user_company', 'is_active',
        'last_login','date_joined', 'groups', 'username']

    def create(self, validated_data):
        groups_data = validated_data.pop('groups', None)
        user = model.objects.create(**validated_data)
        
        if groups_data:
            try:
                user.groups.set(groups_data)
            except Exception as e:
                pass  

        return user

class Filter(django_filters.FilterSet):
    id = django_filters.CharFilter(field_name='id', lookup_expr='exact')
    first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = django_filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    email = django_filters.CharFilter(field_name='email', lookup_expr='icontains')
    groups = RelatedNameFilter(field_name='groups', related_field='name', param_name='groups[]')
    is_active = BooleanInFilter(field_name='is_active', lookup_expr='in')
    last_login = CustomDateRangeFilter(field_name='last_login', param_name='last_login[]')
    date_joined = CustomDateRangeFilter(field_name='date_joined', param_name='date_joined[]')

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
    search_fields = ['first_name', 'last_name', 'email', 'user_company__name', 'is_active',
        'last_login','date_joined', 'groups__name']

    def get_queryset(self):
        user = self.request.user
        qs = CustomUser.objects.filter(user_company=user.user_company)

        # Dodajemy adnotację z minimalną nazwą grupy
        qs = qs.annotate(
            first_group_name=Min('groups__name')
        )

        # Pobierz parametry sortowania z zapytania
        ordering = self.request.query_params.get('ordering')
        if ordering:
            # jeśli zamówienie dotyczy groups lub -groups, zamień na first_group_name
            if ordering == 'groups':
                ordering = 'first_group_name'
            elif ordering == '-groups':
                ordering = '-first_group_name'
            qs = qs.order_by(ordering)
        else:
            # domyślne sortowanie (np. email)
            qs = qs.order_by('-email')

        return qs
    
    def create(self, request):
        user = self.request.user
        data = self.request.data.copy()
        data['user_company'] = user.user_company.id
        data['username'] = data['email']
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    