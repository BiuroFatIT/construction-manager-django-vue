from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Dodatkowe informacje", {"fields": ("user_company",)}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Dodatkowe informacje", {"fields": ("user_company",)}),
    )

    list_display = BaseUserAdmin.list_display + ("get_company",)

    def get_company(self, obj):
        return obj.user_company.name if obj.user_company else "—"

    get_company.short_description = "Company"