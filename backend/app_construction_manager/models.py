from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings


class Address(models.Model):
    street = models.CharField(max_length=255)
    building_number = models.CharField(max_length=10)
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id) + " " + self.street

class Company(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    phone_number_1 = models.CharField(max_length=20)
    phone_number_2 = models.CharField(max_length=20)
    phone_number_3 = models.CharField(max_length=20)
    vat_id = models.CharField(max_length=10)
    regon_id = models.CharField(max_length=14)
    is_active = models.BooleanField()
    timezone = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.id) + " " + str(self.name) 
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price_net = models.FloatField()
    price_gross = models.FloatField()
    estimated_duration_weeks = models.IntegerField()
    usable_area_m2 = models.FloatField()
    net_area_m2 = models.FloatField()
    gross_volume_m3 = models.FloatField()
    is_active = models.BooleanField()
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.id) + " " + str(self.name) 
