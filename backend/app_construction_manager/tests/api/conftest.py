import pytest
import os
import environ
from pathlib import Path
import django
from django.conf import settings

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Configure Django settings before importing anything else
if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'global_project.settings')
    django.setup()

# Now we can safely import Django components
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

env = environ.Env(
    # Set default values for environment variables
    DEBUG=(bool, False),  # Default to False if not set
)

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


@pytest.fixture(scope="session")
def test_user_credentials():
    """
    Fixture to provide test user credentials.
    """
    return {
        "username": env("TEST_USER"),
        "password": env("TEST_USER_PASSWORD")
    }


@pytest.fixture(scope="session")
def user(django_db_setup, django_db_blocker, test_user_credentials):
    """
    Session-scoped fixture that creates a test user in the test database.
    """
    User = get_user_model()
    with django_db_blocker.unblock():
        user, created = User.objects.get_or_create(
            username=test_user_credentials["username"]
        )
        if created:
            # Properly set the password with hashing
            user.set_password(test_user_credentials["password"])
            user.save()
    return user


@pytest.fixture(scope="session")
def api_client(user, test_user_credentials, django_db_blocker):
    from rest_framework.test import APIClient

    client = APIClient()
    with django_db_blocker.unblock():
        response = client.post('/api/v1/auth/token/', data=test_user_credentials)
    assert response.status_code == 200, f"Token auth failed: {response.content}"

    access_token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return client


@pytest.fixture(scope="session")
def address(django_db_setup, django_db_blocker):
    from app_construction_manager.models import Address
    with django_db_blocker.unblock():
        return Address.objects.create(
            street="Test Street",
            building_number="123",
            apartment_number="4A",
            postal_code="12345",
            city="Test City",
            state="Test State",
            country="Testland"
        )


@pytest.fixture(scope="session")
def company_payload(user, address):
    def _payload(as_instance=False):
        if as_instance:
            # For creating model instances directly - use actual objects
            payload = {
                "name": "Test Company",
                "email": "test@example.com",
                "address": address,  # Use actual Address object
                "phone_number_1": "123456789",
                "phone_number_2": "987654321",
                "phone_number_3": "456789123",
                "vat_id": "VAT123456",
                "regon_id": "REGON789456123",
                "is_active": True,
                "timezone": "UTC",
                "create_by": user  # Use actual User object
            }
        else:
            # For API calls - try without address ID for creation
            payload = {
                "name": "Test Company",
                "email": "test@example.com",
                "address": {
                    "street": address.street,
                    "building_number": address.building_number,
                    "apartment_number": address.apartment_number,
                    "postal_code": address.postal_code,
                    "city": address.city,
                    "state": address.state,
                    "country": address.country
                },
                "phone_number_1": "123456789",
                "phone_number_2": "987654321",
                "phone_number_3": "456789123",
                "vat_id": "VAT123456",
                "regon_id": "REGON789456123",
                "is_active": True,
                "timezone": "UTC",
                "create_by": user.id  # Use User ID
            }
        return payload
    return _payload
