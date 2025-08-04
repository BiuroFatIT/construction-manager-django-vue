from django.contrib.auth.models import AbstractUser
from django.db import models
from app_construction_manager.models import Company

class CustomUser(AbstractUser):
    user_company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []