import django_filters
from rest_framework import serializers, viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from global_auth.models import CustomUser

model = CustomUser

class Serializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = model
        fields = ['first_name', 'last_name', 'email', 'user_company', 'is_active','last_login','date_joined', 'groups']

class Filter(django_filters.FilterSet):
    class Meta:
        model = model
        fields = '__all__'

class Pagination(PageNumberPagination):
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    page_size = 20
    max_page_size = 100

class ViewSet(viewsets.ModelViewSet):
    queryset = model.objects.all()
    serializer_class = Serializer
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = Filter
    ordering_fields = '__all__'
    ordering = ['-email']

    def get_queryset(self):
        user = self.request.user
        return CustomUser.objects.filter(user_company=user.user_company)


    