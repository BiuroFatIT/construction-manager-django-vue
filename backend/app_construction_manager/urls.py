from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app_construction_manager.controllers.Company import ViewSet as CompanyViewSet
from app_construction_manager.controllers.Products import ViewSet as ProductsViewSet

router = DefaultRouter()
router.register(r'company', CompanyViewSet)
router.register(r'products', ProductsViewSet)

urlpatterns = [
    path('', include(router.urls))
]
